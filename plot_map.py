import csv
import json
import os
from PIL import Image, ImageDraw, ImageFont


def run():
    # Créer le dossier output s'il n'existe pas
    os.makedirs("output", exist_ok=True)
    
    img = Image.open("output/capture_epure.png")
    draw = ImageDraw.Draw(img)
    width, height = img.size

    lat_max, lon_min = 30.9994, -7.1161  # Coin haut gauche
    lat_min, lon_max = 30.8739, -6.7394  # Coin bas droit

    hotels = []
    with open("output/donnees_filtre.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["latitude"] and row["longitude"]:
                hotels.append({
                    "nom": row["nom"],
                    "lat": float(row["latitude"]),
                    "lon": float(row["longitude"]),
                    "classe": row.get("classe", ""),
                    "prix": row.get("prix", "")
                })

    def geo_to_pixel(lat, lon):
        x = (lon - lon_min) / (lon_max - lon_min) * width
        y = (lat_max - lat) / (lat_max - lat_min) * height
        return int(x), int(y)

    try:
        font = ImageFont.truetype("CenturyGothic.ttf", 14)  
    except:
        try:
            font = ImageFont.truetype("CENRG.ttf", 14)
        except:
            font = ImageFont.load_default()
            print("⚠️ Police Century Gothic introuvable, utilisation de la police par défaut.")

    # Préparer la légende JSON
    legende = []

    # Dessiner les points numérotés
    for i, h in enumerate(hotels, start=1):
        x, y = geo_to_pixel(h["lat"], h["lon"])
        r = 10
        draw.ellipse((x-r, y-r, x+r, y+r), fill="#31849B", outline="#8C8C8C")
        
        # Centrer le numéro au milieu du cercle
        text = str(i)
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x - tw/2, y - th/2), text, fill="white", font=font)
        
        # Ajouter à la légende JSON
        legende.append({
            "numero": i,
            "nom": h["nom"],
            "latitude": h["lat"],
            "longitude": h["lon"],
            "classe": h["classe"],
            "prix": h["prix"]
        })

    # Sauvegarder la carte
    img.save("output/donnees_map.png")

    # Sauvegarder la légende JSON
    with open("output/legende.json", "w", encoding="utf-8") as f:
        json.dump(legende, f, ensure_ascii=False, indent=4)

    print("✅ Carte générée : output/donnees_map.png")
    print("✅ Légende générée : output/legende.json")
    print("✅ Traitement terminé avec succès.")


if __name__ == "__main__":
    run()