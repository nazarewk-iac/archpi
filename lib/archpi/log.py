import logging
import os
import sys


def setup():
    logging.basicConfig(stream=sys.stderr, level=os.environ.get('LOG_LEVEL', 'INFO'))
