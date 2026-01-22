import json
import os
import subprocess
import sys

from ecutils.curves import _curves


def run_benchmarks():
    """
    Runs benchmarks for the core operations of the ecutils library.
    """
    curve_names = _curves.keys()
    configs = [
        {"use_projective": True, "use_lru_cache": True, "name": "Jacobian, with LRU"},
        {
            "use_projective": True,
            "use_lru_cache": False,
            "name": "Jacobian, without LRU",
        },
        {"use_projective": False, "use_lru_cache": True, "name": "Affine, with LRU"},
        {
            "use_projective": False,
            "use_lru_cache": False,
            "name": "Affine, without LRU",
        },
    ]

    all_results = {}

    for config in configs:
        all_results[config["name"]] = {}
        print(f"--- Running benchmarks for: {config['name']} ---")
        for curve_name in curve_names:
            print(f"Benchmarking curve: {curve_name}")

            env = os.environ.copy()
            if not config["use_lru_cache"]:
                env["LRU_CACHE_MAXSIZE"] = "0"
            else:
                env["LRU_CACHE_MAXSIZE"] = "1024"

            result = subprocess.run(
                [
                    sys.executable,
                    "benchmarks_helper.py",
                    curve_name,
                    str(config["use_projective"]),
                ],
                env=env,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"Error benchmarking {curve_name} with config {config['name']}:")
                print(result.stderr)
                continue

            all_results[config["name"]][curve_name] = json.loads(result.stdout)

    # Print results table
    for config_name, config_results in all_results.items():
        print(f"\n--- Results for: {config_name} ---")
        header = "| Curve | Point Addition (µs) | Point Doubling (µs) | Scalar Multiplication (ms) | Koblitz Encoding (ms) | Signature Generation (ms) | Signature Verification (ms) | Diffie-Hellman (ms) | Massey-Omura (ms) |"
        separator = "|---" * (len(header.split("|")) - 1) + "|"
        print(header)
        print(separator)

        for curve_name, timings in config_results.items():
            row = f"| {curve_name} |"
            for op in [
                "Point Addition (µs)",
                "Point Doubling (µs)",
                "Scalar Multiplication (ms)",
                "Koblitz Encoding (ms)",
                "Signature Generation (ms)",
                "Signature Verification (ms)",
                "Diffie-Hellman (ms)",
                "Massey-Omura (ms)",
            ]:
                timing = timings.get(op)
                if isinstance(timing, (int, float)):
                    row += f" {timing:.2f} |"
                else:
                    row += f" {timing} |"
            print(row)


if __name__ == "__main__":
    run_benchmarks()
