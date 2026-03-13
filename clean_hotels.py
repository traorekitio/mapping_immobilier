import csv
import re
import os

def clean_data(input_file, output_file, critere, seuil, comparaison):
    cleaned_data = []

    with open(input_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            valeur = row.get(critere, "").strip()

            if not valeur:
                continue

            match = re.search(r"(\d+)", valeur)
            if match:
                valeur_num = int(match.group(1))
            else:
                continue

            garder = False
            if comparaison == ">":
                garder = valeur_num > seuil
            elif comparaison == ">=":
                garder = valeur_num >= seuil
            elif comparaison == "<":
                garder = valeur_num < seuil
            elif comparaison == "<=":
                garder = valeur_num <= seuil
            elif comparaison == "==":
                garder = valeur_num == seuil

            if garder:
                cleaned_data.append(row)

    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    return len(cleaned_data)  
