# cli.py
import argparse
from core.detector import detect_jvm_and_gc
from parsers.java8_parser import Java8Parser
from parsers.java11plus_parser import Java11PlusParser

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
    if jvm_version == "8":
        parser_obj = Java8Parser()
    elif jvm_version in ["11+", "17", "21"]:
        parser_obj = Java11PlusParser()
    else:
        print("Parser for this JVM version not implemented yet.")
        return

    # Step 3: Parse log
    df = parser_obj.parse_file(log_path)
    print("\nParsed GC events:")
    print(df.head())

    # Step 4: Optional CSV export
    if args.output:
        df.to_csv(args.output, index=False)
        print(f"\nParsed data saved to {args.output}")

if __name__ == "__main__":
    main()
