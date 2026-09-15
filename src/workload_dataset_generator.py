"""Generate an original experimental dataset for a Unit-1 ML project.

The script benchmarks three sorting algorithms under overlapping conditions
(input size, input pattern, and background CPU load) and writes one CSV row per
real execution. It uses only the Python standard library.
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import math
import multiprocessing as mp
import os
import platform
import random
import statistics
import time
import tracemalloc
from pathlib import Path


OUTPUT_FILE = Path("workload_performance_dataset.csv")
RANDOM_SEED = 20260810
INPUT_SIZES = [250, 500, 1000, 2000]
INPUT_PATTERNS = ["random", "sorted", "reverse_sorted", "nearly_sorted"]
ALGORITHMS = ["python_timsort", "merge_sort", "insertion_sort"]
BACKGROUND_LOADS = ["low", "high"]
REPETITIONS = 4


def insertion_sort(values: list[int]) -> list[int]:
    result = values.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def merge_sort(values: list[int]) -> list[int]:
    if len(values) <= 1:
        return values.copy()
    midpoint = len(values) // 2
    left = merge_sort(values[:midpoint])
    right = merge_sort(values[midpoint:])
    merged: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def python_timsort(values: list[int]) -> list[int]:
    return sorted(values)


SORT_FUNCTIONS = {
    "python_timsort": python_timsort,
    "merge_sort": merge_sort,
    "insertion_sort": insertion_sort,
}


def make_input(size: int, pattern: str, seed: int) -> list[int]:
    rng = random.Random(seed)
    values = [rng.randint(0, size * 10) for _ in range(size)]
    if pattern == "sorted":
        return sorted(values)
    if pattern == "reverse_sorted":
        return sorted(values, reverse=True)
    if pattern == "nearly_sorted":
        values.sort()
        swaps = max(1, size // 20)
        for _ in range(swaps):
            a, b = rng.randrange(size), rng.randrange(size)
            values[a], values[b] = values[b], values[a]
    return values


def cpu_load_worker(stop_event: mp.Event) -> None:
    value = 1.000001
    while not stop_event.is_set():
        for _ in range(20_000):
            value = math.sqrt(value + 1.000001)


def percentile(sorted_values: list[float], p: float) -> float:
    position = (len(sorted_values) - 1) * p
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return sorted_values[lower]
    fraction = position - lower
    return sorted_values[lower] * (1 - fraction) + sorted_values[upper] * fraction


def system_id() -> str:
    raw = "|".join(
        [
            platform.system(),
            platform.release(),
            platform.machine(),
            platform.python_version(),
            str(os.cpu_count()),
        ]
    )
    return "SYS-" + hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


def classify_runtime(runtime_ms: float, thresholds: tuple[float, float]) -> str:
    p33, p67 = thresholds
    if runtime_ms <= p33:
        return "fast"
    if runtime_ms <= p67:
        return "moderate"
    return "slow"


def benchmark_once(algorithm: str, values: list[int]) -> tuple[float, float, float, bool]:
    expected = sorted(values)
    fn = SORT_FUNCTIONS[algorithm]
    tracemalloc.start()
    start_wall = time.perf_counter_ns()
    start_cpu = time.process_time_ns()
    result = fn(values)
    cpu_ns = time.process_time_ns() - start_cpu
    wall_ns = time.perf_counter_ns() - start_wall
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    passed = result == expected
    return wall_ns / 1e6, cpu_ns / 1e6, peak_bytes / 1024, passed


def main() -> None:
    rows: list[dict[str, object]] = []
    sid = system_id()
    experiment_number = 1
    base_rng = random.Random(RANDOM_SEED)

    load_process: mp.Process | None = None
    stop_event: mp.Event | None = None

    for load in BACKGROUND_LOADS:
        if load == "high":
            stop_event = mp.Event()
            load_process = mp.Process(target=cpu_load_worker, args=(stop_event,))
            load_process.start()
            time.sleep(0.05)

        try:
            for size in INPUT_SIZES:
                for pattern in INPUT_PATTERNS:
                    seed = base_rng.randrange(1_000_000_000)
                    values = make_input(size, pattern, seed)
                    for algorithm in ALGORITHMS:
                        for repetition in range(1, REPETITIONS + 1):
                            wall_ms, cpu_ms, memory_kb, passed = benchmark_once(algorithm, values)
                            rows.append(
                                {
                                    "experiment_id": f"EXP-{experiment_number:04d}",
                                    "collected_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                                    "system_id": sid,
                                    "task_type": "integer_sorting",
                                    "algorithm": algorithm,
                                    "input_size": size,
                                    "input_pattern": pattern,
                                    "background_load": load,
                                    "repetition": repetition,
                                    "execution_time_ms": wall_ms,
                                    "cpu_time_ms": cpu_ms,
                                    "peak_memory_kb": memory_kb,
                                    "correctness_passed": passed,
                                }
                            )
                            experiment_number += 1
        finally:
            if stop_event is not None:
                stop_event.set()
            if load_process is not None:
                load_process.join(timeout=1)
                if load_process.is_alive():
                    load_process.terminate()
                    load_process.join()
            load_process = None
            stop_event = None

    runtimes = sorted(float(row["execution_time_ms"]) for row in rows)
    p33 = percentile(runtimes, 1 / 3)
    p67 = percentile(runtimes, 2 / 3)
    thresholds = (p33, p67)
    for row in rows:
        row["performance_class"] = classify_runtime(float(row["execution_time_ms"]), thresholds)

    fieldnames = [
        "experiment_id",
        "collected_at_utc",
        "system_id",
        "task_type",
        "algorithm",
        "input_size",
        "input_pattern",
        "background_load",
        "repetition",
        "execution_time_ms",
        "cpu_time_ms",
        "peak_memory_kb",
        "correctness_passed",
        "performance_class",
    ]
    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} observations to {OUTPUT_FILE}")
    print(f"Correctness checks passed: {sum(bool(row['correctness_passed']) for row in rows)} / {len(rows)}")
    print(f"Mean runtime: {statistics.mean(runtimes):.6f} ms")


if __name__ == "__main__":
    main()
