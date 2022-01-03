import argparse
from dataclasses import dataclass

config_name = 'duplicator'


@dataclass
class CommandArgs:
    path: str
    is_recursive: bool
    is_remove: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='command line util for find duplicates')
    parser.add_argument('-p', default='.', help='path to work directory [~/Downloads]')
    parser.add_argument('-r', action='store_true', help='recursive file walker')
    parser.add_argument('--remove', action='store_true', help='remove found duplicates')
    return parser.parse_args()
