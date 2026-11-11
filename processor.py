"""Lab 7 - Fuzz Testing: hardened pizza_order.py (processor.py in the handout).

Fixed version of the buggy Lab 7 application from
SETAPESU26/L6_L7_24_pizza_order (Lab 7).

Hardening rules (chosen so that no text / None input can crash a function,
as the Hypothesis no-crash tests require, while every valid input still
returns exactly what the buggy version returned for it):
  * toppings_price: non-string / empty input -> 0. Unknown or empty
    toppings are ignored (they contribute 0); only known toppings are
    summed. Case and surrounding spaces are still tolerated.
  * pizza_inches: non-string / unknown / empty size -> 0 (no such size).
    Valid sizes still return S=8, M=10, L=12, case/space tolerant.
  * split_bill: the text must be exactly "total/people" with integer
    parts, total >= 0 and people > 0. Anything else (None, missing or
    extra '/', non-numeric parts, decimal parts, people <= 0, or a
    negative total) -> 0.0. Valid inputs still return round(total/people, 2).

Student: Akshat Agarwal, PES1UG24AM024
"""
TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}


def toppings_price(toppings_csv):
    """Price of a comma-separated toppings list; unknown toppings are ignored."""
    if not isinstance(toppings_csv, str):
        return 0
    total = 0
    for token in toppings_csv.split(","):
        name = token.strip().lower()
        if name in TOPPINGS:
            total += TOPPINGS[name]
    return total


def pizza_inches(size):
    """Pizza diameter in inches for S/M/L; 0 for any other input."""
    if not isinstance(size, str):
        return 0
    return SIZES.get(size.strip().upper(), 0)


def split_bill(text):
    """Per-person share of 'total/people', rounded to 2 decimals.

    Returns 0.0 for any malformed or invalid input instead of raising.
    """
    if not isinstance(text, str):
        return 0.0
    parts = text.split("/")
    if len(parts) != 2:
        return 0.0
    try:
        total = int(parts[0].strip())
        people = int(parts[1].strip())
    except (ValueError, OverflowError):
        return 0.0
    if total < 0 or people <= 0:
        return 0.0
    return round(total / people, 2)


def main():
    print("==== Running toppings_price ====")
    try:
        user_input = input("Enter toppings as CSV (e.g. cheese,olives): ")
    except (EOFError, KeyboardInterrupt):
        print("No input given.")
        return
    print("Toppings Price:", toppings_price(user_input))

    print("\n==== Running pizza_inches ====")
    try:
        user_input = input("Enter pizza size (S/M/L): ")
    except (EOFError, KeyboardInterrupt):
        print("No input given.")
        return
    print("Size in Inches:", pizza_inches(user_input))

    print("\n==== Running split_bill ====")
    try:
        user_input = input("Enter total and people (e.g. 900/3): ")
    except (EOFError, KeyboardInterrupt):
        print("No input given.")
        return
    print("Per Person:", split_bill(user_input))


if __name__ == "__main__":
    main()
