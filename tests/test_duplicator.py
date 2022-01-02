import os
import shutil
import unittest
import tempfile

from internal.pkg.duplicator.duplicator import Duplicator
from configs.config_duplicator import CommandArgs


class TestDuplicator(unittest.TestCase):
    def generate_files(self, extensions: list) -> str:
        """
        Генерируем несколько файлов для каждого расширения
        :param extensions: список расширений
        :return: временная директория с файлами
        """
        temp_path_dir = tempfile.mkdtemp()
        for cnt, ext in enumerate(extensions):
            for i in range(cnt+1):
                tempfile.NamedTemporaryFile(suffix='.' + ext, dir=temp_path_dir, delete=False)
        return temp_path_dir


if __name__ == '__main__':
    unittest.main()
