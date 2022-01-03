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
    """
    Утилита для поиска одинаковых файлов в каталоге.
    """
    def __init__(self, command_ags: CommandArgs):
        super().__init__()
        self.new_name = config_name
        self.duplicate_dict = dict()
        self.path = self._prepare_path(command_ags.path)
        self.recursive = command_ags.is_recursive
        self.remove = command_ags.is_remove

    def find_duplicates(self):
        self.walk_rec(self.path)
        logger.info(f'FOUND %d DIFFERENT HASHES', len(self.duplicate_dict))
        for key, value in self.duplicate_dict.items():
            if len(value) > 1:
                print(key, value)

    def walk_rec(self, path: str):
        """
        Рекурсивный поиск в директории. Есть остановка, если не хотим рекурсию.
        Не обрабатываем скрытые файлы
        :param path:
        :return:
        """
        for name in os.listdir(path):
            if name.split('/')[-1][0] == '.':
                continue
            name = os.path.join(path, name)
            if os.path.isdir(name):
                if self.recursive:
                    self.walk_rec(name)
                else:
                    continue
            else:
                print(name)
                hash_sum = md5(name)
                if hash_sum in self.duplicate_dict:
                    self.duplicate_dict[hash_sum].append(name)
                else:
                    self.duplicate_dict[hash_sum] = [name]

    def remove_duplicates(self):
        """
        Удаляет все найденные дубликаты, кроме первого. Первый файл берётся случайным образом
        :return:
        """
        cnt = 0
        for key, value in self.duplicate_dict.items():
            if len(value) > 1:
                for i in range(1, len(value)):
                    os.remove(value[i])
                    cnt += 1
        logger.info(f'REMOVED %d DUPLICATES', cnt)

    def run(self):
        logger.info('START')
        self.find_duplicates()
        if self.remove:
            self.remove_duplicates()
        logger.info('END')


if __name__ == "__main__":
    try:
        args = parse_args()
        command_args = CommandArgs(args.p, args.r, args.remove)
        duplicator = Duplicator(command_args)
        duplicator.run()
    except Exception as e:
        logger.exception('\nException: {e}\n'.format(e=e))
