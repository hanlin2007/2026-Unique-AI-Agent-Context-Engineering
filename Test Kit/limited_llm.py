"""
limited_llm.py — 受限上下文 LLM 包装器

1.每次调用前用 tiktoken 统计消息总 token 数：
2.只保留 system prompt + 最近 MAX_CONTEXT_TOKENS 个 token 的消息，更早的消息被直接丢弃，并不产生产生报错

"""
import tiktoken
from openai import OpenAI

MAX_CONTEXT_TOKENS = 4096  # 硬性上下文上限

# qwen 系列没有官方 tiktoken encoding，用 cl100k_base 近似计数；
# 近似保证截断的"口径一致"，而不要求与真实模型的 tokenizer 完全一致
_ENC = tiktoken.get_encoding("cl100k_base")

# 每条消息的角色标签与分隔符的近似格式开销
_PER_MESSAGE_OVERHEAD = 4


def num_tokens(messages):
    """统计一组消息的总 token 数（content 为空按 0 计）。"""
    total = 0
    for m in messages:
        total += _PER_MESSAGE_OVERHEAD
        total += len(_ENC.encode(m.get("role", "")))
        total += len(_ENC.encode(m.get("content") or ""))
    return total


def truncate_messages(messages, max_tokens=MAX_CONTEXT_TOKENS):
    """截断消息列表：保留全部 system 消息 + 最近的若干条，使总量 ≤ max_tokens。

    更早的消息被静默丢弃（不报错）；至少保留最新一条非 system 消息，
    哪怕它单条就超限（否则请求里没有任何用户输入，模型无从响应）。
    """
    system = [m for m in messages if m.get("role") == "system"]
    rest = [m for m in messages if m.get("role") != "system"]

    kept = []
    budget = max_tokens - num_tokens(system)
    for m in reversed(rest):  # 从最新往最旧装
        cost = num_tokens([m])
        if kept and cost > budget:
            break
        kept.append(m)
        budget -= cost
    return system + list(reversed(kept))


class LimitedLLM:
    """OpenAI 兼容客户端的受限包装，调用方式与 chat.completions.create 对齐。"""

    def __init__(self, base_url, api_key, model, max_tokens=MAX_CONTEXT_TOKENS):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

        # 调试/测试用：记录上一次实际发出的消息（截断后的），不影响截断逻辑
        self.last_sent_messages = None

    def chat(self, messages, **kwargs):
        """先截断、再转发给底层模型；返回值与 openai 的响应对象相同。"""

        messages = truncate_messages(messages, self.max_tokens)
        self.last_sent_messages = messages
        return self.client.chat.completions.create(
            model=self.model, messages=messages, **kwargs
        )
