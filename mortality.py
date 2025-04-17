import pandas as pd
from models import MortalityRecord, Gender

def load_mortality_table(csv_path: str) -> list[MortalityRecord]:
    df = pd.read_csv(csv_path)
    records = []
    for _, row in df.iterrows():
        records.append(
            MortalityRecord(
                age=int(row['age']),
                gender=Gender(row['gender']),
                smoker=bool(row['smoker']),
                qx=float(row['qx'])
            )
        )
    return records

def lookup_qx(records: list[MortalityRecord], age: int, gender: Gender, smoker: bool) -> float:
    for record in records:
        if record.age == age and record.gender == gender and record.smoker == smoker:
            return record.qx
    return 0.0  # Assume no risk if not found (can adjust)