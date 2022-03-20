import os
import random
import sys

sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
))

from configs.config_grouper import CommandArgs, parse_args, config_name
from internal.pkg.base.base import Base
from logger.logger import setup_logger

logger = setup_logger('grouper')


class Grouper(Base):
    """
    Утилита для перемещения файлов в директории в соответствии с их расширением.
    Способна также работать с файлами без расширений и перемещать их в отдельную папку.
    """
    def __init__(self, command_ags: CommandArgs):
        super().__init__()
        self.new_name = config_name
        self.path = self._prepare_path(command_ags.path)
        self.extensions = self._prepare_ext(command_ags.extensions)
        self.files = self._prepare_files()
        self.without_ext = command_ags.without_ext
        self.verbose = command_ags.verbose

    def _prepare_ext(self, ext: list) -> set:
        if len(ext) == 0:
            return self.get_extensions()
        else:
            return set(ext)

    def _prepare_files(self) -> list:
        files = self.get_visible_files()
        files = list(filter(lambda x: x.split('.')[-1] in self.extensions, files))
        return files

    def get_visible_files(self) -> list:
        """
        :return: Список всех файлов в директории, кроме скрытых (корректно для Linux)
        """
        all_files = os.listdir(self.path)
        files = list(filter(lambda x: os.path.isfile(self.path + '/' + x), all_files))
        hidden_files = list(filter(lambda x: x.startswith('.'), files))
        return list(set(files) - set(hidden_files))

    def get_extensions(self) -> set:
        """
        :return: Множество уникальных расширей файлов
        """
        files = self.get_visible_files()
        endings = set()
        for x in files:
            name_splinted = x.split('.')
            if len(name_splinted) > 1:
                endings.add(name_splinted[-1])
        return endings

    def create_dirs_from_ext(self):
        """
        Создаёт в случае отсутствия директории на основе расщирений
        """
        cnt = 0
        for end in self.extensions:
            if not os.path.isdir(self.path + '/' + end):
                os.mkdir(self.path + '/' + end)
                cnt += 1
        logger.info(f'CREATED %d DIRECTORIES', cnt)

    def move_files(self):
        """
        Перемещает файлы в соответствующие директории. Файлы без расширений не обрабатывает.
        Для файлов с одинаковыми именами добавляет к копии случайное число
        """
        for filename in self.files:
            name_splinted = filename.split('.')
            end = name_splinted[-1]
            start_path = self.path + '/' + filename
            if os.path.exists(self.path + '/' + end + '/' + filename):
                ext = filename.split('.')[-1]
                name = filename[:-len(ext) - 1]
                end_path = self.path + '/' + end + '/' + name + '_' + str(int(random.random() * 10000)) + '.' + ext
            else:
                end_path = self.path + '/' + end + '/' + filename
            os.replace(start_path, end_path)
            if self.verbose:
                print(start_path, '->', end_path)
        logger.info(f'%d FILES WITH EXTs MOVED', len(self.files))

    def move_files_without_ext(self):
        """
        Перемещает файлы без расширений
        """
        if not self.without_ext:
            return
        else:
            end = 'UNK_EXT'
            if not os.path.isdir(self.path + '/' + end):
                os.mkdir(self.path + '/' + end)
            files = self.get_visible_files()
            files = list(filter(lambda x: len(x.split('.')) == 1, files))
            for filename in files:
                start_path = self.path + '/' + filename
                if os.path.exists(self.path + '/' + end + '/' + filename):
                    end_path = self.path + '/' + end + '/' + filename + '_' + str(int(random.random() * 10000))
                else:
                    end_path = self.path + '/' + end + '/' + filename
                os.replace(start_path, end_path)
                if self.verbose:
                    print(start_path, '->', end_path)
        logger.info(f'%d FILES WITHOUT EXTs MOVED', len(files))

    def run(self):
        logger.info('START')
        self.create_dirs_from_ext()
        self.move_files()
        self.move_files_without_ext()
        logger.info('END')


if __name__ == "__main__":
    try:
        args = parse_args()
        command_args = CommandArgs(args.p, args.e, args.a, args.v)
        grouper = Grouper(command_args)
        grouper.run()
    except Exception as e:
        logger.exception('\nException: {e}\n'.format(e=e))
