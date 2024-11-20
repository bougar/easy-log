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

    def process_entry(self, line: str) -> LogEntry:
        match = re.match(self.pattern, line.strip(), re.DOTALL)
        if match:
            return LogEntry(data=match.groupdict())
        else:
            return LogEntry()
    
    def process_buffer(self, buffer: list) -> LogEntry:
        lines = "".join(buffer)
        self.logger.debug(f"Reading: {lines}")
        return self.process_entry(lines)

    def read(self) -> Iterator[LogEntry]:
        if self._closed:
            raise ValueError("Reader is closed")

        with open(self.filename, 'r') as _file:
            buffer = []
            while not self._closed:
                line = _file.readline()
                if not self.line_pattern:
                    yield self.process_buffer([line])
                    continue

                if not line and buffer:
                    yield self.process_buffer(buffer)
                    break
                # Check if the line matches the pattern
                if re.match(self.line_pattern, line):
                    if buffer:
                        yield self.process_buffer(buffer)
                    buffer = [line]
                else:
                    buffer.append(line)

            if buffer:  # Process any remaining lines in buffer after breaking the loop
                yield self.process_buffer(buffer)

    def close(self):
        self.logger.info("Closing SimpleFileReader")
        self._closed = True