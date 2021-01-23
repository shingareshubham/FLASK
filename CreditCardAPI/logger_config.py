import os
from logzero import setup_logger
import logging


def get_config():
    """"Provide configuration"""
    pass


def get_logger():
    """"Provide logger"""
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # LOg Size in MB
    max_log_file_size = 100

    my_formatter = logging.Formatter(
        '%(asctime)s - %(filename)s -  %(module)s - %(funcName)s - %(levelname)s: %(message)s'
    )

    my_logger = setup_logger(
        name="Flask_Logger",
        logfile="logs/logger.log",
        formatter=my_formatter,
        maxBytes=1000000*max_log_file_size,
        backupCount=10,
        level=logging.INFO,
        disableStderrLogger=True
    )
    return my_logger
