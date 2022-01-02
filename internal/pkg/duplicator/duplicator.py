import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
))

from configs.config_duplicator import config_name, parse_args, CommandArgs
from internal.pkg.base.base import Base
from logger.logger import setup_logger

logger = setup_logger('duplicator')


def md5(filename: str) -> str:
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class Duplicator(Base):
    def __init__(self, command_ags: CommandArgs):
        super().__init__()
        self.new_name = config_name
        self.duplicate_dict = dict()
        self.path = self._prepare_path(command_ags.path)
        self.max_size = 1024
        self.recursive = command_ags.is_recursive

    def find_duplicates(self):
        self.walk_rec(self.path)

    def walk_rec(self, path: str):
        for name in os.listdir(path):
            name = os.path.join(path, name)
            if os.path.isdir(name):
                if self.recursive:
                    self.walk_rec(name)
                else:
                    continue
            else:
                hash_sum = md5(name)
                if hash_sum in self.duplicate_dict:
                    self.duplicate_dict[hash_sum].append(name)
                else:
                    self.duplicate_dict[hash_sum] = [name]

    def run(self):
        logger.info('START')
        self.find_duplicates()
        logger.info('END')


if __name__ == "__main__":
    try:
        args = parse_args()
        command_args = CommandArgs(args.p, args.r)
        duplicator = Duplicator(command_args)
        duplicator.run()
        for key, value in duplicator.duplicate_dict.items():
            print(key, value)
    except Exception as e:
        logger.exception('\nException: {e}\n'.format(e=e))
