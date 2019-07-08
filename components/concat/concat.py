#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from tensorflow import gfile # Supports both local paths and Cloud Storage (GCS) or S3

# Function doing the actual work
def do_work(input1_file, input2_file, output1_file):
	part1 = next(input1_file)
	part2 = next(input2_file)
	concat = part1+part2
	print(concat)
	_ = output1_file.write(concat)

# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input1-path', type=str, help='Path of the local file or GCS blob containing the Input 1 data.')
parser.add_argument('--input2-path', type=str, help='Path of the local file or GCS blob containing the Input 2 data.')
parser.add_argument('--output1-path', type=str, help='Path of the local file or GCS blob where the Output 1 data should be written.')
parser.add_argument('--output1-path-file', type=str, help='Path of the local file where the Output 1 URI data should be written.')
args = parser.parse_args()

gfile.MakeDirs(os.path.dirname(args.output1_path))
# Opening the input/output files and performing the actual work
with gfile.Open(args.input1_path, 'r') as input1_file, gfile.Open(args.input2_path, 'r') as input2_file, gfile.Open(args.output1_path, 'w') as output1_file:
    do_work(input1_file, input2_file, output1_file)

# Writing args.output1_path to a file so that it will be passed to downstream tasks
Path(args.output1_path_file).parent.mkdir(parents=True, exist_ok=True)
Path(args.output1_path_file).write_text(args.output1_path)

