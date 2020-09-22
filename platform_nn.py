#!/usr/bin/env python
"""
A neural network to predict platform

:Authors:
    Jacob Porter <jsporter@virginia.edu>
"""

import argparse
import datetime
import sys


def train():
    pass


def predict():
    pass


def main():
    """Parse the arguments."""
    tick = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__)
    parser.add_argument("fastq_input",
                        type=str,
                        help=('The input fastq file.'))
    args = parser.parse_args()
    print("Extracting features...", file=sys.stderr)
    print(args, file=sys.stderr)

    tock = datetime.datetime.now()
    print("The process took time: {}".format(tock - tick), file=sys.stderr)


if __name__ == "__main__":
    main()
