import os, json, argparse
import numpy as np
import pandas as pd

DISTRICTS = [
    ("D01","Dhaka","Dhaka",10200000,23.81,90.41), ("D02","Faridpur","Dhaka",2160000,23.60,89.84),
    ("D03","Gazipur","Dhaka",5260000,24.00,90.42), ("D04","Gopalganj","Dhaka",1290000,23.00,89.82),
    ("D05","Kishoreganj","Dhaka",3260000,24.44,90.77), ("D06","Madaripur","Dhaka",1290000,23.16,90.18),
    ("D07","Manikganj","Dhaka",1550000,23.86,90.00), ("D08","Munshiganj","Dhaka",1620000,23.54,90.53),
    ("D09","Narayanganj","Dhaka",3900000,23.62,90.50), ("D10","Narsingdi","Dhaka",2580000,23.93,90.71),
    ("D11","Rajbari","Dhaka",1180000,23.75,89.64), ("D12","Shariatpur","Dhaka",1290000,23.24,90.43),
    ("D13","Tangail","Dhaka",4030000,24.25,89.91), ("D14","Chattogram","Chattogram",9160000,22.35,91.78),
    ("D15","Bandarban","Chattogram",480000,22.19,92.22), ("D16","Brahmanbaria","Chattogram",3300000,23.95,91.11),
    ("D17","Chandpur","Chattogram",2630000,23.23,90.67), ("D18","Cumilla","Chattogram",6210000,23.46,91.18),
    ("D19","Cox's Bazar","Chattogram",2820000,21.42,92.00), ("D20","Feni","Chattogram",1640000,23.01,91.39),
    ("D21","Khagrachhari","Chattogram",710000,23.11,91.98), ("D22","Lakshmipur","Chattogram",1930000,22.94,90.84),
    ("D23","Noakhali","Chattogram",3620000,22.86,91.09), ("D24","Rangamati","Chattogram",640000,22.65,92.17),
    ("D25","Rajshahi","Rajshahi",2910000,24.37,88.60), ("D26","Bogura","Rajshahi",3730000,24.84,89.37),
    ("D27","Chapainawabganj","Rajshahi",1830000,24.59,88.27), ("D28","Joypurhat","Rajshahi",950000,25.09,89.02),
    ("D29","Naogaon","Rajshahi",2780000,24.79,88.93), ("D30","Natore","Rajshahi",1850000,24.42,89.00),
    ("D31","Pabna","Rajshahi",2900000,24.00,89.23), ("D32","Sirajganj","Rajshahi",3350000,24.45,89.70),
    ("D33","Khulna","Khulna",2610000,22.84,89.54), ("D34","Bagerhat","Khulna",1610000,22.65,89.78),
    ("D35","Chuadanga","Khulna",1230000,23.64,88.85), ("D36","Jashore","Khulna",3070000,23.16,89.20),
    ("D37","Jhenaidah","Khulna",2000000,23.54,89.15), ("D38","Kushtia","Khulna",2140000,23.90,89.12),
    ("D39","Magura","Khulna",1030000,23.48,89.41), ("D40","Meherpur","Khulna",700000,23.76,88.63),
    ("D41","Narail","Khulna",780000,23.17,89.51), ("D42","Satkhira","Khulna",2190000,22.71,89.07),
    ("D43","Barishal","Barishal",2570000,22.70,90.35), ("D44","Barguna","Barishal",1010000,22.15,90.12),
    ("D45","Bhola","Barishal",1930000,22.68,90.64), ("D46","Jhalokati","Barishal",660000,22.64,90.19),
    ("D47","Patuakhali","Barishal",1720000,22.35,90.32), ("D48","Pirojpur","Barishal",1190000,22.58,89.97),
    ("D49","Sylhet","Sylhet",3850000,24.89,91.86), ("D50","Habiganj","Sylhet",2350000,24.37,91.41),
    ("D51","Moulvibazar","Sylhet",2120000,24.48,91.77), ("D52","Sunamganj","Sylhet",2690000,25.06,91.39),
    ("D53","Rangpur","Rangpur",3160000,25.74,89.27), ("D54","Dinajpur","Rangpur",3310000,25.62,88.63),
    ("D55","Gaibandha","Rangpur",2560000,25.32,89.52), ("D56","Kurigram","Rangpur",2320000,25.80,89.63),
    ("D57","Lalmonirhat","Rangpur",1420000,25.99,89.28), ("D58","Nilphamari","Rangpur",2090000,25.93,88.85),
    ("D59","Panchagarh","Rangpur",1170000,26.33,88.55), ("D60","Thakurgaon","Rangpur",1530000,26.03,88.46),
    ("D61","Mymensingh","Mymensingh",5890000,24.74,90.40), ("D62","Jamalpur","Mymensingh",2490000,24.92,89.94),
    ("D63","Netrokona","Mymensingh",2320000,24.87,90.72), ("D64","Sherpur","Mymensingh",1500000,25.02,90.01)
]

