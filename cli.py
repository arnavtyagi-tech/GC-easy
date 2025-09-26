# cli.py
import argparse
from core.detector import detect_jvm_and_gc
from parsers.java8_parser import Java8Parser
from parsers.java11_parser import Java11Parser

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

    # Step 2: Select parser based on JVM version
    if jvm_version == "8":
        parser_obj = Java8Parser()
    elif jvm_version == "11+":
        parser_obj = Java11Parser()
    else:
        print("Parser for this JVM version not implemented yet.")
        return

    # Step 3: Parse log file
    df = parser_obj.parse_file(log_path)
    if df.empty:
        print("No GC events found in the log.")
        return

    print("\nParsed GC events:")
    print(df.head(10))  # Show first 10 rows

    # Step 4: Optional CSV export
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nParsed data saved to {args.output}")

if __name__ == "__main__":
    main()
