#!/usr/bin/env python
"""
Extract features useful for machine learning for platform prediction.

:Authors:
    Jacob Porter <jsporter@virginia.edu>
"""

import argparse
import datetime
import math
import sys
from collections import Counter

from SeqIterator.SeqIterator import SeqReader

# String of all of the quality characters.
QUAL_STR = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

# List of features.
HEADER = [
    "mean", "max", "min", "variance", "skewness", "kurtosis", "mean_diff",
    "interval_diff"
]

# Set to true to produce extra print outs to stderr
DEBUG = False


def transformPhredCharToProb(c, offset=33):
    """
    Transform a quality character into a probability.
    """
    return 10**((ord(c) - offset) / (-10.0))


def quality_features(vector, reduced=False):
    """
    Extract features from a probability vector.
    """
    # sys.stderr.write(" ".join(map(str, vector)) + "\n")
    mean = float(sum(vector)) / len(vector)
    my_max = max(vector)
    my_min = min(vector)
    variance = float(sum([math.pow(item - mean, 2)
                          for item in vector])) / len(vector)
    # Division by zero error
    if reduced:
        return [mean, my_max, my_min, variance]
    try:
        skewness = float(
            sum([
                math.pow((item - mean) / (variance + 0.0), 3)
                for item in vector
            ])) / len(vector)
    except ZeroDivisionError:
        skewness = 0
    try:
        kurt = float(
            sum([
                math.pow((item - mean) / (variance + 0.0), 4)
                for item in vector
            ])) / len(vector)
    except ZeroDivisionError:
        kurt = 9 / 5.0
    diff = []
    for i in range(1, len(vector)):
        diff.append(vector[i] - vector[i - 1])
    mean_diff = float(sum(diff)) / len(diff)
    return [
        mean, my_max, my_min, variance, skewness, kurt, mean_diff,
        vector[0] - vector[len(vector) - 1]
    ]


def get_offset(qual):
    """
    Get the quality offset from the quality character string.
    """
    qual_counter = Counter(qual)
    count_list = [qual_counter[char] for char in QUAL_STR]
    offset_33 = sum(count_list[0:25])
    offset_64 = sum(count_list[42:72])
    # offset_inb = sum(count_list[25:42])
    if offset_64 == 0 and offset_33 == 0:
        return 64
    elif offset_33 == 0:
        return 64
    else:
        return 33


def get_features(fastq_input,
                 label,
                 subportions=3,
                 header=False,
                 reduced=False):
    """
    Get the features from all sequences in the file.  Print them to stdout.
    """
    def get_qual_features(qual_ascii, reduced=False):
        seq_qual_prob = list(
            map(lambda x: transformPhredCharToProb(x, offset=offset),
                qual_ascii))
        return quality_features(seq_qual_prob, reduced=reduced)

    reader = SeqReader(fastq_input, file_type='fastq')
    count = 0
    if header:
        if reduced:
            my_header = HEADER[0:4]
        else:
            my_header = HEADER
        sys.stdout.write("\t".join(my_header))
        if subportions > 1:
            sys.stdout.write("\t")
        for i in range(subportions + subportions - 1):
            for item in my_header:
                sys.stdout.write(item + "_" + str(i + 1) + "\t")
        sys.stdout.write("label")
        sys.stdout.write("\n")
    for record in reader:
        features = []
        header, read, qual, _ = record
        if len(qual) == 0:
            continue
        count += 1
        offset = get_offset(qual)
        if DEBUG:
            print("{} Qual len:{} Offset: {}".format(count, len(qual), offset),
                  file=sys.stderr)
        features += get_qual_features(qual, reduced=reduced)
        totallength = int(len(read) / subportions)
        halflength = int(totallength / 2)
        for i in range(subportions + subportions - 1):
            if i == subportions + subportions - 2:
                finallength = len(read)
            else:
                finallength = i * halflength + totallength
            if DEBUG:
                sys.stderr.write(
                    "{} Read len:{} Offset: {} Begin: {}, End: {} {} \n".
                    format(count, len(read), offset, i * halflength,
                           finallength, qual[i * halflength:finallength]))
                sys.stderr.flush()
            features += get_qual_features(qual[i * halflength:finallength],
                                          reduced)
        features.append(label)
        print("\t".join(map(str, features)), file=sys.stdout)
    return count


def main():
    global DEBUG
    """Parse the arguments."""
    tick = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__)
    parser.add_argument("fastq_input",
                        type=str,
                        help=('The input fastq file.'))
    parser.add_argument("label",
                        type=str,
                        help=("The string to label the rows."))
    parser.add_argument("--subportions",
                        "-s",
                        type=int,
                        help=('The number of subportions to divide into.'),
                        default=3)
    parser.add_argument(
        "--header",
        "-d",
        action="store_true",
        help=("Print a header at the top of the feature files."),
        default=False)
    parser.add_argument("--reduced",
                        "-r",
                        action="store_true",
                        help=("Reduce the number of features."),
                        default=False)
    parser.add_argument("--debug",
                        action="store_true",
                        help=("Print more info to stderr."),
                        default=False)
    args = parser.parse_args()
    print("Extracting features...", file=sys.stderr)
    print("Started at: {}".format(tick), file=sys.stderr)
    print(args, file=sys.stderr)
    DEBUG = args.debug
    count = get_features(args.fastq_input, args.label, args.subportions,
                         args.header, args.reduced)
    tock = datetime.datetime.now()
    print("There were {} records processed.".format(count), file=sys.stderr)
    print("The process took time: {}".format(tock - tick), file=sys.stderr)


if __name__ == "__main__":
    main()
