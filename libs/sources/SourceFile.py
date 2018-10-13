
import os
from libs.logger import logger

class SourceFile(object):

    def __init__(self, path):

        if os.path.isfile(path) == False:
            logger.error("File not exist - [%s]", path)
            exit(1)

        self.path = path


    def load(self):
        return open(self.path, 'r');