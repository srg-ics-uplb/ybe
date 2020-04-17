__author__ = 'Robbert Harms'
__date__ = '2020-07-07'
__email__ = 'robbert@xkls.nl'
__license__ = "GPL v3"
__maintainer__ = "Robbert Harms"

import logging.config as logging_config

from ybe.configuration import get_logging_configuration_dict

try:
    logging_config.dictConfig(get_logging_configuration_dict())
except ValueError as e:
    print('Logging disabled, error message: {}'.format(e))

from ybe.__version__ import VERSION, VERSION_STATUS, __version__
from ybe.lib.utils import load, loads, dump, dumps