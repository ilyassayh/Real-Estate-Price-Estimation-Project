# Estimation Immobilière Avito (XGBoost)

Ce projet propose une application Streamlit permettant d'estimer le prix d'un bien immobilier à partir de données issues d'Avito.ma, en utilisant un modèle XGBoost entraîné sur des annonces réelles.

## 📊 Description du projet

- **Nettoyage des données** :
  - Suppression des doublons et des valeurs aberrantes (outliers).
  - Remplacement des valeurs manquantes.
  - Nettoyage de la colonne `price` (conversion en float, suppression du texte 'DH').
  - Traduction et encodage des noms de villes.

- **Feature engineering** :
  - Création de variables indicatrices (one-hot) pour les équipements (`Ascenseur`, `Balcon`, etc.).
  - Extraction de mots-clés du titre de l'annonce (`luxe`, `neuf`, `meublé`, `piscine`, `terrasse`).
  - Ajout du prix au mètre carré (`price_per_m2`).
  - Encodage cible pour la ville (`city_target_enc`).

- **Modélisation** :
  - Entraînement d'un modèle XGBoost pour prédire le prix.
  - Sauvegarde du modèle avec `joblib`.

- **Application Streamlit** :
  - Interface conviviale pour saisir les caractéristiques du bien.
  - Sélection de la ville, équipements, mots-clés, etc.
  - Affichage du prix estimé en temps réel.

## 🚀 Lancer l'application

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   pip install xgboost
   ```

2. **Lancer l'application Streamlit** :
   ```bash
   streamlit run app.py
   ```

3. **Utilisation** :
   - Remplissez le formulaire (ville, surface, nombre de pièces, équipements, etc.).
   - Cliquez sur "Estimer le prix" pour obtenir une estimation basée sur le modèle XGBoost.

## 📁 Fichiers importants
- `data_avito.csv` : Données d'annonces immobilières.
- `notebook_d’estimation_immobilière_XGboost.ipynb` : Notebook de préparation et d'entraînement du modèle.
- `final_modele.joblib` : Modèle XGBoost sauvegardé.
- `app.py` : Application Streamlit.
- `requirements.txt` : Dépendances Python.

## 🙏 Remerciements
Projet réalisé dans le cadre de la formation Simplon.

N'hésitez pas à contribuer ou à proposer des améliorations ! 