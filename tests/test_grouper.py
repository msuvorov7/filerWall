import os
import shutil
import unittest
import tempfile

from internal.pkg.grouper.grouper import Grouper
from configs.config_grouper import CommandArgs


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
        command_args = CommandArgs(path, [])

        grouper = Grouper(command_args)
        found_ext = grouper.get_extensions()
        shutil.rmtree(path)

        self.assertEqual(found_ext, extensions)

    def test_move_files(self):
        extensions = set(['xls', 'docx', 'pdf'])
        path = self.generate_files(extensions)
        command_args = CommandArgs(path, [])

        grouper = Grouper(command_args)
        grouper.run()
        list_dir = os.listdir(path)
        shutil.rmtree(path)
        self.assertEqual(extensions, set(list_dir))

    def test_files_with_equal_names(self):
        temp_path_dir = tempfile.mkdtemp()
        os.mkdir(temp_path_dir + '/' + 'csv')
        file1 = open(temp_path_dir + '/' + 'csv' + '/' + 'file.csv', 'w')
        file1.close()

        file2 = open(temp_path_dir + '/' + 'file.csv', 'w')
        file2.close()

        command_args = CommandArgs(temp_path_dir, [])
        grouper = Grouper(command_args)
        grouper.run()
        len_files = len(os.listdir(temp_path_dir + '/' + 'csv'))
        shutil.rmtree(temp_path_dir)
        self.assertEqual(len_files, 2)

    def test_move_csv_files(self):
        temp_path_dir = tempfile.mkdtemp()
        file1 = open(temp_path_dir + '/' + 'file1.csv', 'w')
        file1.close()

        file2 = open(temp_path_dir + '/' + 'file2.txt', 'w')
        file2.close()

        command_args = CommandArgs(temp_path_dir, ['csv'])
        grouper = Grouper(command_args)
        grouper.run()

        len_csv_files = len(os.listdir(temp_path_dir + '/csv'))
        len_files = len(os.listdir(temp_path_dir))

        txt_dir = os.path.exists(temp_path_dir + '/txt')

        shutil.rmtree(temp_path_dir)
        self.assertEqual(len_files, 2)
        self.assertEqual(txt_dir, False)
        self.assertEqual(len_csv_files, 1)


if __name__ == '__main__':
    unittest.main()
