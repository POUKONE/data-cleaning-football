import pandas as pd
import numpy as np
import re

print("Début du script de nettoyage...")

#Chargeons les données 
file_path = 'merged_players.csv'
try:
    df = pd.read_csv(file_path)
    print(f"Fichier '{file_path}' chargé. {len(df)} lignes trouvées.")
except FileNotFoundError:
    print(f"ERREUR : Le fichier '{file_path}' n'a pas été trouvé.")

#Nettoyons 'Height' (Taille)
#Fonction pour convertir le format "X'Y"" en centimètres
def convert_height_to_cm(height_str):
    if pd.isna(height_str):
        return np.nan
    try:
        #Utilisons re.findall pour trouver les pieds et les pouces
        parts = re.findall(r"(\d+)'(\d+)\"", height_str)
        if parts:
            feet = int(parts[0][0])
            inches = int(parts[0][1])
            total_cm = (feet * 30.48) + (inches * 2.54)
            return round(total_cm)
    except:
        return np.nan #Retourne NaN si le format est inattendu
    return np.nan #Retourne NaN si aucun motif n'est trouvé

#Appliquons la fonction et créer une nouvelle colonne
df['Height (cm)'] = df['Height'].apply(convert_height_to_cm)
print("Colonne 'Height (cm)' créée.")

#Nettoyeons 'Weight' Poids
#Nous allons remplacer kg par rien et convertir en nombre
# errors='coerce' transformera tout ce qui n'est pas un nombre en NaN (valeur nulle)
df['Weight (kg)'] = pd.to_numeric(df['Weight'].str.replace(' kg', ''), errors='coerce')
print("Colonne 'Weight (kg)' créée.")

#Nettoyons 'Transfer Value'
#Remplaçons "Not for Sale" par NaN
#Remplaçons "$" par rien
df['Transfer Value (num)'] = df['Transfer Value'].replace('Not for Sale', np.nan)
df['Transfer Value (num)'] = df['Transfer Value (num)'].str.replace('$', '', regex=False)
df['Transfer Value (num)'] = pd.to_numeric(df['Transfer Value (num)'], errors='coerce')
#Remplissons les NaN restants par 0
df['Transfer Value (num)'] = df['Transfer Value (num)'].fillna(0)
print("Colonne 'Transfer Value (num)' créée.")

#Nettoyons les colonnes de statistiques (Apps, Gls)
#Liste des colonnes qui contiennent des "-" au lieu de 0
stats_cols = ['AT Apps', 'AT Gls', 'AT Lge Apps', 'AT Lge Gls', 'Yth Apps', 'Yth Gls']

#Remplaçons les "-" par 0 dans ces colonnes
df[stats_cols] = df[stats_cols].replace('-', 0)

#Convertir ces colonnes en nombres (entiers)
for col in stats_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
print(f"Colonnes de statistiques ({stats_cols}) nettoyées et converties en entiers")

#Nettoyons 'DOB' (Date de naissance)
#Nous allons extraire uniquement la partie date (jj/mm/aa) avant l'espace
df['DOB_clean'] = df['DOB'].str.split(' ').str[0]
#Convertir en vrai format date
#format='%d%m%Y' indique à pandas que le format est Jour/Mois/Année
df['DOB_clean'] = pd.to_datetime(df['DOB_clean'], format='%d/%m/%Y', errors='coerce')
print("Colonne 'DOB_clean' créée.")

#Supprimons les anciennes colonnes et colonnes inutiles
#Supprimons les colonnes que nous venons de remplacer, plus la colonne d'index inutile
cols_to_drop = ['Unnamed : 0', 'Height', 'Weight', 'Transfer Value', 'DOB']
df = df.drop(columns=cols_to_drop, errors='ignore') #errors='ignore' evite un crash si la colonne n'existe pas
print(f"Colonnes inutiles ({cols_to_drop}) supprimées")

#Supprimons 'Team' qui est presque vide
df = df.drop(columns=['Team'], errors='ignore')
print("Colonne 'Team' (presque vide) supprimée")

#Sauvegardons le fichier nettoyé
output_filename = 'cleaned_players.csv'
df.to_csv(output_filename, index=False, encoding='utf-8-sig')
#index=False est crucial pour Tableau

print("\n--- Nettoyage terminé ! ---")
print(f"Un nouveau fichier a été créé : '{output_filename}'")
print("C'est ce fichier que nous allons maintenant importer dans Tableau")
print("\n--- Aperçu des données nettoyées ---")
df.info()
print(df)