"""
DCOMP320 - Data Structures and Algorithm
Stack-Based Mathematical Expression Evaluator

Uses the Shunting Yard algorithm to convert infix expressions to postfix,
then evaluates the postfix expression using a value stack.
No eval() or equivalent shortcuts are used.
"""


# ─────────────────────────────────────────────
#  Stack Implementation
# ─────────────────────────────────────────────

class Stack:
    """Custom stack data structure backed by a Python list."""

    def __init__(self):
        self._data = []

    def push(self, item):
        """Push an item onto the top of the stack."""
        self._data.append(item)

    def pop(self):
        """Remove and return the top item. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Pop from an empty stack")
        return self._data.pop()

    def peek(self):
        """Return the top item without removing it. Raises IndexError if empty."""
        if self.is_empty():
            raise IndexError("Peek at an empty stack")
        return self._data[-1]

    def is_empty(self):
        """Return True if the stack has no items."""
        return len(self._data) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._data)

    def __repr__(self):
        return f"Stack({self._data})"


# ─────────────────────────────────────────────
#  Tokenizer
# ─────────────────────────────────────────────

def tokenize(expression):
    """
    Split an infix expression string into a list of tokens.
    Tokens are: numbers (int or float), operators (+, -, *, /),
    and parentheses.

    Handles unary minus by inserting a '0' before a leading '-'
    or a '-' that follows an operator or opening parenthesis.

    Returns a list of token strings, or raises ValueError on bad input.
    """
    tokens = []
    i = 0
    expr = expression.strip()

    while i < len(expr):
        ch = expr[i]

        # Skip whitespace
        if ch.isspace():
            i += 1
            continue

        # Number (integer or decimal)
        if ch.isdigit() or ch == '.':
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(expr[i:j])
            i = j
            continue

        # Operator or parenthesis
        if ch in '+-*/()':
            # Detect unary minus: '-' at start, or after operator / '('
            if ch == '-' and (
                len(tokens) == 0 or
                tokens[-1] in ('+', '-', '*', '/', '(')
            ):
                # Unary minus — insert 0 so it becomes "0 - x"
                tokens.append('0')

            tokens.append(ch)
            i += 1
            continue

        # Anything else is an invalid character
        raise ValueError(f"Invalid character '{ch}' in expression: {expression}")

    return tokens


# ─────────────────────────────────────────────
#  Shunting Yard: Infix → Postfix
# ─────────────────────────────────────────────

# Operator precedence (higher number = higher precedence)
PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}


def infix_to_postfix(tokens):
    """
    Convert a list of infix tokens to postfix (Reverse Polish Notation)
    using the Shunting Yard algorithm.

    Returns a list of tokens in postfix order.
    Raises ValueError for mismatched parentheses.
    """
    output = []          # postfix output queue
    op_stack = Stack()   # operator stack

    for token in tokens:
        if _is_number(token):
            output.append(token)

        elif token in PRECEDENCE:
            # Pop operators with greater or equal precedence (left-associative)
            while (
                not op_stack.is_empty() and
                op_stack.peek() in PRECEDENCE and
                PRECEDENCE[op_stack.peek()] >= PRECEDENCE[token]
            ):
                output.append(op_stack.pop())
            op_stack.push(token)

        elif token == '(':
            op_stack.push(token)

        elif token == ')':
            # Pop until matching '('
            while not op_stack.is_empty() and op_stack.peek() != '(':
                output.append(op_stack.pop())
            if op_stack.is_empty():
                raise ValueError("Mismatched parentheses: missing '('")
            op_stack.pop()  # discard the '('

        else:
            raise ValueError(f"Unknown token: {token}")

    # Drain remaining operators
    while not op_stack.is_empty():
        top = op_stack.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses: missing ')'")
        output.append(top)

    return output


def _is_number(token):
    """Return True if the token represents a numeric value."""
    try:
        float(token)
        return True
    except (ValueError, TypeError):
        return False


# ─────────────────────────────────────────────
#  Postfix Evaluator
# ─────────────────────────────────────────────

def evaluate_postfix(postfix_tokens):
    """
    Evaluate a postfix token list using a value stack.

    Returns the numeric result (int if whole number, float otherwise).
    Raises ValueError for invalid expressions and ZeroDivisionError for /0.
    """
    value_stack = Stack()

    for token in postfix_tokens:
        if _is_number(token):
            value_stack.push(float(token))

        elif token in PRECEDENCE:
            if value_stack.size() < 2:
                raise ValueError("Invalid expression: not enough operands")

            right = value_stack.pop()
            left = value_stack.pop()

            if token == '+':
                result = left + right
            elif token == '-':
                result = left - right
            elif token == '*':
                result = left * right
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                result = left / right

            value_stack.push(result)

        else:
            raise ValueError(f"Unknown postfix token: {token}")

    if value_stack.size() != 1:
        raise ValueError("Invalid expression: too many operands")

    result = value_stack.pop()

    # Return as int if the result is a whole number
    if result == int(result):
        return int(result)
    return result


# ─────────────────────────────────────────────
#  High-level Expression Evaluator
# ─────────────────────────────────────────────

def evaluate_expression(expression):
    """
    Evaluate a single infix expression string.

    Pipeline:
        expression string
          → tokenize()
          → infix_to_postfix()   (Shunting Yard)
          → evaluate_postfix()
          → result

    Returns the numeric result, or raises an exception with a descriptive
    message on failure.
    """
    stripped = expression.strip()
    if not stripped:
        raise ValueError("Empty expression")

    tokens = tokenize(stripped)

    if not tokens:
        raise ValueError("Expression contains no valid tokens")

    postfix = infix_to_postfix(tokens)
    return evaluate_postfix(postfix)


# ─────────────────────────────────────────────
#  File I/O
# ─────────────────────────────────────────────

SEPARATOR_PREFIX = '-----'


def is_separator(line):
    """Return True if the line is a separator (only dashes)."""
    stripped = line.strip()
    return bool(stripped) and all(c == '-' for c in stripped)


def process_files(input_path='input.txt', output_path='output.txt'):
    """
    Read expressions from input_path, evaluate each one, and write
    results to output_path. Separator lines are preserved as-is.
    """
    try:
        with open(input_path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: Input file '{input_path}' not found.")
        return

    results = []

    for line in lines:
        raw = line.rstrip('\n')

        if is_separator(raw):
            # Preserve separator line exactly
            results.append(raw)
            continue

        if not raw.strip():
            # Preserve blank lines
            results.append(raw)
            continue

        # Try to evaluate the expression
        try:
            result = evaluate_expression(raw)
            results.append(str(result))
            print(f"  {raw.strip():<30} =>  {result}")
        except ZeroDivisionError as e:
            error_msg = f"ERROR: {e}"
            results.append(error_msg)
            print(f"  {raw.strip():<30} =>  {error_msg}")
        except ValueError as e:
            error_msg = f"ERROR: {e}"
            results.append(error_msg)
            print(f"  {raw.strip():<30} =>  {error_msg}")

    with open(output_path, 'w') as f:
        f.write('\n'.join(results))
        if results:
            f.write('\n')

    print(f"\nResults written to '{output_path}'")


# ─────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 50)
    print("  DCOMP320 Stack Expression Evaluator")
    print("=" * 50)
    print()
    process_files('input.txt', 'output.txt')
