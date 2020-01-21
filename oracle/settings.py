from __future__ import absolute_import
import os, sys
import logging


logger = logging.getLogger(__name__)

try:
    sys.path.append(os.path.expanduser("~/.oracle"))
    from config import *
except Exception:
    from oracle.local_config import *

    logger.warning("Using local configuration settings.")