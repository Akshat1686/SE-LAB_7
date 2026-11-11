# Lab 7: Fuzz Testing for Input Validation Bugs — Pizza Order

Student: Akshat Agarwal, PES1UG24AM024
Source: SETAPESU26/L6_L7_24_pizza_order, Lab 7 (11 November 2026)
Environment verified: Python 3.12.3, pytest 9.2.0, Hypothesis 6.170.15

## File mapping (handout names vs repo names)

The handout calls the application `processor.py` and the test file
`test_processor.py`. In the repo they are `pizza_order.py` and
`test_pizza_order.py`. Both names are included here and are identical
copies, so either pair runs as-is.

| File | Description |
|---|---|
| `pizza_order.py` / `processor.py` | **Fixed** application (identical copies) |
| `test_pizza_order.py` / `test_processor.py` | **Completed** Hypothesis test file (identical copies) |
| `Lab7_Fuzz_Testing_Report.pdf` / `.docx` | Descriptive report with all tests, results, and screenshots |
| `Screenshots/` | Terminal-output screenshots for Steps 2, 4, 5, 6 |
| `logs/` | Full terminal transcripts of every run in the report |

## Results

- Step 2 (buggy): valid inputs worked (70, 8, 300.0); `cheese,xyz` crashed with `KeyError: 'xyz'`. Fuzzing found crashes in all three functions (KeyError, AttributeError, ValueError, ZeroDivisionError, plus a negative per-person share).
- Step 4 (completed tests vs buggy code): **18 failed, 3 passed** in 6.44 s. Only the valid-example tests passed.
- Step 5 (fix): unknown/empty toppings ignored, unknown size -> 0, malformed bill / people <= 0 / negative total -> 0.0, EOF in `main()` handled. Valid inputs unchanged.
- Step 6 (completed tests vs fixed code): **21 passed** in 0.90 s, and 21 passed again on a second run.

## How to run

```bash
pip install hypothesis pytest
python pizza_order.py
python -m pytest test_pizza_order.py -v
```
