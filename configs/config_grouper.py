import argparse
from dataclasses import dataclass

config_name = 'grouper'


@dataclass
class CommandArgs:
    path: str
    extensions: list
    without_ext: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='command line util for group files')
    parser.add_argument('-p', default='.', help='path to work directory [~/Downloads]')
    parser.add_argument('-e', nargs='*', default=[], help='list of grouping extensions [csv/txt/...]')
    parser.add_argument('-a', action='store_true', help='group files without extension')
    return parser.parse_args()
