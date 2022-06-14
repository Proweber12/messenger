import logging
import logging.handlers
from sys import stderr
import os

log = logging.getLogger('app.client')

log_format = logging.Formatter('%(asctime)-25s %(levelname)-10s %(module)-20s %(message)s')

log_file_path = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(log_file_path, 'client.log')

file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.DEBUG)

# stream_handler = logging.StreamHandler(stderr)
# stream_handler.setFormatter(log_format)
# stream_handler.setLevel(logging.DEBUG)

log.addHandler(file_handler)
# log.addHandler(stream_handler)
log.setLevel(logging.DEBUG)


if __name__ == '__main__':
    log.debug("Вывод отладочной информации")
    log.info("Вывод информационного сообщения")
    log.warning("Предупреждающее сообщение")
    log.error("Произошла ошибка")
    log.critical("Произошла критическая ошибка")