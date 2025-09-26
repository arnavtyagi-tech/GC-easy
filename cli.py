# cli.py
import argparse
from core.detector import detect_jvm_and_gc
import pandas as pd

# Import all parsers
from parsers.java8_parser import Java8Parser
from parsers.java11plus_parser import Java11PlusParser

# Map JVM version to parser class
PARSER_MAP = {
    "8": Java8Parser,
    "11+": Java11PlusParser,
}

def main():
    parser = argparse.ArgumentParser(description="GC Log Analyzer CLI")
    parser.add_argument("log_file", help="Path to the GC log file")
    parser.add_argument("--output", help="Optional CSV output file", default=None)
    args = parser.parse_args()

    log_path = args.log_file

    # Step 1: Detect JVM & GC
    detection = detect_jvm_and_gc(log_path)
    jvm_version = detection["jvm_version"]
    gc_types = detection["gc_types"]

    print(f"Detected JVM version: {jvm_version}")
    print(f"Detected GC types: {gc_types}")

    # Step 2: Select parser
    parser_class = PARSER_MAP.get(jvm_version)
    if not parser_class:
        print(f"Parser for JVM version '{jvm_version}' not implemented yet.")
        return

    parser_obj = parser_class()

    # Step 3: Parse full log
    df = parser_obj.parse_file(log_path)
    total_events = len(df)
    print(f"\nTotal GC events parsed: {total_events}")

    # Preview first 10 rows
    print("\nParsed GC events (showing first 10 rows):")
    print(df.head(10))

    # Step 4: Summary of GC types
    print("\nSummary of GC events by collector:")
    summary = df['collector'].value_counts()
    print(summary.to_string())

    # Step 5: Optional CSV export
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nParsed data saved to {args.output}")

if __name__ == "__main__":
    main()
