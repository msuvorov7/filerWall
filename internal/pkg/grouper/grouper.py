import os
import random
import sys

sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
))

from configs.config_grouper import CommandArgs, parse_args, config_name
from internal.pkg.base.base import Base


class Grouper(Base):
    def __init__(self, command_ags: CommandArgs):
        super().__init__()
        self.new_name = config_name
        self.path = self._prepare_path(command_ags.path)
        self.extensions = command_ags.extensions

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
        if len(self.extensions) == 0:
            files, endings = self.get_extensions()
        else:
            files, endings = self.get_visible_files(), self.extensions

        for end in endings:
            if not os.path.isdir(self.path + '/' + end):
                os.mkdir(self.path + '/' + end)

        for filename in files:
            name_splinted = filename.split('.')
            if len(name_splinted) > 1:
                end = name_splinted[-1]
                if end not in endings:
                    continue
                start_path = self.path + '/' + filename
                if os.path.exists(self.path + '/' + end + '/' + filename):
                    ext = filename.split('.')[-1]
                    name = filename[:-len(ext) - 1]
                    end_path = self.path + '/' + end + '/' + name + '_' + str(int(random.random() * 10000)) + '.' + ext
                else:
                    end_path = self.path + '/' + end + '/' + filename
                os.replace(start_path, end_path)
                print(end_path)


if __name__ == "__main__":
    args = parse_args()
    print(args.p)
    print(set(args.e))
    command_args = CommandArgs(args.p, set(args.e))
    grouper = Grouper(command_args)
    print(grouper.new_name)
    print(grouper.name)
    grouper.move_files()
