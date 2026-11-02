import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from serving.export_dashboard_json import suppress_small_cells
from analytics.optimise.run_optimiser import solve_allocation

def test_small_cell_suppression():
    s = pd.Series([2, 10, 25, 40])
    res = suppress_small_cells(s)
    assert res[0] == "<5"
    assert res.count("<5") >= 2

def test_optimiser_budget_constraint():
    df = pd.DataFrame([
        {"district_id": "D01", "division": "Dhaka", "demand_iv_saline": 500, "demand_ns1_kits": 200, "demand_ors": 800,
         "stock_iv_saline": 100, "stock_ns1_kits": 50, "stock_ors": 200, "pop_share": 0.6, "vuln_weight": 1.2},
        {"district_id": "D02", "division": "Dhaka", "demand_iv_saline": 300, "demand_ns1_kits": 100, "demand_ors": 400,
         "stock_iv_saline": 50, "stock_ns1_kits": 20, "stock_ors": 100, "pop_share": 0.4, "vuln_weight": 1.0}
    ])
    alloc_df, _ = solve_allocation(df, budget=50000, alpha=0.3)
    costs = {"iv_saline": 80.0, "ns1_kits": 250.0, "ors": 15.0}
    total_spent = sum(row["allocated"] * costs[row["resource"]] for _, row in alloc_df.iterrows())
    assert total_spent <= 50000.1
