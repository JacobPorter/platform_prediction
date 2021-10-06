#!/usr/bin/env python
"""
A neural network to predict platform

:Authors:
    Jacob Porter <jsporter@virginia.edu>
"""

import argparse
import datetime
import sys

from keras.layers import Dense
from keras.models import Sequential


def train(X, y, input_dim=36, output_dim=5, epochs=25, batch_size=64):
    model = Sequential()
    model.add(Dense(12, input_dim=input_dim, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(output_dim, activation='softmax'))
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    model.fit(X, y, epochs=epochs, batch_size=batch_size)
    model.save("model.h5")


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
