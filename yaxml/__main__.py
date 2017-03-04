import sys
import argparse

import yaxml


def main(args):
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input', required=True)
    parser.add_argument('schema', required=True)

    opts = parser.parse_args(sys.argv[1: ])

if '__main__' == __name__:
    main(sys.argv[1: ])
