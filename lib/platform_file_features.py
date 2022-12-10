#!/usr/bin/env python
"""
Extract features from the phred quality string.

:Authors:
    Jacob Porter <jsporter@virginia.edu>
"""

import argparse
import datetime
import math
import sys
from collections import Counter

from platform_features import get_offset, nonnegative, transform_phred_to_prob
from SeqIterator import SeqReader

HEADER = [
    "avg_length",
    "min_length",
    "max_length",
    "avg_avg_phred",
    "avg_min_phred",
    "avg_max_phred",
]


def get_file_features(fastq_input, positions=(0, 1000), debug=False):
    def get_qual_features(qual_ascii):
        seq_qual_prob = list(
            map(lambda x: transform_phred_to_prob(x, offset=offset), qual_ascii)
        )
        return {
            "avg_avg_phred": sum(seq_qual_prob) / len(seq_qual_prob),
            "avg_min_phred": min(seq_qual_prob),
            "avg_max_phred": max(seq_qual_prob),
        }

    reader = SeqReader(fastq_input, file_type="fastq")
    position = 0
    x, y = positions[0], positions[1]
    qual_array = dict(zip(HEADER[3:], [[]] * 3))
    if x and y and y < x:
        x, y = y, x
    count = 0
    offset = 0
    lengths = []
    for record in reader:
        features = []
        _, read, qual, _ = record
        position += 1
        if position > y:
            break
        if len(qual) == 0 or position < x:
            continue
        count += 1
        lengths.append(len(read))
        if not offset:
            offset = get_offset(qual)
        qual_features = get_qual_features(qual)
        for key, value in qual_features.items():
            qual_array[key].append(value)
    qual_avgs = {key: sum(qual_array[key]) / len(qual_array[key]) for key in qual_array}
    reader.close()
    return (
        sum(lengths) / len(lengths),
        min(lengths),
        max(lengths),
        qual_avgs["avg_avg_phred"],
        qual_avgs["avg_min_phred"],
        qual_avgs["avg_max_phred"],
    )


def get_directory_features(
    directory, positions=(0, 1000), header=False, output=sys.stdout, debug=False
):
    pass


def main():
    """Parse the arguments."""
    tick = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__
    )
    parser.add_argument(
        "directory",
        type=str,
        help=(
            "A directory where fastq files exist. The label must be the second field in the filename. i.e. SRR123456.pacbio.fastq"
        ),
    )
    # parser.add_argument(
    #     "--subportions",
    #     "-s",
    #     type=int,
    #     help=("The number of subportions to divide into."),
    #     default=3,
    # )
    parser.add_argument(
        "--range",
        "-r",
        nargs=2,
        type=nonnegative,
        help=(
            "The range of reads to sample.  " 'To process the whole file, use "0 0".'
        ),
        default=(1, 1000),
    )
    parser.add_argument(
        "--header",
        "-d",
        action="store_true",
        help=("Print a header at the top of the feature files."),
        default=False,
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help=("The location of the file to write the output to."),
        default="stdout",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help=("Print more info to stderr."),
        default=False,
    )
    args = parser.parse_args()
    print("Extracting features...", file=sys.stderr)
    print("Started at: {}".format(tick), file=sys.stderr)
    print(args, file=sys.stderr)
    if args.output == "stdout":
        output = sys.stdout
    else:
        output = open(args.output, "w")
    count = get_directory_features(
        args.directory,
        positions=args.range,
        header=args.header,
        output=output,
        debug=args.debug,
    )
    tock = datetime.datetime.now()
    print("There were {} records processed.".format(count), file=sys.stderr)
    print("The process took time: {}".format(tock - tick), file=sys.stderr)


if __name__ == "__main__":
    main()
