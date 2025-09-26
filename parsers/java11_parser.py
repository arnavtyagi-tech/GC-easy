# parsers/java11_parser.py
import re
from parsers.base_parser import BaseParser

class Java11Parser(BaseParser):
    """
    Parser for Java 11+ unified GC logs
    """

    # Regex to parse unified GC log lines
    pattern = re.compile(
        r"\[(?P<timestamp>[\d\.]+)s\]\[info\]\[gc\] GC\(\d+\) Pause (?P<collector>[\w\s\(\)]+) "
        r"(?P<heap_before>\d+)M->(?P<heap_after>\d+)M\((?P<heap_total>\d+)M\) (?P<pause_ms>[\d\.]+)ms",
        re.IGNORECASE
    )

    def parse_line(self, line):
        match = self.pattern.search(line)
        if match:
            data = match.groupdict()
            return {
                "timestamp": float(data["timestamp"]),
                "collector": data["collector"],
                "heap_before": float(data["heap_before"]),
                "heap_after": float(data["heap_after"]),
                "heap_total": float(data["heap_total"]),
                "pause_ms": float(data["pause_ms"]),
                "cause": None
            }
        return None
