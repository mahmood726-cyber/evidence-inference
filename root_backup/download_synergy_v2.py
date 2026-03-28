"""
Download SYNERGY using synergy_dataset CLI
"""

import subprocess
import os
import pandas as pd

print("=" * 60)
print("SYNERGY Download via CLI")
print("=" * 60)

output_dir = "C:/Users/user/synergy_benchmark"
os.makedirs(output_dir, exist_ok=True)

# Use synergy_dataset show command to get datasets
datasets_to_get = [
    "Appenzeller-Herzog_2019",
    "Hall_2012",
    "Donners_2021",
    "Nelson_2002",
    "Sep_2021"
]

all_data = []

for ds_name in datasets_to_get:
    print(f"\nGetting {ds_name}...")
    try:
        # The synergy_dataset package downloads to a cache and provides data
        result = subprocess.run(
            ["synergy_dataset", "get", ds_name, "-o", f"{output_dir}/{ds_name}.csv"],
            capture_output=True,
            text=True,
            timeout=120
        )
        print(result.stdout[:500] if result.stdout else "")
        if result.stderr:
            print(f"  Info: {result.stderr[:200]}")

        # Check if file was created
        output_file = f"{output_dir}/{ds_name}.csv"
        if os.path.exists(output_file):
            df = pd.read_csv(output_file)
            print(f"  Downloaded: {len(df)} records")
            df['review_id'] = f"SYNERGY_{ds_name}"
            all_data.append(df)
    except Exception as e:
        print(f"  Error: {e}")

if all_data:
    combined = pd.concat(all_data, ignore_index=True)
    combined.to_csv(f"{output_dir}/synergy_combined.csv", index=False)
    print(f"\nCombined: {len(combined)} records")
else:
    print("\nUsing SYNERGY metadata as reference benchmark")

    # Create benchmark reference
    synergy_ref = pd.DataFrame([
        {"dataset": "Appenzeller-Herzog_2019", "records": 2873, "included": 26, "topic": "Medicine"},
        {"dataset": "Bos_2018", "records": 4878, "included": 10, "topic": "Medicine"},
        {"dataset": "Brouwer_2019", "records": 38114, "included": 62, "topic": "Psychology"},
        {"dataset": "Chou_2003", "records": 1908, "included": 15, "topic": "Medicine"},
        {"dataset": "Chou_2004", "records": 1630, "included": 9, "topic": "Medicine"},
        {"dataset": "Donners_2021", "records": 258, "included": 15, "topic": "Medicine"},
        {"dataset": "Hall_2012", "records": 8793, "included": 104, "topic": "CompSci"},
        {"dataset": "Jeyaraman_2020", "records": 1175, "included": 96, "topic": "Medicine"},
        {"dataset": "Leenaars_2019", "records": 5812, "included": 17, "topic": "Psychology"},
        {"dataset": "Leenaars_2020", "records": 7216, "included": 583, "topic": "Medicine"},
        {"dataset": "Meijboom_2021", "records": 882, "included": 37, "topic": "Medicine"},
        {"dataset": "Menon_2022", "records": 975, "included": 74, "topic": "Medicine"},
        {"dataset": "Moran_2021", "records": 5214, "included": 111, "topic": "Biology"},
        {"dataset": "Muthu_2021", "records": 2719, "included": 336, "topic": "Medicine"},
        {"dataset": "Nelson_2002", "records": 366, "included": 80, "topic": "Medicine"},
        {"dataset": "Oud_2018", "records": 952, "included": 20, "topic": "Psychology"},
        {"dataset": "Radjenovic_2013", "records": 5935, "included": 48, "topic": "CompSci"},
        {"dataset": "Sep_2021", "records": 271, "included": 40, "topic": "Psychology"},
        {"dataset": "Smid_2020", "records": 2627, "included": 27, "topic": "CompSci"},
        {"dataset": "van_de_Schoot_2017", "records": 4544, "included": 38, "topic": "Psychology"},
        {"dataset": "van_der_Valk_2021", "records": 841, "included": 15, "topic": "Medicine"},
        {"dataset": "van_der_Waal_2022", "records": 3866, "included": 23, "topic": "Medicine"},
        {"dataset": "van_Dis_2020", "records": 9128, "included": 72, "topic": "Psychology"},
        {"dataset": "Wassenaar_2017", "records": 9511, "included": 39, "topic": "Medicine"},
        {"dataset": "Wolters_2018", "records": 5472, "included": 17, "topic": "Medicine"},
        {"dataset": "Bannach-Brown_2019", "records": 5593, "included": 36, "topic": "Biology"},
    ])

    synergy_ref['prevalence'] = synergy_ref['included'] / synergy_ref['records'] * 100
    synergy_ref.to_csv(f"{output_dir}/synergy_reference.csv", index=False)

    print(f"\nSYNERGY Reference Stats:")
    print(f"  Total datasets: {len(synergy_ref)}")
    print(f"  Total records: {synergy_ref['records'].sum():,}")
    print(f"  Total included: {synergy_ref['included'].sum():,}")
    print(f"  Mean prevalence: {synergy_ref['prevalence'].mean():.2f}%")

print("\nDone!")
