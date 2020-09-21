#!/usr/bin/env python
"""
Extract features useful for machine learning for platform prediction.

:Authors:
    Jacob Porter <jsporter@virginia.edu>
"""

import argparse
import datetime
import sys

from SeqIterator import SeqReader


def get_features(fasta_input, k_length):
    pass


def main():
    """Parse the arguments."""
    tick = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
    parser.add_argument("fasta_input",
                        type=str,
                        help=('The input fasta file.'))
    parser.add_argument("--k_length",
                        "-k",
                        type=int,
                        help=('The length of the kmer.'),
                        default=3)
    args = parser.parse_args()
    count = get_features(args.fasta_input, args.k_length)
    tock = datetime.datetime.now()
    print("The process took time: {}".format(tock - tick), file=sys.stderr)


if __name__ == "__main__":
    main()
