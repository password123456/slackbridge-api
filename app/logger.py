import os
import sys
import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file):
    home_path = os.path.dirname(os.path.realpath(__file__))
    log_dir = os.path.join(home_path, '..', 'logs')
    log_file = os.path.join(log_dir, log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.abspath(log_file)

    logger = logging.getLogger(name)
    logging.getLogger('werkzeug').disabled = True
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s %(name)s [%(levelname)s] | %(filename)s:%(lineno)d | %(funcName)s() -> %(message)s',
        '%Y-%m-%d %H:%M:%S'
    )

    # Set up a rotating file handler (log rotation)
    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
