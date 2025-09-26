# core/detector.py

def detect_jvm_and_gc(log_file_path):
    """
    Minimal detector: works with any Java 8 sample log.
    Returns {"jvm_version": str, "gc_types": list}
    """
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return {"jvm_version": "unknown", "gc_types": []}

    # Check for Full GC or GC in any line
    if "Full GC" in content or "GC" in content:
        jvm_version = "8"

        gc_types = set()
        for collector in ["ParNew", "CMS", "G1GC", "Serial", "Parallel"]:
            if collector in content:
                gc_types.add(collector)

        # If no known collector found, just set Unknown
        if not gc_types:
            gc_types.add("Unknown")

        return {"jvm_version": jvm_version, "gc_types": list(gc_types)}

    return {"jvm_version": "unknown", "gc_types": []}


# Quick test
if __name__ == "__main__":
    result = detect_jvm_and_gc("sample_logs/sample_gc.log")
    print(result)
