# parsers/java8_parser.py
import re
from parsers.base_parser import BaseParser

class Java8Parser(BaseParser):
    """
    Parser for Java 8 GC logs (ParNew, CMS, G1GC, Serial, Parallel)
    """

    # Flexible regex for minor GCs
    gc_pattern = re.compile(
        r"\[GC \[(?P<collector>\w+): (?P<heap_before>\d+)K->(?P<heap_after>\d+)K\((?P<heap_total>\d+)K\), (?P<pause_sec>\d+\.\d+) secs\]\s(?P<total_before>\d+)K->(?P<total_after>\d+)K\((?P<total_heap>\d+)K\), (?P<total_pause_sec>\d+\.\d+) secs\]",
        re.IGNORECASE
    )

    # Flexible regex for Full GCs
    full_gc_pattern = re.compile(
        r"\[Full GC (?P<heap_before>\d+)K->(?P<heap_after>\d+)K\((?P<heap_total>\d+)K\), (?P<pause_sec>\d+\.\d+) secs\]",
        re.IGNORECASE
    )

    def parse_line(self, line):
        # Try minor GC first
        match = self.gc_pattern.search(line)
        if match:
            data = match.groupdict()
            collector = data["collector"]
            return {
                "timestamp": None,
                "collector": collector,
                "heap_before": int(data["heap_before"]) / 1024,
                "heap_after": int(data["heap_after"]) / 1024,
                "heap_total": int(data["heap_total"]) / 1024,
                "pause_ms": float(data["pause_sec"]) * 1000,
                "cause": None
            }

        # Try Full GC
        match = self.full_gc_pattern.search(line)
        if match:
            data = match.groupdict()
            return {
                "timestamp": None,
                "collector": "Full",
                "heap_before": int(data["heap_before"]) / 1024,
                "heap_after": int(data["heap_after"]) / 1024,
                "heap_total": int(data["heap_total"]) / 1024,
                "pause_ms": float(data["pause_sec"]) * 1000,
                "cause": None
            }

        return None
