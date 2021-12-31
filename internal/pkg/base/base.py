from configs.config_base import config_name


class Base:
    """
    Базовый класс для пакетов. Здесь будут общие функции
    """
    def __init__(self):
        self.name = config_name

    def _prepare_path(self, path) -> str:
        path = path.replace('~', '/home/max')
        if path[-1] == '/':
            path = path[:-1]
        return path
