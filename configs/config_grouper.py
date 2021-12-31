import argparse
from dataclasses import dataclass

config_name = 'grouper'


@dataclass
class CommandArgs:
    path: str
    extensions: set


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='command line util for group files')
    parser.add_argument('-p', default='.', help='path to work directory')
    parser.add_argument('-e', nargs='*', default=[], help='list of grouping extensions')
    return parser.parse_args()
