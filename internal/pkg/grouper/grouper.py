from configs.config_grouper import config_name
from internal.pkg.base.base import Base


class Grouper(Base):
    def __init__(self):
        super().__init__()
        self.new_name = config_name


if __name__ == "__main__":
    grouper = Grouper()
    print(grouper.new_name)
    print(grouper.name)
