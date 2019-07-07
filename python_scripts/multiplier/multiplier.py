#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
from tensorflow import gfile # Supports both local paths and Cloud Storage (GCS) or S3

# Function doing the actual work
def do_work(input1_file, output1_file, param1):
	# print("input1_file = ",input1_file," output1_file = ",output1_file," param1 = ",param1)
	number = int(next(input1_file))
	print("number ",number)
	result = number*param1
	print("result ",result)
	_ = output1_file.write(str(result))

# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input1-path', type=str, help='Path of the local file or GCS blob containing the Input 1 data.')
parser.add_argument('--param1', type=int, default=100, help='Parameter 1.')
parser.add_argument('--output1-path', type=str, help='Path of the local file or GCS blob where the Output 1 data should be written.')
parser.add_argument('--output1-path-file', type=str, help='Path of the local file where the Output 1 URI data should be written.')
args = parser.parse_args()

gfile.MakeDirs(os.path.dirname(args.output1_path))
# Opening the input/output files and performing the actual work
with gfile.Open(args.input1_path, 'r') as input1_file, gfile.Open(args.output1_path, 'w') as output1_file:
    do_work(input1_file, output1_file, args.param1)

# Writing args.output1_path to a file so that it will be passed to downstream tasks
Path(args.output1_path_file).parent.mkdir(parents=True, exist_ok=True)
Path(args.output1_path_file).write_text(args.output1_path)

