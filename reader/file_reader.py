import os
import logging
from entry.log_entry import LogEntry
from reader.reader import Reader
from typing import Iterator
import re

class SimpleFileReader(Reader):
    def __init__(self, filename: str, pattern: str = None, line_pattern: str = None):
        self.logger = logging.getLogger("SimpleFileReader")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exists")
        self.filename = filename
        self.pattern = pattern
        self.line_pattern = line_pattern
        self._closed = False
    
    def process_buffer(self, buffer: list) -> LogEntry:
        lines = "".join(buffer)
        self.logger.debug(f"Reading: {lines}")
        match = re.match(self.pattern, lines, re.DOTALL)
        if match:
            return LogEntry(data=match.groupdict())
        else:
            return LogEntry()


    def read(self) -> Iterator[LogEntry]:
        if (self._closed):
            raise ValueError("Reader is closed")
        buffer = []
        with open(self.filename, 'r') as _file:
            while True:
                if (self._closed):
                    self.logger.info("SimpleFileReader closed")
                    break
                line = _file.readline()
                if not line and len(buffer) > 0:
                    yield self.process_buffer(buffer)
                if not line:
                    buffer = []
                    break
                if not self.line_pattern:
                    buffer = [line]
                if self.line_pattern and re.match(self.line_pattern, line):
                    if len(buffer) > 0:
                        yield self.process_buffer(buffer)
                    buffer = [line]
                    continue
                if self.line_pattern and not re.match(self.line_pattern, line):
                    buffer.append(line)
                    continue
                yield self.process_buffer(buffer)
    
    def close(self):
        self.logger.info("Closing SimpleFileReader")
        self._closed = True