"""Compatibility entry point for C1/C2/C3 direct calibration runs.

The implementation lives in phase0_run_complex_direct.py and intentionally
matches the simple baseline method: one prompt, one model response, one JSON.
"""

from phase0_run_complex_direct import main


if __name__ == "__main__":
    main()
