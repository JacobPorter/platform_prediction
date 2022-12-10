#!/usr/bin/env python
"""
Only emit rows from a file that do NOT have the search string.

:Authors:
    Jacob Porter <jsporter@virginia.edu>
"""
import os
import sys

# Check that the correct number of command line arguments were provided
if len(sys.argv) != 3:
    print("Usage: python3 program.py input_file.txt search_string")
    sys.exit(1)

# Read the input file name and the string to search for from the command line
input_file_name = sys.argv[1]
search_string = sys.argv[2]

# Check if the input file exists
if not os.path.exists(input_file_name):
    print("Error: Input file does not exist")
    sys.exit(1)

# Open the input file and read the lines
# Iterate over the lines and print those that do not contain the search string
with open(input_file_name, "r") as input_file:
    for line in input_file:
        if search_string not in line:
            sys.stdout.write(line)