# parsers/java8_parser.py
import re
import pandas as pd

class Java8Parser:
    def __init__(self):
        # Compile regex patterns for different GC types
        self.patterns = {
            "ParNew": re.compile(r"(\d+\.\d+): \[GC \(.*?\) \[ParNew: (\d+)K->(\d+)K\((\d+)K\)\], (\d+\.\d+) secs\]"),
            "CMS_initial": re.compile(r"(\d+\.\d+): \[GC \(CMS Initial Mark\).*? (\d+)K\((\d+)K\)\], (\d+\.\d+) secs"),
            "CMS_final": re.compile(r"(\d+\.\d+): \[GC \(CMS Final Remark\).*? (\d+)K\((\d+)K\)\], (\d+\.\d+) secs"),
            "Full_GC": re.compile(r"(\d+\.\d+): \[Full GC.*? (\d+)K->(\d+)K\((\d+)K\)\], (\d+\.\d+) secs"),
            "Serial": re.compile(r"(\d+\.\d+): \[GC \(.*?\) (\d+)K->(\d+)K\((\d+)K\), (\d+\.\d+) secs\]"),
            "Parallel": re.compile(r"(\d+\.\d+): \[GC \(.*?\) \[PSYoungGen: (\d+)K->(\d+)K\((\d+)K\)\] (\d+)K->(\d+)K\((\d+)K\), (\d+\.\d+) secs\]"),
            "G1GC": re.compile(r"(\d+\.\d+): \[GC pause \((.*?)\).*? (\d+)M->(\d+)M\((\d+)M\), (\d+\.\d+) secs\]"),
            "ZGC": re.compile(r"(\d+\.\d+): \[(Pause Mark Start|Concurrent Mark|Pause Relocate Start|Pause Relocate End) (\d+\.?\d*)ms\]"),
            "Shenandoah": re.compile(r"(\d+\.\d+): \[(Pause Init Mark|Concurrent Mark|Pause Final Evac|Concurrent Cleanup) (\d+\.?\d*)ms\]"),
        }

    def parse_file(self, file_path):
        rows = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parsed = self.parse_line(line)
                if parsed:
                    rows.append(parsed)
        df = pd.DataFrame(rows)
        return df

    def parse_line(self, line):
        for key, pattern in self.patterns.items():
            match = pattern.search(line)
            if match:
                if key == "ParNew":
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": "ParNew",
                        "heap_before": int(match.group(2)) / 1024,
                        "heap_after": int(match.group(3)) / 1024,
                        "heap_total": int(match.group(4)) / 1024,
                        "pause_ms": float(match.group(5)) * 1000,
                        "cause": self.extract_cause(line)
                    }
                elif key.startswith("CMS"):
                    collector_type = "CMS (initial)" if key == "CMS_initial" else "CMS (remark)"
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": collector_type,
                        "heap_before": int(match.group(2)) / 1024,
                        "heap_after": int(match.group(3)) / 1024,
                        "heap_total": int(match.group(3)) / 1024,
                        "pause_ms": float(match.group(4)) * 1000,
                        "cause": "CMS Initial Mark" if key == "CMS_initial" else "CMS Final Remark"
                    }
                elif key == "Full_GC":
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": "Full GC",
                        "heap_before": int(match.group(2)) / 1024,
                        "heap_after": int(match.group(3)) / 1024,
                        "heap_total": int(match.group(4)) / 1024,
                        "pause_ms": float(match.group(5)) * 1000,
                        "cause": self.extract_cause(line)
                    }
                elif key == "Serial":
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": "Serial GC",
                        "heap_before": int(match.group(2)) / 1024,
                        "heap_after": int(match.group(3)) / 1024,
                        "heap_total": int(match.group(4)) / 1024,
                        "pause_ms": float(match.group(5)) * 1000,
                        "cause": self.extract_cause(line)
                    }
                elif key == "Parallel":
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": "Parallel GC",
                        "heap_before": int(match.group(5)) / 1024,
                        "heap_after": int(match.group(6)) / 1024,
                        "heap_total": int(match.group(7)) / 1024,
                        "pause_ms": float(match.group(8)) * 1000,
                        "cause": self.extract_cause(line)
                    }
                elif key == "G1GC":
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": match.group(2),
                        "heap_before": int(match.group(3)),
                        "heap_after": int(match.group(4)),
                        "heap_total": int(match.group(5)),
                        "pause_ms": float(match.group(6)) * 1000,
                        "cause": None
                    }
                elif key in ["ZGC", "Shenandoah"]:
                    return {
                        "timestamp": float(match.group(1)),
                        "collector": match.group(2),
                        "heap_before": None,
                        "heap_after": None,
                        "heap_total": None,
                        "pause_ms": float(match.group(3)),
                        "cause": None
                    }
        return None

    def extract_cause(self, line):
        # Extract the reason for GC from the line
        cause_match = re.search(r"\((.*?)\)", line)
        if cause_match:
            return cause_match.group(1)
        return None
