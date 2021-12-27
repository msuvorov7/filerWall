import os

from configs.config_grouper import config_name
from internal.pkg.base.base import Base


class Grouper(Base):
    def __init__(self):
        super().__init__()
        self.new_name = config_name

    def get_visible_files(self, path='.'):
        all_files = os.listdir(path)
        files = list(filter(lambda x: os.path.isfile(path + '/' + x), all_files))
        hidden_files = list(filter(lambda x: x.startswith('.'), files))
        return list(set(files) - set(hidden_files))


if __name__ == "__main__":
    grouper = Grouper()
    print(grouper.new_name)
    print(grouper.name)
    print(grouper.get_visible_files())
