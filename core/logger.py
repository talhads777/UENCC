import logging, sys
def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh = logging.FileHandler('uencc.log'); fh.setFormatter(formatter); logger.addHandler(fh)
        ch = logging.StreamHandler(sys.stdout); ch.setFormatter(formatter); logger.addHandler(ch)
    return logger
