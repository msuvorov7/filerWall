import os

from configs.config_grouper import config_name
from internal.pkg.base.base import Base


class Grouper(Base):
    def __init__(self, path):
        super().__init__()
        self.new_name = config_name
        self.path = self._prepare_path(path)

    def get_visible_files(self) -> list:
        all_files = os.listdir(self.path)
        files = list(filter(lambda x: os.path.isfile(self.path + '/' + x), all_files))
        hidden_files = list(filter(lambda x: x.startswith('.'), files))
        return list(set(files) - set(hidden_files))

    def get_extensions(self) -> (list, set):
        files = self.get_visible_files()
        endings = set()
        for x in files:
            name_splinted = x.split('.')
            if len(name_splinted) > 1:
                endings.add(name_splinted[-1])
        return files, endings

    def move_files(self):
        files, endings = self.get_extensions()
        for end in endings:
            if not os.path.isdir(self.path + '/' + end):
                os.mkdir(self.path + '/' + end)

        for filename in files:
            name_splinted = filename.split('.')
            if len(name_splinted) > 1:
                end = name_splinted[-1]
                os.replace(self.path + '/' + filename, self.path + '/' + end + '/' + filename)
                print(end + '/' + filename)


if __name__ == "__main__":
    grouper = Grouper('~/Downloads/ML-main')
    print(grouper.new_name)
    print(grouper.name)
    grouper.move_files()
