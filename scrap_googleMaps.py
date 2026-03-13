import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
import random
import os

def run(recherche="hôtels Ouarzazate"):
    """
    Lance le scraping Google Maps et sauvegarde donnees.csv
    Retourne le chemin du CSV généré
    """
    # Créer le dossier output s'il n'existe pas
    os.makedirs("output", exist_ok=True)
    
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.google.com/maps")
        time.sleep(random.uniform(2, 4))

        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(recherche)
        search_box.send_keys(Keys.ENTER)
        time.sleep(random.uniform(6, 9))

        results_panel = driver.find_element(By.XPATH, '//div[contains(@aria-label,"Résultats pour")]')

        last_height = 0
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_panel)
            time.sleep(random.uniform(1, 2))
            new_height = driver.execute_script("return arguments[0].scrollHeight", results_panel)
            if new_height == last_height:
                break
            last_height = new_height

        links_to_visit = []
        results = driver.find_elements(By.XPATH, '//a[contains(@href,"/maps/place")]')
        for result in results:
            name = result.get_attribute("aria-label")
            link = result.get_attribute("href")
            if link and (link not in [l[1] for l in links_to_visit]):
                links_to_visit.append((name, link))

        data = []

        for idx, (name, link) in enumerate(links_to_visit):
            try:
                driver.get(link)
                time.sleep(random.uniform(2, 5))

                lat, lon = None, None
                match_at = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", link or "")
                match_d = re.search(r"!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)", link or "")
                if match_at:
                    lat, lon = match_at.groups()
                elif match_d:
                    lat, lon = match_d.groups()

                try:
                    classe_elem = driver.find_element(By.XPATH, '//span[contains(text(),"étoile")]')
                    classe = classe_elem.text
                except:
                    classe = ""

                try:
                    prix_elem = driver.find_element(By.XPATH, '//span[contains(text(),"MAD")]')
                    prix = prix_elem.text
                except:
                    prix = ""

                data.append({
                    "nom": name,
                    "lien": link,
                    "latitude": lat,
                    "longitude": lon,
                    "classe": classe,
                    "prix": prix
                })

                print(f"[{idx+1}/{len(links_to_visit)}] {name} ✅")
                time.sleep(random.uniform(1, 3))

            except Exception as e:
                print(f"Erreur sur {idx+1} ({name}): {e}")
                continue

        file_path = os.path.join("output", "donnees.csv")
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nom", "lien", "latitude", "longitude", "classe", "prix"])
            writer.writeheader()
            writer.writerows(data)

        print(f"\n✅ Total résultats trouvés : {len(data)}")
        print(f"📁 Données enregistrées dans {file_path}")
        return file_path

    finally:
        driver.quit()


if __name__ == "__main__":
    run()