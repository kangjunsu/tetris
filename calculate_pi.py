"""Calculate pi using the Gauss-Legendre algorithm."""

from decimal import Decimal, getcontext
import argparse


def calculate_pi(digits: int) -> Decimal:
    """Return pi calculated to approximately the requested decimal digits."""
    if digits < 1:
        raise ValueError("digits must be at least 1")

    getcontext().prec = digits + 5

    a = Decimal(1)
    b = Decimal(1) / Decimal(2).sqrt()
    t = Decimal("0.25")
    p = Decimal(1)

    iterations = max(3, digits.bit_length())
    for _ in range(iterations):
        next_a = (a + b) / 2
        b = (a * b).sqrt()
        t -= p * (a - next_a) ** 2
        a = next_a
        p *= 2

    pi = (a + b) ** 2 / (4 * t)
    getcontext().prec = digits
    return +pi


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate pi to N decimal digits.")
    parser.add_argument(
        "digits",
        nargs="?",
        type=int,
        default=50,
        help="number of significant digits to calculate (default: 50)",
    )
    args = parser.parse_args()

    print(calculate_pi(args.digits))


if __name__ == "__main__":
    main()
