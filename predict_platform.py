#!/usr/bin/env python
"""
Predicts the sequencing platform for a fastq file.
This classification task uses two classifers.

The top-level classifier predicts long read platforms.
It predicts the following classes: nanopore, pacbio, short_reads.

If this classifier predicts short_reads, then the bottom-level classifier is used.
Otherwise, the results from the top-level classifier are reported.

The bottom-level classifer predicts short read platforms.
It predicts the following classes: illumina, bgiseq, ion_torrent_or_trimmed.

:Authors:
    Jacob S. Porter <jsporter@virginia.edu>
"""
import argparse
import datetime
import os
import statistics
import sys
from typing import List, Tuple

from numpy import asarray, where
from platform_features import get_features
from platform_file_features import get_file_features
from simple_estimator import load_model, predict

BOTTOM_PATH = os.getenv("BOTTOM_MODEL")
if not BOTTOM_PATH:
    BOTTOM_PATH = "./models/bottom/GradBoost/"

TOP_PATH = os.getenv("TOP_MODEL")
if not TOP_PATH:
    TOP_PATH = "./models/top/GradBoost/"

# The default maximum number of reads for
# feature extraction in the top-level classifer.
TOP_RANGE_DEF = 3000

# The default maximum number of reads for
# feature extraction in the bottom-level classifer.
BOTTOM_RANGE_DEF = 1000


def perform_classification(
    fastq_input: List[str],
    top_path: str,
    bottom_path: str,
    top_positions: Tuple[int, int] = (1, TOP_RANGE_DEF),
    bottom_positions: Tuple[int, int] = (1, BOTTOM_RANGE_DEF),
) -> int:
    """
    Do the classification of a list of fastq files.

    Parameters
    ----------
    fastq_input: List[str]
        A list of file locations as strings.
    top_path: str
        The directory where the top-level classifer resides.
    bottom_path: str
        The directory where the bottom-level classifier resides.
    top_positions: Tuple[int, int]
        The beginning and ending reads for feature extraction for the
        top-level classifer.
    bottom_positions: Tuple[int, int]
        The beginning and ending reads for feature extraction for the
        bottom-level classifer.

    Returns
    -------
    file_count: int
        The number of files processed.

    """
    t_model, t_encoder, t_name = load_model(top_path)
    b_model, b_encoder, b_name = load_model(bottom_path)
    file_count = 0
    for fastq_file in fastq_input:
        top_prediction = predict_top(
            fastq_file, t_model, t_name, t_encoder, top_positions
        )
        if top_prediction[1] != "short_reads":
            my_printer(top_prediction)
        else:
            my_printer(
                predict_platform(
                    fastq_file, b_model, b_name, b_encoder, bottom_positions
                )
            )
        file_count += 1
    return file_count


def my_printer(row: List) -> None:
    print("\t".join(map(str, row)))


def predict_top(fastq_input, model, name, encoder, positions=(0, TOP_RANGE_DEF)):
    """
    Predict the sequencing platform from a fastq file.

    Parameters
    ----------
    fastq_input: str
        The location of the fastq file.
    model: binary
        A sklearn model.
    name: str
        The name of the model.
    encoder: binary
        A sklearn encoder object to translate numbers to string labels.
    positions: (int, int)
        The beginning and ending record positions of reads
        to be used for prediction.

    Returns
    -------
    fastq_input: str
        The location of the file that was classified.
    platform: str
        A string representing the platform.
    prob_1: float
        The probability that the prediction is correct
        as determined by the classifer.
    read_count: int
        The number of reads examined.
    """
    features, read_count = get_file_features(fastq_input, positions=positions)
    features = asarray(features).reshape(1, -1)
    responses, proba, order = predict(model, name, features, encoder)
    platform = responses[0]
    ind = where(order == platform)[0]
    prob_1 = proba[0, ind][0]
    return fastq_input, platform, prob_1, "NA", "NA", read_count


def predict_platform(
    fastq_input, model, name, encoder, positions=(1, BOTTOM_RANGE_DEF)
):
    """
    Predict the sequencing platform from a fastq file.

    Parameters
    ----------
    fastq_input: str
        The location of the fastq file.
    model: binary
        A sklearn model.
    name: str
        The name of the model.
    encoder: binary
        A sklearn encoder object to translate numbers to string labels.
    positions: (int, int)
        The beginning and ending record positions of reads
        to be used for prediction.

    Returns
    -------
    platform: str
        A string representing the platform.
    prob_1: float
        The probability that the prediction is correct.
        This is the frequency of reads predicted that
        resulted in the most common platform.
    prob_2: float
        An alternate probability of prediction correctness.
        This is the average probability of the reads as determined
        by the classifier.
    count: int
        The number of feature records created.

    """
    count, features, _, _ = get_features(
        fastq_input, label=None, positions=positions, output=None
    )
    features = asarray(features)
    responses, proba, order = predict(model, name, features, encoder)
    responses = responses.tolist()
    platform = max(set(encoder.classes_), key=responses.count)
    order_p = 0
    for i, item in enumerate(order):
        if item == platform:
            order_p = i
            break
    preds = list(filter(lambda x: x[0] == platform, zip(responses, proba)))
    prob_1 = len(preds) / len(responses)
    prob_2 = 0.0
    stdev = []
    for item in preds:
        prob_2 += item[1][order_p]
        stdev.append(item[1][order_p])
    prob_2 /= len(preds)
    if platform.startswith("ion"):
        platform = "ion_torrent_or_trimmed"
    return fastq_input, platform, prob_1, prob_2, statistics.stdev(stdev), count


def nonnegative(value):
    """Check that value is a non-negative integer."""
    my_error = argparse.ArgumentTypeError(
        "%s is not a non-negative integer value" % value
    )
    try:
        my_value = int(value)
    except ValueError as non_neg:
        raise my_error from non_neg
    if my_value < 0:
        raise my_error
    return my_value


def main():
    """Parse the arguments."""
    tick = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__
    )
    parser.add_argument(
        "fastq_input", type=str, nargs="+", help=("An input fastq file.")
    )
    parser.add_argument(
        "--top_range",
        "-r",
        type=nonnegative,
        nargs=2,
        help=(
            "The beginning and ending positions of reads to evaluate in the top classifier.  "
            "Use '0 0' to specify the whole file."
        ),
        default=[1, TOP_RANGE_DEF],
    )
    parser.add_argument(
        "--bottom_range",
        "-s",
        type=nonnegative,
        nargs=2,
        help=(
            "The beginning and ending positions of reads to evaluate in the bottom classifier.  "
            "Use '0 0' to specify the whole file."
        ),
        default=[1, BOTTOM_RANGE_DEF],
    )
    parser.add_argument(
        "--top_model",
        "-t",
        help=("The path to the Simple_Estimator model to use as the top classifier."),
        default=TOP_PATH,
    )
    parser.add_argument(
        "--bottom_model",
        "-b",
        help=(
            "The path to the Simple_Estimator model to use as the bottom classifier."
        ),
        default=BOTTOM_PATH,
    )
    args = parser.parse_args()
    print("Predicting platform...", file=sys.stderr)
    print("Started at: {}".format(tick), file=sys.stderr)
    print(args, file=sys.stderr)
    print("\t".join(("File", "Platform", "Prob", "Alt_Prob", "Stdev_Prob", "Reads")))
    perform_classification(
        args.fastq_input,
        args.top_model,
        args.bottom_model,
        args.top_range,
        args.bottom_range,
    )
    tock = datetime.datetime.now()
    print("Predict platform took time: {}".format(tock - tick), file=sys.stderr)


if __name__ == "__main__":
    main()
