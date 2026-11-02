# EPISCOPE — Bangladesh Epidemiological Surveillance & Decision Support System

 # Live Link - https://huggingface.co/spaces/rakib1010/episcope-bangladesh

**EPISCOPE** is an end-to-end Big Data epidemiological analytics platform designed for real-time disease surveillance, early outbreak detection, caseload forecasting, and equitable medical resource allocation across all **64 districts and 8 divisions of Bangladesh**.

Built on a **PySpark Medallion Lakehouse architecture (Bronze → Silver → Gold)**, EPISCOPE processes noisy, multi-source clinical reporting streams into decision-grade analytical marts and serves them through an offline-capable, zero-dependency **D3.js v7 Geospatial & Policy Simulation Dashboard**.

---

## Key Architectural Highlights

1. **Synthetic Epidemiological Data Generator (`generator/generate_data.py`)**
   * Simulates multi-year district-level weekly surveillance reports across 64 Bangladesh districts (`D01`–`D64`) for endemic and epidemic pathogens (e.g., Dengue, Cholera/AWD, Malaria, Nipah, Chikungunya).
   * Injects realistic reporting flaws (duplicates, negative counts, out-of-bounds epi-weeks, schema drift, missing timestamps) alongside ground-truth outbreak surges.

2. **PySpark Medallion Lakehouse (`pipeline/`)**
   * **Bronze Layer (`ingest_bronze.py`):** Raw schema enforcement, ingestion metadata tagging, and append-only Parquet storage.
   * **Silver Layer (`transform_silver.py`):** Enforces **12 automated Data Quality (DQ) rules**, quarantining malformed records while standardizing district names, ISO epi-weeks, and population denominators.
   * **Gold Layer (`build_gold.py`):** Builds district-week analytical marts with rolling baselines, incidence per 100,000 population, and demand-supply telemetry.

3. **Advanced Epidemiological Analytics & Policy Simulators (`analytics/`)**
   * **Outbreak Detection & Conflict C1 ROC (`detection/run_detection.py`):** Computes rolling Z-score anomalies ($Z = \frac{Y_t - \mu}{\sigma}$) and evaluates **Conflict C1**—the trade-off between **Outbreak Sensitivity**, **False Alerts per District-Year**, and **Median Days to Detect** across thresholds $Z \in [1.5, 4.0]$.
   * **Caseload Forecasting (`forecast/run_forecast.py`):** Generates 4-week ahead projections per district and pathogen with **80% prediction intervals (`pi_low_80` – `pi_high_80`)**.
   * **PuLP Resource Optimization & Conflict C3 Equity (`optimise/run_optimiser.py`):** Formulates medical supply dispatch (`ORS`, `IV_FLUIDS`, `NS1_KITS`, `BED_NETS`) as a Linear Programming problem using **PuLP**. Evaluates **Conflict C3**—the trade-off between pure utilitarian efficiency ($\alpha = 0.0$) and strict minimum district equity floors ($\alpha \in \{0.3, 0.6, 0.95\}$) across budgets from `1M` to `10M` BDT.
   * **Seasonal Preparedness Matrix (`calendar/build_calendar.py`):** Aggregates 52 epi-week × 8 division historical intensity matrices for pre-monsoon and winter surge staging.

4. **Interactive D3.js Command Center (`dashboard/`)**
   * **64-District Choropleth Map** with live metric toggling (`Cases` | `Incidence/100k` | `Z-Score`) and click-to-filter scope.
   * **52-Week Historical + 4-Week Spark Forecast Horizon** with 80% prediction interval stems.
   * **Division × 52 Epi-Week Seasonality Heatmap**.
   * **Interactive Conflict C1 (Z-Score ROC) & Conflict C3 (Budget/Equity $\alpha$) Policy Simulators**.

---

## Repository Structure

