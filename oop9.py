import math
from fractions import Fraction


class Rational:
    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, str):
            parts = numerator.split('/')
            if len(parts) == 1:
                self.n = int(parts[0])
                self.d = 1
            elif len(parts) == 2:
                self.n = int(parts[0])
                self.d = int(parts[1])
            else:
                raise ValueError("Invalid rational number format")
        else:
            self.n = numerator
            self.d = denominator

        if self.d == 0:
            raise ZeroDivisionError("Denominator cannot be zero")

        self._simplify()

    def _simplify(self):
        common_divisor = math.gcd(abs(self.n), abs(self.d))
        self.n = self.n // common_divisor
        self.d = self.d // common_divisor
        if self.d < 0:
            self.n *= -1
            self.d *= -1

    def __add__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        new_n = self.n * other.d + other.n * self.d
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        new_n = self.n * other.d - other.n * self.d
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        new_n = self.n * other.n
        new_d = self.d * other.d
        return Rational(new_n, new_d)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Rational(other)
        if not isinstance(other, Rational):
            return NotImplemented
        if other.n == 0:
            raise ZeroDivisionError("Division by zero")
        new_n = self.n * other.d
        new_d = self.d * other.n
        return Rational(new_n, new_d)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    def __call__(self):
        return self.n / self.d

    def __getitem__(self, key):
        if key == "n":
            return self.n
        elif key == "d":
            return self.d
        else:
            raise KeyError("Key must be 'n' or 'd'")

    def __setitem__(self, key, value):
        if key == "n":
            self.n = value
        elif key == "d":
            if value == 0:
                raise ZeroDivisionError("Denominator cannot be zero")
            self.d = value
        else:
            raise KeyError("Key must be 'n' or 'd'")
        self._simplify()

    def __repr__(self):
        if self.d == 1:
            return str(self.n)
        return f"{self.n}/{self.d}"


def evaluate_expression(expr):
    def infix_to_postfix(tokens):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operators = []

        for token in tokens:
            if token in '+-*/':
                while (operators and operators[-1] != '(' and
                       precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Remove '('
            else:
                output.append(token)

        while operators:
            output.append(operators.pop())

        return output

    tokens = expr.split()
    try:
        postfix = infix_to_postfix(tokens)
        stack = []

        for token in postfix:
            if token in '+-*/':
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
            else:
                if '/' in token:
                    stack.append(Rational(token))
                else:
                    stack.append(Rational(int(token), 1))

        if len(stack) != 1:
            raise ValueError("Invalid expression")
        return stack[0]
    except Exception as e:
        raise ValueError(f"Error evaluating expression: {str(e)}")


def main():
    with open('input01.txt', 'r') as file:
        for line in file:
            expr = line.strip()
            if not expr:
                continue
            try:
                result = evaluate_expression(expr)
                print(f"{expr} = {result} (≈{result():.6f})")
            except Exception as e:
                print(f"Error evaluating expression '{expr}': {e}")


if __name__ == "__main__":
    main()