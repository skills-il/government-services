#!/usr/bin/env python3
"""This version does not calculate a grant amount.

Versions 1.4.0 to 1.6.0 usually showed twice the correct amount.
"""

import argparse
import sys

NOTICE = (
    "This tool no longer prints a grant amount. Versions 1.4.0 to 1.6.0 usually "
    "showed twice the correct amount, so do not rely on them.\n"
    "Use the simulator in the Tax Authority's online claim system and its official "
    "claim pages.\n"
    "If you already filed, check with the Tax Authority before changing or "
    "cancelling anything."
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_known_args()
    print(NOTICE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
