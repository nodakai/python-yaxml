import sys
import argparse

import yaxml


parser = argparse.ArgumentParser(description='')
parser.add_argument('input', required=True)
parser.add_argument('schema', required=True)

opts = parser.parse_args(sys.argv[1: ])
