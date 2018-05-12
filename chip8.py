#!/usr/bin/env python3

import sys

from run_conf import RunConfiguration


def main():
    return RunConfiguration.from_args().run()


if __name__ == "__main__":
    sys.exit(main())
