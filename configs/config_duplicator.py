import argparse
from dataclasses import dataclass

config_name = 'duplicator'


@dataclass
class CommandArgs:
    path: str
    is_recursive: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='command line util for find duplicates')
    parser.add_argument('-p', default='.', help='path to work directory [~/Downloads]')
    parser.add_argument('-r', action='store_true', help='recursive file walker')
    return parser.parse_args()
