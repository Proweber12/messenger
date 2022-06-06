import logging
import sys
import inspect

import logs.client_log_config
import logs.server_log_config

if sys.argv[0].find('client.py') == -1:
    LOGGER = logging.getLogger('app.server')
else:
    LOGGER = logging.getLogger('app.client')


def log(log_func):
    def wrapper(*args, **kwargs):
        func = log_func(*args, **kwargs)
        LOGGER.info(f'Функция {log_func.__name__} была вызвана с параметрами {args}, {kwargs} | '
                    f'Из модуля {log_func.__module__} | '
                    f'Эта функция была вызвана в функции {inspect.stack()[1][3]}', stacklevel=2)
        return func
    return wrapper