```text
episcope/
├── README.md
├── requirements.txt
├── .gitignore
├── run_pipeline.py                      # End-to-end pipeline orchestrator
├── generator/
│   └── generate_data.py                 # Synthetic 64-district epidemiological data generator
├── pipeline/
│   ├── bronze/
│   │   └── ingest_bronze.py             # Raw -> Bronze Parquet ingestion
│   ├── silver/
│   │   └── transform_silver.py          # 12 Data Quality (DQ) rules & quarantine
│   └── gold/
│       └── build_gold.py                # District-week Gold analytical mart builder
├── analytics/
│   ├── detection/
│   │   └── run_detection.py             # Z-score outbreak detector & Conflict C1 ROC evaluator
│   ├── forecast/
│   │   └── run_forecast.py              # 4-week caseload forecaster with 80% PI
│   ├── optimise/
│   │   └── run_optimiser.py             # PuLP LP supply allocator & Conflict C3 Equity grid
│   └── calendar/
│       └── build_calendar.py            # Division x 52 Epi-Week seasonality matrix
├── serving/
│   └── export_dashboard_json.py         # Exports Gold marts & GeoJSON into dashboard JSON/bundle.js
├── dashboard/
│   ├── index.html                       # Interactive D3.js v7 Command Center UI
│   ├── bundle.js                        # Pre-bundled offline data payload (__EPISCOPE_*__)
│   ├── districts.geojson                # 64-district Bangladesh boundary polygons
│   ├── dashboard_mart.json              # Exported Gold mart telemetry
│   ├── conflict_c1_roc.json             # Conflict C1 ROC sensitivity vs. false-alarm metrics
│   └── conflict_c3_equity.json          # Conflict C3 Budget vs. Equity (alpha) optimization grid
├── data/
│   ├── raw/                             # Synthetic input datasets (.gitkeep)
│   ├── bronze/                          # Bronze Parquet tables (.gitkeep)
│   ├── silver/                          # Silver Parquet tables & DQ quarantine (.gitkeep)
│   └── gold/                            # Gold Parquet analytical marts (.gitkeep)
└── tests/
    └── test_episcope.py                 # Automated Pytest suite (DQ rules, Z-score, PuLP LP)
```

---

## Quick Start & Execution Guide

### 1. Environment Setup
Ensure **Python 3.10+** and **Java 11/17 (JDK)** are installed for PySpark.

```powershell
git clone [https://github.com/rakib10-10/Episcope_Big_Data_Project.git](https://github.com/rakib10-10/Episcope_Big_Data_Project.git)
cd Episcope_Big_Data_Project

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run the Full Medallion & Analytics Pipeline
Execute each stage sequentially (or via `python run_pipeline.py` if present):

```powershell
# Step 1: Generate synthetic 64-district surveillance & ground-truth outbreak data
python generator/generate_data.py

# Step 2: Run Medallion Lakehouse (Bronze -> Silver [12 DQ Rules] -> Gold)
python pipeline/bronze/ingest_bronze.py
python pipeline/silver/transform_silver.py
python pipeline/gold/build_gold.py

# Step 3: Run Epidemiological Analytics (Detection C1, Forecast, PuLP C3, Calendar)
python analytics/detection/run_detection.py
python analytics/forecast/run_forecast.py
python analytics/optimise/run_optimiser.py
python analytics/calendar/build_calendar.py

# Step 4: Export Gold marts to dashboard JSON & bundle.js
python serving/export_dashboard_json.py
```

### 3. Launch the Interactive D3.js Dashboard
Because `dashboard/bundle.js` pre-bundles the exported JSON and GeoJSON payloads into `window.__EPISCOPE_*__` globals, you can open `dashboard/index.html` directly in any browser or serve it over HTTP:

```powershell
python -m http.server 8080 --directory dashboard
```
Then open **`http://localhost:8080`** in your browser.

### 4. Run Automated Unit & Data Quality Tests
```powershell
pytest tests/test_episcope.py -v
```
