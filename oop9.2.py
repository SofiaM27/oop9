import math
from typing import Union, List, Iterable


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

    def __radd__(self, other):
        return self.__add__(other)

    def __repr__(self):
        if self.d == 1:
            return str(self.n)
        return f"{self.n}/{self.d}"

    def __float__(self):
        return self.n / self.d


class RationalList:
    def __init__(self, data: Iterable[Union[Rational, int, str]] = None):
        self._data = []
        if data is not None:
            for item in data:
                self.append(item)

    def append(self, item: Union[Rational, int, str]):
        if not isinstance(item, Rational):
            item = Rational(item) if isinstance(item, str) else Rational(item)
        self._data.append(item)

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        if not isinstance(value, Rational):
            value = Rational(value) if isinstance(value, str) else Rational(value)
        self._data[index] = value

    def __len__(self):
        return len(self._data)

    def __add__(self, other):
        new_list = RationalList(self._data)
        if isinstance(other, (RationalList, list)):
            for item in other:
                new_list.append(item)
        else:
            new_list.append(other)
        return new_list

    def __radd__(self, other):
        new_list = RationalList()
        if isinstance(other, (Rational, int, str)):
            new_list.append(other)
        new_list += self
        return new_list

    def __iadd__(self, other):
        if isinstance(other, (RationalList, list)):
            for item in other:
                self.append(item)
        else:
            self.append(other)
        return self

    def __repr__(self):
        return repr(self._data)

    def sum(self):
        total = Rational(0)
        for num in self._data:
            total += num
        return total


def read_numbers_from_file(filename: str) -> RationalList:
    numbers = RationalList()
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            for token in line.split():
                try:
                    numbers.append(token)
                except ValueError as e:
                    print(f"Warning: Could not parse '{token}' in {filename}: {e}")
    return numbers


def main():
    filenames = ['input01.txt', 'input02.txt', 'input03.txt']

    for filename in filenames:
        try:
            numbers = read_numbers_from_file(filename)
            total = numbers.sum()
            print(f"File: {filename}")
            print(f"Number of elements: {len(numbers)}")
            print(f"Sum as fraction: {total}")
            print(f"Sum as decimal: {float(total):.6f}")
            print("-" * 40)
        except FileNotFoundError:
            print(f"Error: File {filename} not found")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    main()