import logging
from datetime import datetime


class Logger:
    def __init__(self):
        log_level = logging.INFO
        log_filename = f'logs/output_{datetime.now().strftime("%d-%m-%Y")}.log'

        # Configure logging
        logging.basicConfig(filename=log_filename, level=log_level,
                            format='%(levelname)s - %(message)s')

    def log(self, message, level=logging.INFO):
        # Log a message with the specified level
        logging.log(level, message)

    def log_info(self, message):
        self.log(message, logging.INFO)

    def log_warning(self, message):
        self.log(message, logging.WARNING)

    def log_error(self, message):
        self.log(message, logging.ERROR)

    def log_critical(self, message):
        self.log(message, logging.CRITICAL)
