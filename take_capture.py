import pyautogui
import time
import webbrowser
import sys
import pytesseract  
from PIL import Image
import csv
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def log(message):
    print(f"[🟢] {message}")


def wait_for_element(driver, xpath, timeout=30):
    """Attend qu'un élément soit présent et visible"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        log(f"✅ Élément trouvé : {xpath}")
        return element
    except TimeoutException:
        log(f"⏰ Timeout - Élément non trouvé : {xpath}")
        return None


def wait_for_page_load(driver, timeout=30):
    """Attend que la page soit complètement chargée"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        log("✅ Page complètement chargée")
        return True
    except TimeoutException:
        log("⏰ Timeout - Page pas complètement chargée")
        return False


def wait_for_visual_element(image_path, confidence=0.8, timeout=30):
    """Attend qu'un élément visuel apparaisse à l'écran"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                log(f"✅ Élément visuel trouvé : {image_path}")
                return location
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(1)
    
    log(f"⏰ Timeout - Élément visuel non trouvé : {image_path}")
    return None


def run(zone: str):
    """
    Lance Google Earth Web, capture une zone et sauvegarde l'image + coordonnées
    Args:
        zone (str): nom de la zone à rechercher (ex: "Ouarzazate")
    Returns:
        str: chemin de l'image capturée
    """
    # Créer le dossier output s'il n'existe pas
    os.makedirs("output", exist_ok=True)
    
    # Configuration du navigateur
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    
    try:
        log(f"Lancement de Google Earth Web pour la zone '{zone}'")
        driver.get("https://earth.google.com/web/@0,-3.34350003,0a,22251752.77375655d,35y,0h,0t,0r/data=CgRCAggBOgMKATBCAggASg0I____________ARAA")
        
        # Attendre que la page soit chargée
        wait_for_page_load(driver)
        time.sleep(4)
        log(f"Fermeture de la fenêtre de publicité")
        pyautogui.click(x=1209, y=303)  # Fallback
        time.sleep(4)

        log(f"Fermeture du commentaire")
        pyautogui.click(x=1877, y=148)  # Fallback
        time.sleep(2)
        # Attendre que la barre de recherche soit disponible
        search_box = wait_for_element(driver, "//input[@aria-label='Rechercher']", timeout=20)
        if not search_box:
            # Essayer avec un autre sélecteur
            search_box = wait_for_element(driver, "//input[@placeholder='Rechercher dans Google Earth']", timeout=10)
        
        if search_box:
            log(f"Saisie de la requête : '{zone}'")
            search_box.clear()
            search_box.send_keys(zone)
            search_box.send_keys("\n")
        else:
            log(f"Fermeture de la fenêtre de publicité")
            pyautogui.click(x=1209, y=303)  # Fallback
            time.sleep(2)
            # Fallback vers pyautogui si Selenium ne trouve pas l'élément
            log("Utilisation de pyautogui comme fallback")
            pyautogui.click(x=234, y=243)
            time.sleep(2)
            pyautogui.typewrite(zone, interval=0.1)
            pyautogui.press("enter")
        
        # Attendre que la recherche soit terminée (attendre que la vue change)
        log("Attente de la fin de la recherche...")
        time.sleep(15)  # Délai minimum pour la recherche
        
        # Vérifier si une popup de résultats est apparue
        popup_xpath = "//div[contains(@class, 'place-card') or contains(@class, 'search-result')]"
        popup = wait_for_element(driver, popup_xpath, timeout=10)
        
        log(f"Zoom arrière pour cadrer la zone {zone}.")
        pyautogui.moveTo(960, 540)
        for _ in range(1):
            pyautogui.scroll(-300)
            time.sleep(1)

        # Fermer la popup si elle existe
        log(f"Fermeture de la fenêtre descriptive de {zone} avant le if.")
        pyautogui.click(x=1866, y=281)  # Fallback
        if popup:
            log(f"Fermeture de la fenêtre descriptive de {zone}.")
            close_button = wait_for_element(driver, "//button[@aria-label='Fermer' or @aria-label='Close']", timeout=5)
            if close_button:
                close_button.click()
            else:
                pyautogui.click(x=1866, y=281)  # Fallback
            time.sleep(2)

        log("Ouverture du menu 'Calques'.")
        layers_button = wait_for_element(driver, "//button[@aria-label='Calques' or contains(@aria-label, 'Layers')]", timeout=10)
        if layers_button:
            layers_button.click()
        else:
            pyautogui.click(x=65, y=928)  # Fallback
        time.sleep(2)

        log("Sélection du calque 'Épuré'.")
        clean_layer = wait_for_element(driver, "//div[contains(text(), 'Épuré') or contains(text(), 'Clean')]", timeout=10)
        if clean_layer:
            clean_layer.click()
        else:
            #pyautogui.click(x=141, y=656)  # Fallback
            pyautogui.click(x=162, y=618)  # Fallback
        time.sleep(2)

        log(f"Fermeture de la petite fenêtre explication.")
        pyautogui.click(x=56, y=298)  # Fallback
        time.sleep(2)

        log("Fermeture du menu 'Calques'.")
        pyautogui.click(x=364, y=275)
        time.sleep(2)



        log("Capture d'écran en cours...")
        left, top, width, height = 96, 289, 1754, 564
        image_path = "output/capture_epure.png"
        screenshot = pyautogui.screenshot(
            image_path,
            region=(left, top, width, height)
        )
        log(f"✅ Capture enregistrée sous {image_path}")

        # Partie coordonnées (reste identique)
        coins = {
            "Coin supérieur gauche": (left, top),
            "Coin supérieur droit": (left + width, top),
            "Coin inférieur droit": (left + width, top + height),
            "Coin inférieur gauche": (left, top + height)
        }

        coord_zone = (1719, 984, 192, 32)
        coords_resultats = []

        for nom, (x, y) in coins.items():
            log(f"Déplacement vers {nom} ({x}, {y})")
            pyautogui.moveTo(x, y, duration=1)
            time.sleep(1)

            screenshot_coord = pyautogui.screenshot(region=coord_zone)
            coord_text = pytesseract.image_to_string(screenshot_coord).strip()
            log(f"{nom} → Coordonnées détectées : {coord_text}")

            coords_resultats.append({"coin": nom, "coordonnees": coord_text})

        with open("output/coordonnees_coins.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["coin", "coordonnees"])
            writer.writeheader()
            writer.writerows(coords_resultats)
        log("💾 Coordonnées sauvegardées dans output/coordonnees_coins.csv")

        with open("output/coordonnees_coins.json", "w", encoding="utf-8") as f:
            json.dump(coords_resultats, f, indent=4, ensure_ascii=False)
        log("💾 Coordonnées sauvegardées dans output/coordonnees_coins.json")

        return image_path

    except Exception as e:
        log(f"❌ Erreur : {e}")
        return None

    finally:
        log("Fermeture du navigateur")
        driver.quit()
        log("Script terminé.")


if __name__ == "__main__":
    run("Ouarzazate")