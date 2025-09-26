# parsers/java8_parser.py
import re
import pandas as pd

class Java8Parser:
    """
    Parser for Java 8 GC logs
    """

    minor_gc_pattern = re.compile(
        r"\[GC \[(?P<collector>\w+): (?P<heap_before>\d+)K->(?P<heap_after>\d+)K\((?P<heap_total>\d+)K\), (?P<pause_sec>[\d\.]+) secs\].*",
        re.IGNORECASE
    )

    full_gc_pattern = re.compile(
        r"\[Full GC (?P<heap_before>\d+)K->(?P<heap_after>\d+)K\((?P<heap_total>\d+)K\), (?P<pause_sec>[\d\.]+) secs\].*",
        re.IGNORECASE
    )

    def parse_line(self, line):
        # Minor GC
        match = self.minor_gc_pattern.search(line)
        if match:
            data = match.groupdict()
            return {
                "timestamp": None,
                "collector": data["collector"],
                "heap_before": int(data["heap_before"])/1024,
                "heap_after": int(data["heap_after"])/1024,
                "heap_total": int(data["heap_total"])/1024,
                "pause_ms": float(data["pause_sec"])*1000,
                "cause": None
            }

        # Full GC
        match = self.full_gc_pattern.search(line)
        if match:
            data = match.groupdict()
            return {
                "timestamp": None,
                "collector": "Full",
                "heap_before": int(data["heap_before"])/1024,
                "heap_after": int(data["heap_after"])/1024,
                "heap_total": int(data["heap_total"])/1024,
                "pause_ms": float(data["pause_sec"])*1000,
                "cause": None
            }
        return None

    def parse_file(self, file_path):
        events = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                result = self.parse_line(line)
                if result:
                    events.append(result)
        return pd.DataFrame(events)
