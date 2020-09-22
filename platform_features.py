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

QUAL_STR = '!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'


def transformPhredCharToProb(c, offset=33):
    return 10**((ord(c) - offset) / (-10.0))


def quality_features(vector):
    mean = float(sum(vector)) / len(vector)
    my_max = max(vector)
    my_min = min(vector)
    variance = float(sum([math.pow(item - mean, 2)
                          for item in vector])) / len(vector)
    # Division by zero error
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
    return [mean, my_max, my_min, variance, skewness, kurt, mean_diff]


def get_offset(qual):
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


def get_features(fastq_input, k_length):
    reader = SeqReader(fastq_input, file_type='fastq')
    for record in reader:
        header, read, mid, qual = record
        len_read = len(read)
        offset = get_offset(qual)
        seq_qual_prob = map(
            lambda x: transformPhredCharToProb(x, offset=offset), qual)
        first_qual_features = quality_features(seq_qual_prob)


def main():
    """Parse the arguments."""
    tick = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=__doc__)
    parser.add_argument("fastq_input",
                        type=str,
                        help=('The input fasta file.'))
    parser.add_argument("--k_length",
                        "-k",
                        type=int,
                        help=('The length of the kmer.'),
                        default=3)
    args = parser.parse_args()
    count = get_features(args.fastq_input, args.k_length)
    tock = datetime.datetime.now()
    print("The process took time: {}".format(tock - tick), file=sys.stderr)


if __name__ == "__main__":
    main()
