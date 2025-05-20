#!/usr/bin/env python
import sys
from audioclast import Audioclast

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("on", "off"):
        print("Usage: main.py {on|off}")
        sys.exit(1)

    audioclast = Audioclast()
    if sys.argv[1] == "on":
        audioclast.start()
    else:
        audioclast.stop()


if __name__ == "__main__":
    main()
