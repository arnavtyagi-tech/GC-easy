# core/detector.py
import re

def detect_jvm_and_gc(log_file_path):
    """
    Detect JVM version and GC types for Java 8, 11, 17, 21 logs.
    Returns: {"jvm_version": str, "gc_types": list}
    """
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return {"jvm_version": "unknown", "gc_types": []}

    # --- Java 11, 17, 21 unified logging detection ---
    if re.search(r"\[\d+\.\d+s\]\[info\]\[gc\]", content):
        # Detect JVM version from header if available, else default to 11+
        if "Java 17" in content:
            jvm_version = "17"
        elif "Java 21" in content:
            jvm_version = "21"
        else:
            jvm_version = "11+"

        gc_types = set()
        for collector in ["G1 Evacuation Pause", "G1 Humongous Allocation", "Shenandoah", "ZGC"]:
            if collector in content:
                gc_types.add(collector)
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
    print(detect_jvm_and_gc("sample_logs/sample_gc.log"))
    print(detect_jvm_and_gc("sample_logs/sample_gc_java11.log"))
