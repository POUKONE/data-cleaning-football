# Script de Nettoyage de Données de Football (ETL)

Ce projet contient un script Python conçu pour nettoyer et standardiser un jeu de données de joueurs de football (`merged_players.csv`). L'objectif principal est de préparer les données pour une analyse et une visualisation dans des outils comme Tableau ou PowerBI.

## Fonctionnalités

Le script effectue les opérations de nettoyage suivantes :

* **Conversion de la taille :** Transformation du format impérial (pieds/pouces, ex: 6'2") vers le système métrique (cm).
* **Nettoyage du poids :** Suppression des unités textuelles (kg) pour conversion numérique.
* **Traitement financier :** Nettoyage de la colonne 'Transfer Value' (suppression des symboles monétaires, gestion des mentions "Not for Sale").
* **Standardisation des statistiques :** Remplacement des valeurs manquantes (indiquées par "-") par 0 et conversion en nombres entiers pour les matchs et les buts.
* **Formatage des dates :** Extraction et conversion des dates de naissance (DOB) au format standard (datetime).
* **Suppression de colonnes :** Retrait des colonnes brutes obsolètes et des colonnes vides.

## Prérequis

Pour exécuter ce script, vous devez avoir Python installé ainsi que les bibliothèques suivantes :

* pandas
* numpy

Vous pouvez installer les dépendances via pip :

```bash
pip install pandas numpy
