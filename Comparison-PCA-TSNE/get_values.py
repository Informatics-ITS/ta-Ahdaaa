import json
import random
from main import merge_datasets

def get_random_sample_json(label=1):
    merged = merge_datasets()
    
    # Filter sesuai label
    subset = merged[merged["defective"] == label]
    
    if subset.empty:
        raise ValueError(f"Tidak ditemukan data dengan label defective = {label}")
    
    # Ambil baris acak
    row = subset.sample(n=1, random_state=random.randint(0, 9999)).iloc[0]

    # Ubah jadi dict dan cetak JSON
    data_dict = row.drop("defective").to_dict()
    data_dict["defective"] = int(row["defective"])  # Sertakan juga label untuk validasi manual

    return json.dumps(data_dict, indent=2)

print("🎯 Random DEFECT sample:")
print(get_random_sample_json(label=1))

# print("\n✅ Random NON-DEFECT sample:")
# print(get_random_sample_json(label=0))