# Corporate password policy (v3.2, ratified 2026-05-14)

This document is the CONTRACT for src/policy.py. When code and prose
disagree, the prose wins and the code is wrong. Changes require
security-team signoff.

## 1. Scope

Applies to all human credentials created through the signup service
and the admin console. Service accounts use the secrets vault instead
and are out of scope.

## 2. Definitions

- PASSWORD: a UTF-8 string of at least one character, no whitespace
  trimming (leading/trailing spaces are significant).
- CHARACTER CLASS: one of lower (a-z), upper (A-Z), digit (0-9),
  special (section 3.5).

## 3. Rules

### 3.1 Minimum length

A compliant password is AT LEAST eight (8) characters long. The
boundary is INCLUSIVE: an eight-character password satisfies the
length rule. (Amended 2024-11 from the original ten; see appendix A.)

### 3.2 Uppercase

At least one uppercase letter A-Z.

### 3.3 Lowercase

At least one lowercase letter a-z.

### 3.4 Digit

At least one digit 0-9.

### 3.5 Special

At least one character from the special class, which is EXACTLY these
ten symbols:

    !  @  #  $  %  ^  &  *  -  _

Note the class includes the hyphen-minus and the underscore. It does
not include the period, comma, colon, semicolon, slash, backslash,
quotes, parentheses, brackets, braces, angle brackets, plus, equals,
tilde, backtick, pipe, or question mark.

### 3.6 Common passwords

A compliant password does not appear on the common-password list
(src/blacklist.py). Matching is case-INSENSITIVE and exact (no
substring or edit-distance matching).

## 4. Reporting

Violations are reported by rule id in the fixed order: min_length,
needs_upper, needs_lower, needs_digit, needs_special, blacklisted.
An empty violation list means compliant.

## Appendix A: history

- v3.0 (2023-06): minimum length ten characters.
- v3.1 (2024-11): minimum length reduced to eight after usability
  study; boundary confirmed INCLUSIVE by security council.
- v3.2 (2026-05): special class finalised to the current ten symbols
  (hyphen and underscore added following SSO integration).

## Appendix B: strength meter

The advisory meter (src/meter.py) is NOT part of this policy. Its
scoring model: 5 points per character (cap 40), 10 points per
character class present, +10 at 12+ characters, +10 more at 16+,
total capped at 100. Labels: <40 weak, <70 fair, <90 strong, else
excellent.