def build_geojson(out_path):
    features = []
    for did, name, div, pop, lat, lon in DISTRICTS:
        d = 0.22
        poly = [[[lon-d,lat-d],[lon+d,lat-d],[lon+d,lat+d],[lon-d,lat+d],[lon-d,lat-d]]]
        features.append({"type":"Feature","properties":{"district_id":did,"district_name":name,"division":div},"geometry":{"type":"Polygon","coordinates":poly}})
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump({"type":"FeatureCollection","features":features}, f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sf", type=float, default=0.02)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-date", type=str, default="2021-01-01")
    parser.add_argument("--end-date", type=str, default="2025-12-31")
    parser.add_argument("--output", type=str, default="data/raw")
    args = parser.parse_args()

    np.random.seed(args.seed)
    os.makedirs(args.output, exist_ok=True)
    # build_geojson disabled to protect real map

    pop_rows = []
    for did, name, div, pop, lat, lon in DISTRICTS:
        for band, share in [("0-14",0.26),("15-29",0.28),("30-49",0.27),("50-64",0.12),("65+",0.07)]:
            for sex in ["M", "F"]:
                pop_rows.append({"district_id":did,"district_name":name,"division":div,"age_band":band,"sex":sex,"population":int(pop*share*0.5)})
    pd.DataFrame(pop_rows).to_csv(os.path.join(args.output, "population.csv"), index=False)

    fac_rows = []
    for did, name, div, pop, lat, lon in DISTRICTS:
        for i in range(1, 11):
            fid = f"FAC-{did}-{i:02d}"
            ftype = "Hospital" if i <= 2 else ("Upazila_HC" if i <= 6 else "Clinic")
            beds = 250 if i <= 2 else (50 if i <= 6 else 15)
            fac_rows.append({"facility_id":fid,"district_id":did,"division":div,"facility_type":ftype,"beds":beds,"icu_beds":max(0, int(beds*0.08))})
    fac_df = pd.DataFrame(fac_rows)
    fac_df.to_csv(os.path.join(args.output, "facilities.csv"), index=False)

    dates = pd.date_range(args.start_date, args.end_date, freq="D")
    doy = dates.dayofyear.values
    weather_list = []
    for did, name, div, pop, lat, lon in DISTRICTS:
        temp = 26.0 + 6.0 * np.sin(2 * np.pi * (doy - 100) / 365.25) + np.random.normal(0, 1.2, len(dates))
        rain_prob = 0.15 + 0.60 * np.maximum(0, np.sin(2 * np.pi * (doy - 150) / 365.25))
        rain = np.where(np.random.rand(len(dates)) < rain_prob, np.random.gamma(2.2, 12.0, len(dates)), 0.0)
        hum = 65.0 + 22.0 * np.sin(2 * np.pi * (doy - 150) / 365.25) + np.random.normal(0, 3.0, len(dates))
        wdf = pd.DataFrame({"district_id":did,"date":dates.strftime("%Y-%m-%d"),"temperature_c":np.round(temp,1),"rainfall_mm":np.round(rain,1),"humidity_pct":np.round(np.clip(hum,30,100),1)})
        weather_list.append(wdf)
    pd.concat(weather_list, ignore_index=True).to_parquet(os.path.join(args.output, "weather.parquet"), index=False)

    diseases = [("A90","Dengue"), ("A00","Diarrhoea"), ("J10","Influenza"), ("B50","Malaria")]
    outbreaks = []
    for oid in range(1, 31):
        did = DISTRICTS[oid % 64][0]
        dis_code, dis_name = diseases[oid % 4]
        start_idx = np.random.randint(60, max(65, len(dates)-45))
        dur = np.random.randint(14, 35)
        outbreaks.append({
            "outbreak_id": f"OB-{oid:02d}", "district_id": did, "disease": dis_name, "icd10_code": dis_code,
            "start_date": dates[start_idx].strftime("%Y-%m-%d"),
            "end_date": dates[min(len(dates)-1, start_idx+dur)].strftime("%Y-%m-%d"),
            "multiplier": round(np.random.uniform(2.8, 5.5), 2)
        })
    ob_df = pd.DataFrame(outbreaks)
    ob_df.to_csv("generator/ground_truth_outbreaks.csv", index=False)

    stock_dates = dates[::7]
    stock_rows = []
    for _, frow in fac_df.iterrows():
        for d in stock_dates:
            stock_rows.append({
                "facility_id": frow["facility_id"], "district_id": frow["district_id"], "date": d.strftime("%Y-%m-%d"),
                "iv_saline": int(np.random.randint(80, 600)), "ns1_kits": int(np.random.randint(50, 400)),
                "ors": int(np.random.randint(200, 1500)), "antimalarials": int(np.random.randint(30, 200)),
                "occupied_beds": int(np.random.uniform(0.3, 0.9) * frow["beds"])
            })
    pd.DataFrame(stock_rows).to_parquet(os.path.join(args.output, "stock.parquet"), index=False)

    total_target = int(25_000_000 * args.sf)
    print(f"Generating {total_target:,} encounter records at SF={args.sf}...")

    d_ids = [d[0] for d in DISTRICTS]
    d_weights = np.array([d[3] for d in DISTRICTS], dtype=float)
    d_weights /= d_weights.sum()

    dist_chosen = np.random.choice(d_ids, size=total_target, p=d_weights)
    fac_num = np.random.randint(1, 11, size=total_target)
    fac_ids = "FAC-" + pd.Series(dist_chosen).str.cat(pd.Series(fac_num).apply(lambda x: f"-{x:02d}"), sep="")

    season_w = 1.0 + 0.65 * np.sin(2 * np.pi * (doy - 180) / 365.25)
    season_w /= season_w.sum()
    onset_idx = np.random.choice(len(dates), size=total_target, p=season_w)
    onset_dates = dates[onset_idx]
    delays = np.clip(np.random.gamma(1.8, 2.0, size=total_target).astype(int), 0, 21)
    report_dates = onset_dates + pd.to_timedelta(delays, unit="D")

    icd_choices = np.random.choice(["A90","A00","J10","B50","OTHER"], size=total_target, p=[0.32,0.28,0.20,0.08,0.12])
    cht_mask = np.isin(dist_chosen, ["D15","D21","D24"])
    icd_choices[cht_mask] = np.random.choice(["B50","A90","A00"], size=cht_mask.sum(), p=[0.65,0.20,0.15])

    enc_df = pd.DataFrame({
        "encounter_id": [f"ENC-{i:09d}" for i in range(total_target)],
        "patient_id": [f"NID-{np.random.randint(1000000, 9999999)}" for _ in range(total_target)],
        "facility_id": fac_ids.values,
        "district_id": dist_chosen,
        "onset_date": onset_dates.strftime("%Y-%m-%d"),
        "report_date": report_dates.strftime("%Y-%m-%d"),
        "age_years": np.random.choice([3, 12, 24, 38, 55, 72], size=total_target, p=[0.12,0.18,0.28,0.24,0.11,0.07]),
        "sex": np.random.choice(["M", "F"], size=total_target),
        "icd10_code": icd_choices,
        "lab_confirmed": np.random.choice([True, False], size=total_target, p=[0.62, 0.38]),
        "admitted": np.random.choice([True, False], size=total_target, p=[0.25, 0.75]),
        "outcome": np.random.choice(["RECOVERED", "DECEASED"], size=total_target, p=[0.985, 0.015])
    })

    ob_spikes = []
    for _, ob in ob_df.iterrows():
        n_extra = max(40, int(1800 * args.sf))
        ob_dates = pd.date_range(ob["start_date"], ob["end_date"])
        chosen_d = np.random.choice(ob_dates, size=n_extra)
        ob_spikes.append(pd.DataFrame({
            "encounter_id": [f"ENC-OB-{ob['outbreak_id']}-{i}" for i in range(n_extra)],
            "patient_id": [f"NID-{np.random.randint(1000000,9999999)}" for _ in range(n_extra)],
            "facility_id": f"FAC-{ob['district_id']}-01",
            "district_id": ob["district_id"],
            "onset_date": pd.to_datetime(chosen_d).strftime("%Y-%m-%d"),
            "report_date": (pd.to_datetime(chosen_d) + pd.to_timedelta(np.random.randint(0,4,n_extra), unit="D")).strftime("%Y-%m-%d"),
            "age_years": np.random.randint(5, 65, size=n_extra),
            "sex": np.random.choice(["M", "F"], size=n_extra),
            "icd10_code": ob["icd10_code"],
            "lab_confirmed": True, "admitted": True, "outcome": "RECOVERED"
        }))
    enc_df = pd.concat([enc_df] + ob_spikes, ignore_index=True)

    art_mask = (enc_df["facility_id"] == "FAC-D01-01") & (enc_df["onset_date"] >= "2024-08-01") & (enc_df["onset_date"] <= "2024-08-21")
    enc_df.loc[art_mask, "report_date"] = "2024-08-22"

    n = len(enc_df)
    enc_df.loc[np.random.choice(n, size=int(0.005 * n), replace=False), "facility_id"] = "FAC-ORPHAN-999"
    enc_df.loc[np.random.choice(n, size=int(0.005 * n), replace=False), "age_years"] = 212
    enc_df.loc[np.random.choice(n, size=int(0.005 * n), replace=False), "report_date"] = "2020-01-01"
    dup_rows = enc_df.sample(frac=0.02, random_state=args.seed)
    enc_df = pd.concat([enc_df, dup_rows], ignore_index=True)

    enc_df.to_parquet(os.path.join(args.output, "encounters.parquet"), index=False)
    print(f"Done! Wrote {len(enc_df):,} encounter records to {args.output}/encounters.parquet")

if __name__ == "__main__":
    main()
