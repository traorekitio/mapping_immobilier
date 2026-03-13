import streamlit as st
import take_capture
import scrap_googleMaps
import clean_hotels
import plot_map
import pandas as pd
import os

# Créer le dossier output s'il n'existe pas
os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="Cartographie des Hôtels", layout="wide")

st.title("Projet de Cartographie des Points d'Intérêt")

# Étape 1 : choix de la zone
st.header("1️Définir la zone d'étude")
zone = st.text_input("Entrez une zone (ex: Ouarzazate, Rabat...)", "Ouarzazate")

if st.button("Capturer la zone sur Google Earth") and zone:
    image_path = take_capture.run(zone)   
    if image_path:
        st.session_state["capture_image"] = image_path  
        st.success(f"✅ Capture effectuée pour {zone}")
    else:
        st.error("❌ Erreur lors de la capture.")

if "capture_image" in st.session_state:
    st.subheader("Carte capturée")
    st.image(st.session_state["capture_image"], caption=f"Carte capturée : {zone}")

    with open(st.session_state["capture_image"], "rb") as f:
        st.download_button("Télécharger la capture", f, file_name="capture_epure.png")


# Étape 2 : scraping
st.header("Récupérer les données Google Maps")
requete = st.text_input("Requête de recherche Google Maps :", f"hôtels {zone}")

if st.button("🔍 Lancer le scraping") and requete:
    csv_path = scrap_googleMaps.run(requete)
    if csv_path:
        st.session_state["scraped_csv"] = csv_path  
        st.success("✅ Scraping terminé, données enregistrées dans output/donnees.csv")
    else:
        st.error("❌ Erreur lors du scraping.")

if "scraped_csv" in st.session_state:
    csv_path = st.session_state["scraped_csv"]
    df = pd.read_csv(csv_path)

    st.subheader("Aperçu des données collectées")
    st.dataframe(df.head(10))

    with open(csv_path, "r", encoding="utf-8") as f:
        st.download_button("Télécharger les données", f, file_name="donnees.csv")


# Étape 3 : Nettoyage / filtre
st.header("Filtrer les résultats")
critere = st.selectbox("Critère de filtre", ["classe", "prix"])
comparaison = st.selectbox("Comparaison", [">", ">=", "<", "<=", "=="])
seuil = st.number_input("Seuil numérique (étoiles ou prix)", value=2)

if st.button("🧹 Appliquer le filtre"):
    nb_conserves = clean_hotels.clean_data("output/donnees.csv", "output/donnees_filtre.csv", critere, seuil, comparaison)
    st.session_state["filtered_csv"] = "output/donnees_filtre.csv"
    st.success(f"Filtrage terminé ! {nb_conserves} éléments conservés dans output/donnees_filtre.csv")

if "filtered_csv" in st.session_state:
    filtered_path = st.session_state["filtered_csv"]
    df_f = pd.read_csv(filtered_path)

    st.subheader("Aperçu des données filtrées")
    st.write(f"Nombre total de lignes : {len(df_f)}")
    st.dataframe(df_f.head(10))

    with open(filtered_path, "r", encoding="utf-8") as f:
        st.download_button("Télécharger les données filtrées", f, file_name="donnees_filtre.csv")


# Étape 4 : Génération de la carte finale
st.header("Générer la carte et la légende")
if st.button("Créer la carte"):
    plot_map.run()
    st.session_state["map_image"] = "output/donnees_map.png"   
    st.session_state["map_legend"] = "output/legende.json"     
    st.success("Carte générée avec succès !")

if "map_image" in st.session_state:
    st.subheader("Carte générée")
    st.image(st.session_state["map_image"], caption="Carte générée")

    with open(st.session_state["map_image"], "rb") as f:
        st.download_button("Télécharger la carte", f, file_name="donnees_map.png")

    if "map_legend" in st.session_state:
        with open(st.session_state["map_legend"], "r", encoding="utf-8") as f:
            st.download_button("Télécharger la légende (JSON)", f, file_name="legende.json")


st.info("Pipeline complète prête à être utilisée !")