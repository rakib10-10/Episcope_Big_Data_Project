"""Aggregate encounters.parquet into a small docs/data.js for the static dashboard.
Run from the project root:  python make_web_data.py
"""
import json, os, sys
import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else r"C:\Rakib-1173-C-42\backup\encounters.parquet"
OUT = os.path.join("docs", "data.js")

df = pd.read_parquet(SRC)
df["onset_date"] = pd.to_datetime(df["onset_date"], errors="coerce")
df["report_date"] = pd.to_datetime(df["report_date"], errors="coerce")
df["month"] = df["onset_date"].dt.strftime("%Y-%m")
df["delay"] = (df["report_date"] - df["onset_date"]).dt.days
df["age_group"] = pd.cut(
    df["age_years"], bins=[-1, 4, 14, 24, 44, 64, 200],
    labels=["0-4", "5-14", "15-24", "25-44", "45-64", "65+"],
).astype(str)

monthly = df.groupby(["month", "icd10_code"]).size().unstack(fill_value=0).sort_index()
age_sex = df.groupby(["age_group", "sex"]).size().unstack(fill_value=0)
age_sex = age_sex.reindex(["0-4", "5-14", "15-24", "25-44", "45-64", "65+"]).fillna(0)
dist = df.groupby("district_id").agg(
    cases=("encounter_id", "size"), admitted=("admitted", "sum"), lab=("lab_confirmed", "sum")
).sort_values("cases", ascending=False).head(20)
outcomes = df["outcome"].value_counts()
by_code = df["icd10_code"].value_counts()

data = {
    "total": int(len(df)),
    "patients": int(df["patient_id"].nunique()),
    "districts": int(df["district_id"].nunique()),
    "facilities": int(df["facility_id"].nunique()),
    "lab_pct": round(float(df["lab_confirmed"].mean() * 100), 1),
    "admit_pct": round(float(df["admitted"].mean() * 100), 1),
    "avg_delay": round(float(df["delay"].mean()), 2),
    "date_min": str(df["onset_date"].min().date()),
    "date_max": str(df["onset_date"].max().date()),
    "months": monthly.index.tolist(),
    "monthly": {c: monthly[c].astype(int).tolist() for c in monthly.columns},
    "age_groups": age_sex.index.tolist(),
    "age_sex": {s: age_sex[s].astype(int).tolist() for s in age_sex.columns},
    "dist_names": dist.index.tolist(),
    "dist_cases": dist["cases"].astype(int).tolist(),
    "dist_admitted": dist["admitted"].astype(int).tolist(),
    "dist_lab": dist["lab"].astype(int).tolist(),
    "outcome_names": outcomes.index.astype(str).tolist(),
    "outcome_counts": outcomes.astype(int).tolist(),
    "code_names": by_code.index.astype(str).tolist(),
    "code_counts": by_code.astype(int).tolist(),
}

os.makedirs("docs", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("window.DATA = " + json.dumps(data) + ";")
print("Wrote", OUT, round(os.path.getsize(OUT) / 1024, 1), "KB")
