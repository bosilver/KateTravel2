

import logging

# Prepare Log
def get_logger(name):
    log = logging.getLogger(name)

    log.setLevel(logging.DEBUG)

    formatter_verbose = logging.Formatter('%(asctime)s %(levelname)8s %(message)s')
    formatter_short = logging.Formatter('[%(levelname)8s] %(message)s')
    fh = logging.FileHandler('/tmp/KateTravel.log')
    fh.setFormatter(formatter_verbose)
    log.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter_short)
    log.addHandler(sh)

    return log
