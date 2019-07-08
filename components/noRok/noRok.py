#!/usr/bin/env python3
import argparse
import os
from urllib.request import urlopen

# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input1-path', type=str, help='Path of the local file or GCS blob containing the Input 1 data.')
args = parser.parse_args()

data = urlopen(args.input1_path) # it's a file like object and works just like a file
for line in data: # files are iterable
    print(line)