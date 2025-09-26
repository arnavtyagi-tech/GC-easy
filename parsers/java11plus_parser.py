# parsers/java11plus_parser.py
import re
import pandas as pd

class Java11PlusParser:
    """
    Unified parser for Java 11, 17, and 21 GC logs
    """

    # Updated regex to correctly capture all collector names
    pattern = re.compile(
        r"\[(?P<timestamp>[\d\.]+)s\]\[info\]\[gc\]\s*GC\(\d+\)\s*Pause\s*(?P<collector>.*?)\s+"
        r"(?P<heap_before>\d+)M->(?P<heap_after>\d+)M\((?P<heap_total>\d+)M\)\s*(?P<pause_ms>[\d\.]+)ms",
        re.IGNORECASE
    )

    # Known collectors
    known_collectors = [
        "G1 Evacuation Pause",
        "G1 Humongous Allocation",
        "Shenandoah",
        "ZGC"
    ]

    def parse_line(self, line):
        match = self.pattern.search(line)
        if match:
            data = match.groupdict()
            collector_name = data["collector"].strip()

            # Determine GC type prefix
            gc_type_prefix = None
            if "Young" in collector_name:
                gc_type_prefix = "Young"
            elif "Full" in collector_name:
                gc_type_prefix = "Full"

            # Standardize collector name
            for known in self.known_collectors:
                if known in collector_name:
                    if gc_type_prefix:
                        collector_name = f"{gc_type_prefix} ({known})"
                    else:
                        collector_name = known
                    break

            return {
                "timestamp": float(data["timestamp"]),
                "collector": collector_name,
                "heap_before": float(data["heap_before"]),
                "heap_after": float(data["heap_after"]),
                "heap_total": float(data["heap_total"]),
                "pause_ms": float(data["pause_ms"]),
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
