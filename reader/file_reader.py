import os
import logging
from entry.log_entry import LogEntry
from reader.reader import Reader
from typing import Iterator
import time
import re
from typing import Iterator, List, Optional

class SimpleFileReader(Reader):
    def __init__(self, filename: str, pattern: Optional[str] = None, line_pattern: Optional[str] = None):
        self.logger = logging.getLogger("SimpleFileReader")
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File {filename} does not exist")
        self.filename = filename
        self.pattern = pattern
        self.line_pattern = line_pattern
        self._closed = False

    def process_entry(self, line: str) -> LogEntry:
        match = re.match(self.pattern, line.strip(), re.DOTALL)
        if match:
            return LogEntry(data=match.groupdict())
        return LogEntry()

    def process_buffer(self, buffer: List[str]) -> LogEntry:
        lines = "".join(buffer)
        self.logger.debug(f"Reading: {lines}")
        return self.process_entry(lines)

    def _yield_buffer(self, buffer: List[str]):
        if buffer:
            yield self.process_buffer(buffer)
            buffer.clear()

    def read(self) -> Iterator[LogEntry]:
        if self._closed:
            raise ValueError("Reader is closed")

        with open(self.filename, 'r') as _file:
            buffer = []

            while not self._closed:
                line = _file.readline()

                # Handle end-of-file scenario
                if not line:
                    yield from self._yield_buffer(buffer)
                    time.sleep(0.5)
                    continue

                # If no line pattern, process each line individually
                if not self.line_pattern:
                    yield self.process_buffer([line])
                    continue

                # If line matches the pattern, process current buffer and start a new one
                if re.match(self.line_pattern, line):
                    yield from self._yield_buffer(buffer)
                buffer.append(line)

            # Process any remaining lines in the buffer
            yield from self._yield_buffer(buffer)

    def close(self):
        self.logger.info("Closing SimpleFileReader")
        self._closed = True
