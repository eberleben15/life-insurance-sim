import csv

with open("data/mortality_table.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["age", "gender", "smoker", "qx"])

    for age in range(30, 101):
        for gender in ["M", "F"]:
            for smoker in [True, False]:
                base_qx = 0.0005 * (1.07 ** (age - 30))  # Exponential increase
                if smoker:
                    base_qx *= 2  # Smokers have higher mortality
                writer.writerow([age, gender, smoker, round(min(base_qx, 1.0), 6)])