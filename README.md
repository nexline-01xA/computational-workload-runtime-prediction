# Machine Learning-Based Characterisation and Runtime Prediction of Computational Workloads

**Experimental ML project for computational workload characterisation, statistical analysis, and runtime prediction.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white)](https://jupyter.org/)
[![Dataset](https://img.shields.io/badge/Dataset-384%20runs-111827)](#dataset)
[![Validation](https://img.shields.io/badge/Validation-384%2F384-166534)](#data-quality-and-validation)
[![License](https://img.shields.io/badge/License-MIT-0F172A)](LICENSE)

> A controlled benchmarking study that turns real sorting executions into an original dataset, analyses workload effects using ML Unit 1 statistics, and explores polynomial runtime prediction.

## Overview

Runtime depends on more than input size. Algorithm choice, input arrangement, background CPU activity, and measurement variability can all influence observed performance.

This project uses sorting as a controlled workload. The included Python benchmark **generates the dataset through execution**, validates the output of every run, and records runtime/resource measurements. The resulting data is analysed with statistics and probability concepts from ML Unit 1, followed by polynomial curve fitting for runtime modelling.

## Research questions

| ID | Question |
|---|---|
| RQ1 | How does runtime scale with input size? |
| RQ2 | How strongly does algorithm choice affect observed runtime? |
| RQ3 | Does input arrangement change algorithm performance? |
| RQ4 | Does controlled background CPU load affect runtime? |
| RQ5 | How variable are repeated measurements of the same condition? |
| RQ6 | How well can a simple polynomial approximate runtime within the observed range? |

## Experimental design

| Factor | Levels |
|---|---|
| Algorithms | Python TimSort, Merge Sort, Insertion Sort |
| Input sizes | 250, 500, 1,000, 2,000 |
| Input patterns | Random, sorted, reverse-sorted, nearly sorted |
| Background CPU load | Low, high |
| Repetitions | 4 |

Total:

```text
3 × 4 × 4 × 2 × 4 = 384 experimental runs
```

The conditions deliberately overlap, allowing controlled comparisons where one factor changes while the others are held constant.

## Experimental pipeline

```text
Experimental Design
        ↓
Workload Generation
        ↓
Sorting Execution
        ↓
Runtime / CPU / Memory Measurement
        ↓
Correctness Validation
        ↓
CSV Dataset
        ↓
Statistical Analysis
        ↓
Polynomial Runtime Modelling
        ↓
Interpretation + Limitations
```

## Dataset

`data/workload_performance_dataset.csv` contains **384 observations across 14 fields**.

Key fields include algorithm, input size, input pattern, background load, repetition, execution time, CPU time, peak Python memory, correctness status, and performance class.

### Dataset snapshot

- 384 observations
- 14 fields
- 384 / 384 correctness checks passed
- No missing values in the checked-in dataset
- 96 unique experimental conditions × 4 repetitions

Descriptive aggregates from the checked-in dataset:

| Metric | Value |
|---|---:|
| Mean runtime | 218.985851 ms |
| Median runtime | 3.095790 ms |
| Mean Python TimSort runtime | 0.128741 ms |
| Mean Merge Sort runtime | 16.015539 ms |
| Mean Insertion Sort runtime | 640.813272 ms |
| Mean low-load runtime | 153.256332 ms |
| Mean high-load runtime | 284.715369 ms |

See [`results/dataset_summary.md`](results/dataset_summary.md) for the same summary.

## Data quality and validation

The benchmark validates each sorting result against Python's `sorted()` reference output. The checked-in dataset contains **384 successful correctness checks out of 384 runs**.

The analysis notebook also checks dataset structure, missing values, duplicate observations, experiment identifiers, timing validity, and expected repetition counts.

## Analysis

The executed notebook in [`notebooks/ML_Unit1_Workload_Analysis.ipynb`](notebooks/ML_Unit1_Workload_Analysis.ipynb) covers:

1. Problem formulation and experimental design
2. Dataset loading and schema inspection
3. Data-quality validation
4. Descriptive statistics
5. Probability and conditional probability
6. Expectation and variability
7. Covariance and correlation
8. Overlapping-condition analysis
9. Runtime distributions and algorithm comparisons
10. Input-size scaling
11. Polynomial curve fitting
12. Actual-versus-predicted runtime analysis
13. Limitations and scaling strategy

The project distinguishes **measured observations** from **modelled values**. Polynomial fits are treated as approximations over the observed range rather than universal extrapolators.

## Visual evidence

The repository keeps ten figures generated from the same dataset:

- `01_runtime_distribution.png` — overall runtime distribution
- `02_boxplot_by_algorithm.png` — runtime spread by algorithm
- `03_runtime_vs_size.png` — scaling with input size
- `04_runtime_by_pattern.png` — input-pattern effect
- `05_load_comparison.png` — low vs high background load
- `06_correlation_heatmap.png` — numerical associations
- `07_repetition_variability.png` — repeated-run variability
- `08_interaction_pattern_algorithm.png` — algorithm × pattern interaction
- `09_polynomial_fits.png` — fitted runtime curves
- `10_actual_vs_predicted.png` — observed vs modelled runtime

Browse [`results/figures/`](results/figures/).

## Reproducibility

The benchmark source is [`src/workload_dataset_generator.py`](src/workload_dataset_generator.py).

```bash
python src/workload_dataset_generator.py
```

The script uses only the Python standard library. The analysis notebook is intended for Jupyter/Google Colab.

Absolute runtime values are environment-dependent; reproducing the **method and dataset structure** matters more than expecting identical wall-clock timings on another machine.

## Repository structure

```text
computational-workload-runtime-prediction/
├── data/
│   ├── workload_performance_dataset.csv
│   └── README.md
├── src/
│   ├── workload_dataset_generator.py
│   └── README.md
├── notebooks/
│   └── ML_Unit1_Workload_Analysis.ipynb
├── results/
│   ├── dataset_summary.md
│   └── figures/
├── report/
│   └── ML_Workload_Project_Report.pdf
├── presentation/
│   └── ML_Workload_Project_Presentation.pptx
├── docs/
│   ├── methodology.md
│   ├── experimental_design.md
│   ├── data_dictionary.md
│   ├── reproducibility.md
│   └── limitations.md
├── .github/workflows/validate.yml
├── CITATION.cff
├── LICENSE
├── requirements.txt
└── README.md
```

## Academic scope

This is an **academic/engineering project repository** organised around a research-style workflow: experimental design → measurement → validation → analysis → modelling → limitations.

It does **not** claim IEEE publication, peer review, or certification.

## Limitations

The current study is bounded by one workload family, three sorting implementations, four input sizes, four repetitions, and one benchmark environment/collection batch. Python-level memory is measured rather than hardware performance counters, and the polynomial models should not be extrapolated far outside the observed range.

See [`docs/limitations.md`](docs/limitations.md).

## Future work

The project can be extended with larger inputs, more repetitions, additional algorithms and workload families, multi-machine experiments, CPU/GPU comparisons, richer hardware telemetry, stronger multivariable models, uncertainty estimation, and algorithm/resource recommendation.

## Author

**Hemanth Nomula**  
B.Tech Artificial Intelligence and Machine Learning  
SRM Institute of Science and Technology

GitHub: [@nexline-01xA](https://github.com/nexline-01xA)

## License

MIT License. See [`LICENSE`](LICENSE).
