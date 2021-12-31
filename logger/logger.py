import logging
import os

from configs.config_logger import LOG_DIR_PATH


def setup_logger(name: str,
                 mode: str = 'w',
                 level=logging.INFO,
                 path_to_log: str = LOG_DIR_PATH,
                 handlers: dict = {'info': logging.INFO, 'error': logging.ERROR}
                 ) -> logging.Logger:
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    logger = logging.getLogger(name)
    logger.setLevel(level)

    for handler_name, handler_level in handlers.items():
        # handler = logging.FileHandler(os.path.join(path_to_log, f'{handler_name}.log'), mode=mode)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(handler_level)
        logger.addHandler(handler)

    return logger
