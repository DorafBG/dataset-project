import pandas as pd
from utils import EUROPEAN_COUNTRIES_ISO3, ISO3_TO_ISO2
import os

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "2023_oecd_PPP.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "oecd_ppp_cleaned.csv")


def main():
    print("Chargement des données PPP...")
    df = pd.read_csv(RAW_FILE)
    
    print(f"Données brutes : {len(df)} lignes")
    print(f"Colonnes disponibles : {list(df.columns)}")
    
    # 1. Filtrage sur pays européens
    print("\nÉtape 1: Filtrage des pays européens...")
    df_filtered = df[df['REF_AREA'].isin(EUROPEAN_COUNTRIES_ISO3)].copy()
    
    print(f"Après filtrage : {len(df_filtered)} lignes")
    
    # 2. Sélection des colonnes utiles uniquement
    print("\nÉtape 2: Sélection des colonnes...")
    df_cleaned = df_filtered[['REF_AREA', 'Zone de référence', 'OBS_VALUE']].copy()
    
    # Renommage pour clarifier
    df_cleaned.columns = ['country_code', 'country_name', 'ppp_value']
    
    # 3. Conversion ISO3 vers ISO2
    print("\nÉtape 3: Conversion des codes pays ISO3 vers ISO2...")
    df_cleaned['country_code'] = df_cleaned['country_code'].map(ISO3_TO_ISO2)
    
    print(f"Codes convertis : {df_cleaned['country_code'].unique()[:10]}...")
    
    # 4. Tri par code pays
    df_cleaned = df_cleaned.sort_values('country_code').reset_index(drop=True)
    
    print(f"\nNombre de pays dans le dataset final : {len(df_cleaned)}")

    df_cleaned.rename(columns={'country_code': 'code_pays', 'country_name': 'pays'}, inplace=True)
    print(df_cleaned)
    # 5. Sauvegarder le fichier nettoyé
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_cleaned.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    print(f"\n✓ Fichier nettoyé sauvegardé : {OUTPUT_FILE}")
if __name__ == "__main__":
    main()