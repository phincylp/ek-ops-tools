import logging


def get_logger(name, file_name):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(process)d - %(message)s')
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger