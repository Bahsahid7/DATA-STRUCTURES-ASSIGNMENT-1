# DCOMP320 – Stack-Based Mathematical Expression Evaluator

**Course:** DCOMP320 – Data Structures and Algorithm  
**Assignment:** Stacks Implementation  
**Semester:** 03&05 (September 2026 – February 2027)  
**Institution:** Limkokwing University of Creative Technology – Sierra Leone

---

## How to Run

### Requirements
- Python 3.7 or higher
- No external libraries required

### Steps

1. Place your expressions in `input.txt` (one expression per line, separated by `-----` lines).
2. Run the evaluator:

```bash
python stack_expression_evaluator.py
```

3. Results are written to `output.txt` in the same format as the input.

### Run the Tests

```bash
python -m unittest tests/test_stack_expression_evaluator.py -v
```

---

## Input File Format (`input.txt`)

- Each mathematical expression goes on its own line.
- Expressions are separated by lines containing only dashes (`-----`).
- Supported operators: `+`, `-`, `*`, `/`
- Parentheses are supported and evaluated first.
- Integer and decimal numbers are both supported.
- Negative numbers are supported (e.g., `-3 + 5`).

**Example `input.txt`:**

```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

---

## Output File Format (`output.txt`)

- Each result is written on the same line position as its corresponding expression.
- Separator lines (`-----`) are preserved exactly as they appear in the input.
- If an expression is invalid, the line in the output reads `ERROR: <reason>` instead of a number.
- Whole-number results are written as integers (e.g., `13`, not `13.0`).
- Decimal results are written as floating-point numbers (e.g., `3.3333333333333335`).

**Example `output.txt`** (corresponding to the input above):

```
13
-----
16
-----
-10
```

---

## Operator Precedence

The evaluator follows standard mathematical precedence rules:

| Priority | Operator        |
|----------|-----------------|
| 1 (highest) | `( )` Parentheses |
| 2        | `*` `/` Multiply / Divide |
| 3 (lowest)  | `+` `-` Add / Subtract |

Operators at the same precedence level are evaluated left to right.

---

## Project Structure

```
dcomp320-stack-assignment/
│
├── stack_expression_evaluator.py   # Main program
├── input.txt                       # Sample input expressions
├── output.txt                      # Generated results (created on run)
└── tests/
    └── test_stack_expression_evaluator.py  # Unit tests (51 tests)
```

---

## Assumptions and Limitations

- **No `eval()`:** The program does not use Python's built-in `eval()` function or any equivalent. All evaluation is done via the custom Stack class and the Shunting Yard algorithm.
- **Separator lines** must contain only dash (`-`) characters. Any other characters on a line will be treated as an expression.
- **Blank lines** in the input are preserved as blank lines in the output.
- **Unary minus** is supported at the start of an expression or after an opening parenthesis (e.g., `-3 + 5`, `(-3 * 2)`). Unary plus is not supported.
- **Integer results:** If a result has no fractional part (e.g., `8 / 2 = 4.0`), it is written as an integer (`4`).
- **Division by zero** produces an `ERROR:` line in the output; the program continues processing remaining expressions.
- **Invalid expressions** (mismatched parentheses, unknown characters, missing operands) also produce `ERROR:` lines without crashing the program.
- The input file must be named `input.txt` and must exist in the same directory as the script, or a custom path can be passed to `process_files()` in the source code.
