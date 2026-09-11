readme_content = """# Litigation Support Workpaper Engine

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![pytest](https://img.shields.io/badge/pytest-100%25-green.svg)](https://docs.pytest.org/)

An automated, production-grade forensic data pipeline designed to ingest raw transactional exception logs and audit outputs (from engines like `fee-leakage-audit`), transform them via zero-copy vectorization, and output structured, audit-ready summary tables, comprehensive analytical work papers, and visual trial exhibits for litigation support under **ERISA Section 406 (Prohibited Transactions) and Section 408 (Exemptions)** enforcement actions.

---

## Direct EBSA GS-14 Alignment

Built specifically to satisfy **U.S. Department of Labor EBSA GS-14 Specialized Experience** requirements:
1. **Voluminous Financial Records:** Rigorously parses and aggregates massive transactional logs, maintaining zero numerical drift and absolute evidentiary integrity.
2. **Analytical Work Products:** Automatically compiles structured summary schedules, statistical breakdowns, and certified textual workpapers suitable for administrative proceedings and federal court litigation.
3. **Trial Preparation & Support:** Outputs clean, indexed schedule CSVs and evidentiary exhibits designed to support the Office of the Solicitor (SOL) and investigative teams.

---

## Core Architecture & Technical Mandates

* **Python 3.12+ Standards:** Utilizes native lowercase generics (`list`, `dict`) and pipe syntax (`|`) without legacy typing imports or `from __future__ import annotations`.
* **Anti-Loop Mandate:** Strictly prohibits explicit loops (`for`, `while`) and legacy `pandas.apply()` across all mathematical calculations and vector aggregations.
* **Forced Vectorization:** Implements SIMD-aligned vectorization via NumPy linear algebra engines and zero-copy contiguous memory access (`.to_numpy(dtype=np.float64, copy=False)`).
* **Modular src-layout:** Clean separation of concerns across ingestion, vector aggregation, and workpaper rendering modules, backed by 100% `pytest` test coverage mapped to formal test case IDs (`TC-01+`).

---

## Project Structure

```text
litigation-support-workpaper-engine/
├── pyproject.toml
├── README.md
├── src/
│   └── litigation_engine/
│       ├── __init__.py
│       ├── ingestion.py
│       ├── aggregation.py
│       ├── workpaper.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_aggregation.py
│   └── test_workpaper.py
└── data/
    └── sample_transactions.csv
```

---

## Setup

```
# 1. Clone repository and create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Upgrade packaging toolchain
pip install --upgrade pip setuptools wheel

# 3. Install package in editable mode with development/testing dependencies
pip install -e ".[dev]"

# 4. Running the Pipeline
python src/litigation_engine/main.py

# 5. Execute the test suite
pytest -v --cov=litigation_engine --cov-report=term-missing
```

---

## Sample Output

```
================================================================================
EXHIBIT WORKPAPER: EBSA LITIGATION SUPPORT SUPPORTING ANALYSIS
CASE CAPTION: EBSA v. Vertex Retirement Services LLC (Case No. 2:26-cv-0406)
STATUTORY AUTHORITY: ERISA SECTION 406 / 408 ENFORCEMENT
================================================================================
SUMMARY STATISTICS:
  - Total Prohibited Transactions Identified: 3
  - Cumulative Disputed Restitution Amount:   $75,700.50
--------------------------------------------------------------------------------
DETAILED PLAN-LEVEL BREAKDOWN:
--------------------------------------------------------------------------------
   plan_id breach_type  transaction_count  total_loss_amount  mean_loss_amount  max_loss_amount  cumulative_liability
Plan_Alpha      406(a)                  2            60700.5          30350.25          48200.5               60700.5
 Plan_Beta      406(b)                  1            15000.0          15000.00          15000.0               75700.5
================================================================================
END OF WORKPAPER - CERTIFIED TRUE AND CORRECT
================================================================================
```

---
