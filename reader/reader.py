from abc import ABC, abstractmethod
from typing import Iterator
from entry.log_entry import LogEntry

class Reader(ABC):
    @abstractmethod
    def read(self) -> Iterator[LogEntry]:
        pass