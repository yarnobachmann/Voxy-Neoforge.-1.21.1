#!/usr/bin/env python3
"""
Validate that mixins declared in resource JSON files are present in the built JAR.
"""

import json
import sys
import zipfile
from pathlib import Path


def find_jar() -> Path | None:
    jars = sorted(
        jar for jar in Path("build/libs").glob("*.jar")
        if "sources" not in jar.name
    )
    return jars[0] if jars else None


def validate_config(config_path: Path, jar_entries: set[str]) -> int:
    print(f"Checking {config_path.name}...")

    with config_path.open(encoding="utf-8") as handle:
        config = json.load(handle)

    package = config.get("package")
    if not package:
        print("  ERROR: Missing package declaration")
        return 1

    errors = 0
    for array_type in ("mixins", "client", "server"):
        mixins = config.get(array_type, [])
        if not mixins:
            continue

        print(f"  Validating .{array_type}[]...")
        for mixin in mixins:
            class_path = f"{package}.{mixin}".replace(".", "/") + ".class"
            if class_path in jar_entries:
                print(f"    OK {mixin}")
            else:
                print(f"    MISSING {mixin}")
                print(f"      Expected: {class_path}")
                errors += 1

    print()
    return errors


def main() -> int:
    print("=== MIXIN CONFIGURATION VALIDATION ===\n")

    jar_path = find_jar()
    if jar_path is None:
        print("ERROR: No JAR file found in build/libs/")
        return 1

    print(f"Validating JAR: {jar_path.name}\n")
    with zipfile.ZipFile(jar_path) as jar:
        jar_entries = set(jar.namelist())

    configs = sorted(Path("src/main/resources").glob("*.mixins.json"))
    if not configs:
        print("WARNING: No mixin configuration files found")
        return 0

    errors = sum(validate_config(config, jar_entries) for config in configs)

    print("=== VALIDATION SUMMARY ===")
    print(f"JAR file: {jar_path.name}")
    print(f"JAR size: {jar_path.stat().st_size // 1024 // 1024}M")
    print()

    if errors:
        print("VALIDATION FAILED")
        print(f"Found {errors} phantom mixin reference(s)")
        return 1

    print("ALL CHECKS PASSED")
    print("All mixin references are valid and present in JAR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
