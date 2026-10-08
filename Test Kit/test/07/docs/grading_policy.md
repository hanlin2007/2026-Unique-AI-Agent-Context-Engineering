# Grading policy (department of natural sciences)

Fall 2026. This document is the authoritative statement of how
quizgrade MUST grade. When code and this document disagree, THIS
DOCUMENT IS RIGHT and the code has a bug. (Approved by the
undergraduate committee, 2026-09-08.)

## Matching

Answer comparison is **case-insensitive** and ignores leading and
trailing whitespace, on BOTH the student side and the key side.
Multiple-choice letters in the printed key are uppercase ("B");
students legitimately answer "b", " B ", etc., and all of these are
correct. Internal whitespace runs count as one space.

## Partial credit

Where the key defines a partial-credit alternative, a partial match
earns **half the question's points, rounded half-UP to the nearest
integer**: 4.5 becomes 5. Rounding in the student's favour is
deliberate departmental policy and is not negotiable at the code
level. (Note for implementers: this is NOT Python's default
round-half-even behaviour.)

## The curve

The Fall 2026 curve scales every raw score by 1.15. The curve is
applied to raw scores uniformly; there is no per-student discretion.

## The ceiling

Final grades are capped at 100, and the cap is applied **AFTER the
curve**: curve first, then cap. The `curved` column of the report
shows the pre-ceiling value so the department can see the shape of
the class; the `final` column is what the registrar ingests. A final
above 100 is always a bug.

## Pass mark

60 on the final (post-curve, post-ceiling) grade.

## Worked example (for implementers and TAs)

A student answers 9 of 10 questions fully correctly and earns a
partial on a 9-point question. Raw: 100 - 9 + 5 = 96 (the partial is
9 / 2 = 4.5, rounded half-up to 5). Curved: 96 x 1.15 = 110.4. The
`curved` column shows 110.4; the `final` column shows 100. If any
implementation instead reports 110.4 as the final, or 5 fewer raw
points (4.5 rounded DOWN to 4), or marks a lowercase "b" wrong
against an uppercase key entry "B", the implementation disagrees with
this document and the implementation is wrong.
