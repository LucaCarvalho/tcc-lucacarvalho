import logging

def get_logger(level=logging.INFO) -> logging.Logger:
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)
    return logging.getLogger()
