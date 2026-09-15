# Project Notes

## Methodology

The study uses integer sorting as a controlled computational workload. The benchmark varies algorithm, input size, input arrangement, and controlled background CPU load, with four repetitions per unique combination.

Each execution records wall-clock runtime, CPU time, Python-level peak memory, correctness, environment metadata, and a derived performance class. The output is checked against Python's reference `sorted()` implementation.

The analysis then applies descriptive statistics, probability and conditional probability, expectation and variability, covariance/correlation, controlled comparisons, and polynomial curve fitting for runtime approximation.

## Experimental design

| Factor | Levels |
|---|---|
| Algorithm | Python TimSort, Merge Sort, Insertion Sort |
| Input size | 250, 500, 1,000, 2,000 |
| Input pattern | Random, sorted, reverse-sorted, nearly sorted |
| Background load | Low, high |
| Repetitions | 4 |

Total observations: `3 × 4 × 4 × 2 × 4 = 384`.

The overlap is intentional: changing one factor while holding the others fixed supports controlled comparisons, such as low versus high background load for the same algorithm, size, and pattern.

## Data dictionary

| Field | Description |
|---|---|
| `experiment_id` | Unique execution identifier |
| `collected_at_utc` | UTC measurement timestamp |
| `system_id` | Anonymous benchmark-system identifier |
| `task_type` | Workload family |
| `algorithm` | Sorting implementation |
| `input_size` | Number of integers sorted |
| `input_pattern` | Input arrangement |
| `background_load` | Low/high competing CPU condition |
| `repetition` | Replication index 1–4 |
| `execution_time_ms` | Wall-clock runtime in milliseconds |
| `cpu_time_ms` | CPU processing time in milliseconds |
| `peak_memory_kb` | Peak Python-level allocated memory |
| `correctness_passed` | Reference-output correctness check |
| `performance_class` | Derived runtime category |

## Reproducibility

The benchmark uses only the Python standard library:

```bash
python src/workload_dataset_generator.py
```

The analysis notebook is intended for Jupyter/Google Colab and expects the CSV dataset in its working directory.

Exact timing values are environment-dependent. Re-running the project reproduces the experimental procedure and schema, but timing values can legitimately differ across computers and runtime environments.

## Limitations

The current version is bounded to one workload family, three sorting implementations, four input sizes, four repetitions, and one benchmark environment/collection batch. Memory measurements are Python-level rather than hardware performance counters. Polynomial fits should not be treated as reliable far outside the observed input range.
