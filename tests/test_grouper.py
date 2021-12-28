import os
import shutil
import unittest
import tempfile

from internal.pkg.grouper.grouper import Grouper


class TestGrouper(unittest.TestCase):

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

    def test_get_files(self):
        """
        Test to find unique extensions if folder
        """
        extensions = set(['xls', 'docx', 'pdf'])
        path = self.generate_files(extensions)

        grouper = Grouper(path)
        _, found_ext = grouper.get_extensions()
        shutil.rmtree(path)

        self.assertEqual(found_ext, extensions)

    def test_move_files(self):
        extensions = set(['xls', 'docx', 'pdf'])
        path = self.generate_files(extensions)

        grouper = Grouper(path)
        grouper.move_files()
        list_dir = os.listdir(path)
        shutil.rmtree(path)
        self.assertEqual(extensions, set(list_dir))


if __name__ == '__main__':
    unittest.main()
