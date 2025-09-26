# parsers/base_parser.py
from abc import ABC, abstractmethod
import pandas as pd

class BaseParser(ABC):
    """
    Abstract base parser for GC logs.
    """

    @abstractmethod
    def parse_line(self, line):
        """Parse a single line of GC log."""
        pass

    def parse_file(self, file_path):
        """Parse entire GC log and return DataFrame of events."""
        events = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parsed = self.parse_line(line.strip())
                if parsed:
                    events.append(parsed)
        return pd.DataFrame(events)
