#!/usr/bin/python
import sys
import os
import math
from argparse import ArgumentParser

parser = ArgumentParser(description="Generate dependecy graph")
parser.add_argument('--size', '-S',
                    type=float,
                    help="Size of each object (KB)",
                    required=True)
parser.add_argument('--num', '-N',
                    type=int,
                    help="Number of objects",
                    required=True)
parser.add_argument('--out', '-O',
                    type=str,
                    help="Output file",
                    required=True)
args = parser.parse_args()

def gen():
  pass

if __name__ == "__main__":
  gen()
