import os
import logging
from entry.log_entry import LogEntry
from reader.reader import Reader
from typing import Iterator

class SimpleFileReader(Reader):
    def __init__(self, filename: str):
        self.logger = logging.getLogger("SimpleFileReader")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exists")
        self.filename = filename
        self._closed = False

    def read(self) -> Iterator[LogEntry]:
        if (self._closed):
            raise ValueError("Reader is closed")
        with open(self.filename, 'r') as _file:
            for line in _file:
                if (self._closed):
                    self.logger.info("SimpleFileReader closed")
                    break
                self.logger.debug(f"Reading: {line}")
                # Crear un objeto LogEntry por cada línea leída
                log_entry = LogEntry()
                yield log_entry
    
    def close(self):
        self.logger.info("Closing SimpleFileReader")
        self._closed = True
        