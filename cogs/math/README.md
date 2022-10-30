# Math

## Summary

A basic calculator with support for:

- Addition, subtraction, multiplication, and division
- Exponentiation and square roots
- Modulo and absolute value
- Sine, cosine, and tangent
- Two constants: e and pi

Although order of operations is mostly respected, it is good practice to be
explicit with grouping. Due to the calculator's internal design, addition and
subtraction has higher precedence than exponentiation, e.g. `2^7 - 1` is read
as `2^(7 - 1)` rather than `(2^7) - 1` as normal order of operations would
dictate.

## Examples

`!calc (2^97) - 1` yields `158456325028528675187087900671`

`!calc sqrt(pi)` yields `1.7724538509055159`
