# 第六题：Agent 上下文工程

## **试题背景**

2026 年以来，Agent 领域的前沿重心正从"更强的模型"转向"更强的 Harness"：Claude Code、Codex 等产品的核心竞争力不仅仅在于底座模型本身，更在于模型外层的"Harness"——上下文压缩（compaction）、记忆系统（memory）、子 Agent 上下文管理、Plan-and-Execute、自我验证循环。这套思想被称为 **Context Engineering**。

本题将复现 Agent 上下文工程的设计与实现：我们提供了一个上下文被硬性截断到 4096 token 的弱上下文 LLM 接口，以及一个信息总量远超 4096 token 的长程任务集。单上下文、无记忆的朴素 ReAct Agent 在这个任务集上必然失败。我们希望你：**在模型不变、上下文窗口不变的前提下，仅靠 Harness 设计提升长程 Agent 性能**，并在我们的基准实验数据集上进行验证。

## **考试环境提供**

1. `limited_llm.py`：一个 OpenAI 兼容客户端的包装器。每次调用前，它会用 `tiktoken` 统计消息总 token 数，只保留 system prompt + 最近 4096 token，更早的消息直接丢弃（不报错）。你可以把底层 endpoint 指向任何第三方模型厂商的 API 或本地部署的 Qwen2.5-7B 等任何 OpenAI 兼容服务，但**不得修改、绕过我们提供的上下文截断环境**。评分时我们会检查该文件的哈希。
2. `tests/`：参照 [CORE-Bench](https://huggingface.co/datasets/zhangfw123/CORE-Bench) 和 [SWE-bench](https://www.swebench.com/) 设计的测试数据集。每个任务是一个独立的小型 Python 项目目录（10~30 个文件，总文本量约 20k token），其中：
   1. 存在若干真实 bug，位于某个 `src/*.py` 中；
   2. 提供 `tests/test_task.py`，`pytest` 全绿即判该任务通过；
   3. 仓库中 70% 以上文件是干扰信息（长日志、无关文档、命名诱人的错误"答案文件"、一份会误导你去找错误文件的 README）；
   4. 任何单一文件都不超过 1500 token，但"全部读一遍"必然撑爆上下文。

## **任务要求**

### **Part 1：最小 Agent Loop（3 分）**

可以自由选用 LangChain / Langg raph / AutoGen / OpenAI Agents SDK 等 Agent 框架，也可以不依赖任何 Agent 框架，手写一个 Agent 主循环的最小代码：解析模型输出的工具调用（可用 JSON 协议或 XML 协议自定）、执行、把结果回填、直到模型输出终止标记。工具集合由参赛者自行设计，不限定工具数量、名称或具体接口形式，但应围绕代码检索、局部内容读取、文件修改、测试验证等软件调试所需能力展开，并可在后续任务阶段中补充设计工具，要求：

- 不得提供可执行任意 Shell 命令、执行任意 Python 代码或其他等价的通用代码执行工具
- 单个任务内工具调用上限 60 次，超出判定为违规。
- 应在说明文档中简要解释工具集合的设计思路，包括：为什么选择这些工具、如何控制上下文增长，以及这些限制如何影响 Agent 的定位、修改与验证策略。

## **Part 2：Harness 设计与评测消融（4 分）**

### **2.1 经典机制实现（任选两种完成）**

1. **Compaction**：上下文占用超过阈值时，触发一次"用 LLM 总结历史"的压缩，把对话历史替换为结构化状态。
2. **外置记忆文件**：Agent 主动维护工作目录下 `NOTES.md` 并按需召回，设计分级记忆系统等。
3. **探索子 Agent**：允许主 Agent 派生子 Agent，授予只读工具（read/grep），由子 Agent 返回探索结果。
4. **分步计划跟踪**：强制 Agent 先产出分步计划（todo list），每步完成后更新状态，计划本身作为独立短消息常驻上下文。

### **2.2 机制创新设计**

- 自由设计并实现一种机制，写明设计动机、创新点和优缺点等，纳入下方消融。

### **2.3 评测与消融**

Agent 领域有一个共识是，"没有 eval 就没有系统"。要求：

1. 编写测试脚本：批量测试，并输出每个任务的 通过/失败、工具调用次数、上下文窗口变化、触发的 Harness 机制列表、总耗时。
2. 消融实验：在同一底座模型、同一任务集上，分别运行：
   - (a) Baseline（最小 Agent Loop）；
   - (b) 你的完整 Harness；
   - (c) 你的 Harness 去掉你认为贡献最大的一项机制。

最终以 `REPORT.md` 的形式提交对消融实验结论的分析及其机制的解释、失败的根因与改进等。

## **Part 3：前沿思考与探索**

### **3.1 经典文献阅读**

阅读 *[ReAct: Synergizing Reasoning and Acting in Language Models, 2022](https://arxiv.org/abs/2210.03629)*，总结论文中提出的经典方法，并结合本题谈谈你有什么新的感悟。

### **3.2 前沿文献阅读**

阅读 [Anthropic, Effective context engineering for AI agents, 2025](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

- 总结其中对 Context Engineering 的核心定义，以及其关于上下文选择、Just-in-Time 信息获取、Compaction、结构化 Memory、Sub-agent 等机制的设计思想。
- 结合本题中 4096 token 的受限上下文环境，以及你在 Part 2 中动手实现的 Harness，思考为什么单纯扩大模型上下文窗口并不能完全解决长程 Agent 的问题？关于提升 Agent 在实际任务中的表现，你有什么新的启发和思考？

### **3.3 开放思考**

相比传统 AI 使用方式，你在完成本项目过程中是如何更高效、更好地使用 AI 的？你认为 LLM / Agent 时代人的核心竞争力和关键能力是什么？