# 🗺️ Mapping Immobilier - Cartographie des Hôtels au Maroc

Application interactive pour capturer, scraper et visualiser les hôtels sur une carte géographique à partir de Google Maps et Google Earth.

## 📋 Fonctionnalités

- 📸 **Capture Google Earth** : Capture automatique de zones géographiques
- 🔍 **Scraping Google Maps** : Extraction des données hôtelières (nom, localisation, prix, étoiles)
- 🧹 **Filtrage des données** : Filtrer par classe, prix ou autres critères
- 🗺️ **Visualisation cartographique** : Génération de cartes avec légende JSON

## 🛠️ Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Navigateur web (pour Streamlit)

## 📦 Installation

1. **Clone le repo** :
```bash
git clone https://github.com/traorekitio/mapping_immobilier.git
cd mapping_immobilier
```

2. **Crée un environnement virtuel** (recommandé) :
```bash
python -m venv venv
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate
```

3. **Installe les dépendances** :
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation

Lance l'application Streamlit :

```bash
streamlit run app.py
```

L'app s'ouvrira automatiquement dans ton navigateur à `http://localhost:8501`

## 📝 Étapes du pipeline

### 1️⃣ Définir la zone d'étude
- Rentre une zone (ex: Ouarzazate, Rabat, Fès)
- Clique sur "Capturer la zone sur Google Earth"
- Télécharge l'image capturée

### 2️⃣ Récupérer les données Google Maps
- Rentre une requête de recherche (ex: "hôtels Ouarzazate")
- Clique sur "🔍 Lancer le scraping"
- Les données sont sauvegardées dans `output/donnees.csv`
- Aperçu et téléchargement disponibles

### 3️⃣ Filtrer les résultats
- Choisis un critère : **classe** (étoiles) ou **prix**
- Sélectionne une comparaison : `>`, `>=`, `<`, `<=`, `==`
- Rentre un seuil numérique
- Clique sur "🧹 Appliquer le filtre"
- Résultat dans `output/donnees_filtre.csv`

### 4️⃣ Générer la carte finale
- Clique sur "Créer la carte"
- La carte et la légende sont générées
- Télécharge la carte (`donnees_map.png`) et la légende (`legende.json`)

## 📂 Structure du projet

```
mapping_immobilier/
├── app.py                    # Application principale Streamlit
├── take_capture.py           # Module de capture Google Earth
├── scrap_googleMaps.py       # Module de scraping Google Maps
├── clean_hotels.py           # Module de filtrage des données
├── plot_map.py               # Module de génération de cartes
├── requirements.txt          # Dépendances Python
├── .gitignore                # Fichiers à ignorer dans git
├── README.md                 # Ce fichier
└── output/                   # Dossier de sortie (créé automatiquement)
    ├── donnees.csv           # Données brutes scrapées
    ├── donnees_filtre.csv    # Données filtrées
    ├── donnees_map.png       # Carte générée
    └── legende.json          # Légende au format JSON
```

## 🔧 Modules

- **`take_capture.py`** : Capture de zones géographiques via Google Earth
- **`scrap_googleMaps.py`** : Extraction de données depuis Google Maps
- **`clean_hotels.py`** : Nettoyage et filtrage des données
- **`plot_map.py`** : Création et visualisation de cartes géographiques

## 📋 Fichiers de sortie

- `donnees.csv` : Données brutes (nom, localisation, prix, étoiles, etc.)
- `donnees_filtre.csv` : Données après filtrage
- `donnees_map.png` : Image de la carte avec les points d'intérêt
- `legende.json` : Légende en format JSON

## 💡 Exemple d'utilisation

1. Cherche les hôtels à Marrakech avec au moins 4 étoiles
2. Scrape les données depuis Google Maps
3. Filtre pour garder seulement les hôtels avec 4+ étoiles
4. Génère la carte finale
5. Télécharge la carte et les données

## 🐛 Troubleshooting

Si l'app ne démarre pas :
```bash
# Réinstalle les dépendances
pip install --upgrade -r requirements.txt

# Ou redémarre l'environnement virtuel
deactivate
venv\Scripts\activate
streamlit run app.py
```

## 📝 Licence

Ce projet est ouvert pour usage personnel et éducatif.

## 👤 Auteur

Mounira - PFE (Projet de Fin d'Études)

---

**Besoin d'aide ?** Crée une issue sur GitHub ou contacte le développeur.
