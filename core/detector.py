# core/detector.py

def detect_jvm_and_gc(log_file_path):
    """
    Detect JVM version and GC types for Java 8 and Java 11+ logs.
    Returns: {"jvm_version": str, "gc_types": list}
    """
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return {"jvm_version": "unknown", "gc_types": []}

    # --- Java 11+ unified logging detection ---
    if "[info][gc]" in content:
        jvm_version = "11+"
        gc_types = set()
        for collector in ["G1 Evacuation Pause", "G1 Humongous Allocation", "Shenandoah", "ZGC"]:
            if collector in content:
                gc_types.add(collector)
        # Fallback if no known collector found
        if not gc_types:
            gc_types.add("Unknown")
        return {"jvm_version": jvm_version, "gc_types": list(gc_types)}

    # --- Java 8 detection ---
    elif "Full GC" in content or "GC" in content:
        jvm_version = "8"
        gc_types = set()
        for collector in ["ParNew", "CMS", "G1GC", "Serial", "Parallel"]:
            if collector in content:
                gc_types.add(collector)
        if not gc_types:
            gc_types.add("Unknown")
        return {"jvm_version": jvm_version, "gc_types": list(gc_types)}

    # --- Unknown JVM ---
    return {"jvm_version": "unknown", "gc_types": []}


# Quick test
if __name__ == "__main__":
    # Test Java 8 log
    result = detect_jvm_and_gc("sample_logs/sample_gc.log")
    print("Java 8 log detection:", result)

    # Test Java 11 log
    result2 = detect_jvm_and_gc("sample_logs/sample_gc_java11.log")
    print("Java 11 log detection:", result2)
