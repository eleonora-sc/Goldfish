import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir='logs') -> None:
        # Create log directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create a filename base on the current date and time
        filename = os.path.join(log_dir,f"log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

        # Setup the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create a file handler and set the level to debug
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)

        # Create the fomatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log(self,message,level="debug"):
        """will append to the current log file

        Args:
            message (_type_): _description_
            level (str, optional): _description_. Defaults to "debug".
        """
        if level == "debug":
            self.logger.debug(message)
        elif level == "info":
            self.logger.info(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "critical":
            self.logger.critical(message)
        else:
            self.logger.debug(message)