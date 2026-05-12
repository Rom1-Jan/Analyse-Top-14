# 🏉 Analyse de la saison 2025-2026 du TOP 14

Ce projet personnel automatise le suivi et l'analyse du championnat de France de rugby via un pipeline de données **ETL** (Extract, Transform, Load) complet.

### 📝 Présentation
L'ensemble du projet est organisé pour transformer des données brutes en données exploitables :

* **Collecte** : Récupération automatisée des résultats via l'**API TheSportsDB** couplée à un **Web Scraping** (BeautifulSoup4) sur **Rugbyrama** pour obtenir le classement officiel (bonus inclus).
* **Traitement** : Nettoyage, normalisation et enrichissement des données (calculs de bilans, mapping GPS des stades) avec **Python** et **Pandas**.
* **Visualisation** : Exploitation des données raffinées dans un dashboard **Power BI** interactif.

---

## 🎯 Objectifs

- Récupérer les données de matchs via une API et du scraping web
- Stocker et structurer les données avec Python et Pandas
- Visualiser les statistiques dans un dashboard PowerBI interactif

---

## 🛠️ Stack technique

| Outil | Usage |
|-------|-------|
| Python | Collecte et traitement des données |
| Pandas | Manipulation des DataFrames |
| Requests | Appels API |
| BeautifulSoup4 | Scraping web |
| PowerBI | Dashboard de visualisation |

---

## 📁 Structure du projet

```
├──top14_data_pipeline.py       # Script principal de collecte et traitement
├── top14_data.json        # Données brutes des matchs (API TheSportsDB)
├── classements.json       # Données brutes des classements (scraping Rugbyrama)
├── top14_matches.csv      # DataFrame des matchs exporté
├── top14_teams.csv        # DataFrame des équipes exporté
├── classements.csv        # DataFrame des classements exporté
└── README.md
```

---

## 📡 Sources de données

- **[TheSportsDB API](https://www.thesportsdb.com/)** — Résultats et informations des matchs (API gratuite, clé `123`)
- **[Rugbyrama](https://www.rugbyrama.fr/)** — Classements par journée avec bonus offensifs et défensifs (scraping BeautifulSoup)

---

## ⚙️ Installation

```bash
# Cloner le repo
git clone https://github.com/Rom1-Jan/top14-analysis.git
cd top14-analysis

# Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate.bat  # Windows
source venv/bin/activate    # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt
```

---

## ⚙️ Utilisation

1.  **Mise à jour des données :**
    Exécutez le script Python pour rafraîchir les fichiers sources avec les derniers scores :
    ```bash
    python top14_data_pipeline.py
    ```

2.  **Actualisation du Dashboard :**
    Ouvrez le fichier Power BI et cliquez sur le bouton **Actualiser** dans le ruban Accueil pour intégrer les nouvelles données.

---

## 📈 Dashboard PowerBI

Le dashboard permet de :

- Filtrer par équipe et par journée
- Visualiser le taux de victoire domicile / extérieur
- Consulter les résultats et le classement par journée
- Comparer les points marqués et encaissés par équipe
- Localiser les stades sur une carte interactive

---

## 🔮 Prochaines étapes

- Migration vers PostgreSQL
- Ajout d'un modèle Machine Learning (scikit-learn) pour prédire les résultats
- Déploiement du dashboard via Streamlit

---

## 👤 Auteur

**Romain Janoueix** — Étudiant BUT Informatique spécialisation Data