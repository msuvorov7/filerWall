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

    def test_find_duplicates(self):
        """
        Test to find duplicates of empty filies
        :return:
        """
        path = self.generate_files(['csv', 'txt'])
        duplicator = Duplicator(CommandArgs(path, False, False))
        duplicator.find_duplicates()
        shutil.rmtree(path)
        self.assertEqual(len(duplicator.duplicate_dict), 1)

    def test_remove_duplicates(self):
        """
        Test to remove duplicates of empy filies
        :return:
        """
        path = self.generate_files(['csv', 'txt'])
        duplicator = Duplicator(CommandArgs(path, False, True))
        duplicator.run()
        len_files = len(os.listdir(path))
        shutil.rmtree(path)
        self.assertEqual(len_files, 1)

    def test_find_different(self):
        """
        Test to find duplicates of two different files
        :return:
        """
        path = tempfile.mkdtemp()

        with open(path + '/file1', 'w') as f:
            f.write('max')
        with open(path + '/file2', 'w') as f:
            f.write('MAXIM')

        duplicator = Duplicator(CommandArgs(path, False, False))
        duplicator.run()
        shutil.rmtree(path)
        self.assertEqual(len(duplicator.duplicate_dict), 2)


if __name__ == '__main__':
    unittest.main()
