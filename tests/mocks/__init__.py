""" file: __init__.py (xjson.tests.mocks)
"""

import logging.config
from xjson._log_config import LOG_CONFIG
logging.config.dictConfig(LOG_CONFIG)

PRINT_INTERCEPTIONS = False
