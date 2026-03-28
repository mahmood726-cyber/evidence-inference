"""
Download SYNERGY Benchmark Dataset for ASReview 5-Star
Phase 1.2: Integrate systematic reviews from SYNERGY benchmark
"""

import os
import pandas as pd
import requests
from io import StringIO

print("=" * 60)
print("SYNERGY Benchmark Dataset Download")
print("=" * 60)

# SYNERGY datasets from official list
SYNERGY_DATASETS = [
    ("Appenzeller-Herzog_2019", 2873, 26),
    ("Bos_2018", 4878, 10),
    ("Brouwer_2019", 38114, 62),
    ("Chou_2003", 1908, 15),
    ("Chou_2004", 1630, 9),
    ("Donners_2021", 258, 15),
    ("Hall_2012", 8793, 104),
    ("Jeyaraman_2020", 1175, 96),
    ("Leenaars_2019", 5812, 17),
    ("Leenaars_2020", 7216, 583),
    ("Meijboom_2021", 882, 37),
    ("Menon_2022", 975, 74),
    ("Moran_2021", 5214, 111),
    ("Muthu_2021", 2719, 336),
    ("Nelson_2002", 366, 80),
    ("Oud_2018", 952, 20),
    ("Radjenovic_2013", 5935, 48),
    ("Sep_2021", 271, 40),
    ("Smid_2020", 2627, 27),
    ("van_de_Schoot_2017", 4544, 38),
    ("van_der_Valk_2021", 841, 15),
    ("van_der_Waal_2022", 3866, 23),
    ("van_Dis_2020", 9128, 72),
    ("Wassenaar_2017", 9511, 39),
    ("Wolters_2018", 5472, 17),
    ("Bannach-Brown_2019", 5593, 36),
]

print(f"\nTotal SYNERGY datasets: {len(SYNERGY_DATASETS)}")
total_records = sum(d[1] for d in SYNERGY_DATASETS)
total_included = sum(d[2] for d in SYNERGY_DATASETS)
print(f"Total records: {total_records:,}")
print(f"Total included: {total_included:,}")
print(f"Prevalence: {total_included/total_records*100:.2f}%")

# Create output directory
output_dir = "C:/Users/user/synergy_benchmark"
os.makedirs(output_dir, exist_ok=True)

# Download datasets using synergy_dataset CLI
print("\n" + "-" * 60)
print("Downloading SYNERGY datasets...")
print("-" * 60)

all_records = []

# Use direct GitHub raw URLs for each dataset
base_url = "https://raw.githubusercontent.com/asreview/synergy-dataset/master/datasets"

for ds_name, n_records, n_included in SYNERGY_DATASETS[:10]:  # First 10 for speed
    try:
        print(f"\nDownloading: {ds_name} ({n_records:,} records)")

        # Try to get the dataset
        # SYNERGY datasets are stored as individual review CSVs
        url = f"{base_url}/{ds_name}/{ds_name}.csv"
        resp = requests.get(url, timeout=60)

        if resp.status_code == 200:
            df = pd.read_csv(StringIO(resp.text))
            df['review_id'] = f"SYNERGY_{ds_name}"
            df['source'] = 'SYNERGY'

            # Standardize label column
            if 'label_included' not in df.columns:
                if 'included' in df.columns:
                    df['label_included'] = df['included']
                elif 'label' in df.columns:
                    df['label_included'] = df['label']

            all_records.append(df)
            print(f"   Downloaded: {len(df):,} records")
        else:
            print(f"   HTTP {resp.status_code} - trying alternative...")

            # Try alternative path
            url2 = f"{base_url}/{ds_name}/output/{ds_name}.csv"
            resp2 = requests.get(url2, timeout=60)
            if resp2.status_code == 200:
                df = pd.read_csv(StringIO(resp2.text))
                df['review_id'] = f"SYNERGY_{ds_name}"
                df['source'] = 'SYNERGY'
                all_records.append(df)
                print(f"   Downloaded: {len(df):,} records")
            else:
                print(f"   Not found")

    except Exception as e:
        print(f"   Error: {str(e)[:50]}")
        continue

# Combine available datasets
if all_records:
    synergy_df = pd.concat(all_records, ignore_index=True)

    # Ensure required columns exist
    required_cols = ['title', 'abstract', 'label_included', 'review_id', 'source']
    for col in required_cols:
        if col not in synergy_df.columns:
            synergy_df[col] = ""

    # Save combined dataset
    output_file = os.path.join(output_dir, "synergy_benchmark_combined.csv")
    synergy_df.to_csv(output_file, index=False)

    print("\n" + "=" * 60)
    print("SYNERGY DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Datasets downloaded: {len(all_records)}")
    print(f"Total records: {len(synergy_df):,}")

    if 'label_included' in synergy_df.columns:
        n_incl = synergy_df['label_included'].sum()
        print(f"Included: {n_incl:,}")
        print(f"Excluded: {len(synergy_df) - n_incl:,}")
        print(f"Prevalence: {n_incl/len(synergy_df)*100:.2f}%")

    print(f"\nSaved to: {output_file}")

else:
    print("\nNo datasets downloaded - using metadata only")

    # Create metadata-only dataset
    metadata_df = pd.DataFrame([
        {
            'dataset_name': name,
            'n_records': n_rec,
            'n_included': n_incl,
            'prevalence': n_incl/n_rec,
            'source': 'SYNERGY'
        }
        for name, n_rec, n_incl in SYNERGY_DATASETS
    ])

    meta_file = os.path.join(output_dir, "synergy_metadata.csv")
    metadata_df.to_csv(meta_file, index=False)
    print(f"Metadata saved to: {meta_file}")

print("\n" + "=" * 60)
print("SYNERGY benchmark reference created!")
print("=" * 60)
