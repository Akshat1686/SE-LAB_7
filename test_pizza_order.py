"""Lab 7 - Fuzz Testing for pizza_order.py (processor.py in the handout).

Completed Hypothesis test file for all three functions:
  toppings_price, pizza_inches, split_bill

Naming: this file is test_pizza_order.py in the repo (Lab 7);
the handout calls the same file test_processor.py, and the application
pizza_order.py is the handout's processor.py. The fixed application
is hardened so that no text / None input crashes any function:
  * toppings_price: unknown or empty toppings contribute 0; None / "" -> 0
  * pizza_inches: unknown / None / "" size -> 0 (no such size)
  * split_bill: malformed text, non-numeric parts, people <= 0,
    or a negative total -> 0.0

Student: Akshat Agarwal, PES1UG24AM024
Run:  python -m pytest test_pizza_order.py -v
"""
import pytest
from hypothesis import given, settings, strategies as st

from pizza_order import TOPPINGS, toppings_price, pizza_inches, split_bill


# ---------------------------------------------------------------------------
# Starter tests, completed (Step 3): no-crash properties over text | None.
# These are the tests Hypothesis was meant to run on the buggy code:
# each one failed there with a minimised counterexample (see the report).
# ---------------------------------------------------------------------------
@settings(max_examples=100, deadline=None)
@given(st.text() | st.none())
def test_toppings_price_no_crash(s):
    result = toppings_price(s)
    assert isinstance(result, int)
    assert result >= 0


@settings(max_examples=100, deadline=None)
@given(st.text() | st.none())
def test_pizza_inches_no_crash(s):
    result = pizza_inches(s)
    assert result in (0, 8, 10, 12)


@settings(max_examples=100, deadline=None)
@given(st.text() | st.none())
def test_split_bill_no_crash(s):
    result = split_bill(s)
    assert isinstance(result, float)
    assert result >= 0


# ---------------------------------------------------------------------------
# Extra fuzzing: richer strategies that generate the shapes each function
# actually receives, so Hypothesis can reach the same bugs from other angles.
# ---------------------------------------------------------------------------
@settings(max_examples=100, deadline=None)
@given(st.lists(st.text(min_size=1, max_size=8), min_size=0, max_size=6))
def test_toppings_price_csv_lists(tokens):
    """Random comma-joined tokens: result must equal the sum of the known
    toppings in the list, ignoring every unknown / empty token."""
    csv_text = ",".join(tokens)
    result = toppings_price(csv_text)
    expected = sum(TOPPINGS[t.strip().lower()] for t in tokens
                   if t.strip().lower() in TOPPINGS)
    assert result == expected


@settings(max_examples=100, deadline=None)
@given(st.text(min_size=0, max_size=3))
def test_pizza_inches_short_text(s):
    """Short strings hit '', 'S', 'M', 'L', lower case, spaces and junk."""
    assert pizza_inches(s) in (0, 8, 10, 12)


@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=-10000, max_value=10000),
       st.integers(min_value=-10, max_value=10))
def test_split_bill_structured(total, people):
    """'total/people' built from integers: division by zero, negative
    people and negative totals must all be handled, never crash."""
    result = split_bill(f"{total}/{people}")
    assert isinstance(result, float)
    if people > 0 and total >= 0:
        assert result == round(total / people, 2)
    else:
        assert result == 0.0


@settings(max_examples=100, deadline=None)
@given(st.text())
def test_split_bill_any_text(s):
    assert isinstance(split_bill(s), float)
    assert split_bill(s) >= 0


# ---------------------------------------------------------------------------
# Deterministic tests: valid behaviour is preserved, and the exact
# edge cases Hypothesis minimised on the buggy code now have names.
# ---------------------------------------------------------------------------
def test_toppings_price_valid_examples():
    assert toppings_price("cheese,olives") == 70
    assert toppings_price("CHEESE, Olives ") == 70  # case / space tolerant
    assert toppings_price("paneer") == 50
    assert toppings_price("cheese,cheese") == 80


def test_toppings_price_invalid_returns_zero():
    assert toppings_price("") == 0
    assert toppings_price(None) == 0
    assert toppings_price("xyz") == 0
    assert toppings_price("cheese,xyz") == 40  # known part kept, unknown ignored
    assert toppings_price("cheese,,olives") == 70


def test_pizza_inches_valid_examples():
    assert pizza_inches("S") == 8
    assert pizza_inches("m") == 10
    assert pizza_inches(" L ") == 12


def test_pizza_inches_invalid_returns_zero():
    assert pizza_inches("") == 0
    assert pizza_inches("X") == 0
    assert pizza_inches(None) == 0


def test_split_bill_valid_examples():
    assert split_bill("900/3") == 300.0
    assert split_bill("1000/4") == 250.0
    assert split_bill(" 900 / 3 ") == 300.0


@pytest.mark.parametrize("bad", ["", "900", "900/0", "900/three", "900.5/3",
                                 "900/3/1", None, "900/-3", "-100/2"])
def test_split_bill_invalid_returns_zero(bad):
    assert split_bill(bad) == 0.0
