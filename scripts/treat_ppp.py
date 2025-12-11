import pandas as pd
import os

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "2023_oecd_PPP.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "oecd_ppp_cleaned.csv")

# Liste des pays européens à garder (codes ISO3)
EUROPEAN_COUNTRIES = [
    'ALB', 'AUT', 'BEL', 'BGR', 'BIH', 'HRV', 'CYP', 'CZE', 'DNK', 'EST', 
    'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA', 'LVA', 'LTU', 
    'LUX', 'MLT', 'MNE', 'MKD', 'NLD', 'NOR', 'POL', 'PRT', 'ROU', 'SRB', 
    'SVK', 'SVN', 'ESP', 'SWE', 'CHE', 'TUR', 'GBR'
]

# Mapping ISO3 vers ISO2 pour les pays européens
ISO3_TO_ISO2 = {
    'ALB': 'AL', 'AUT': 'AT', 'BEL': 'BE', 'BGR': 'BG', 'BIH': 'BA', 
    'HRV': 'HR', 'CYP': 'CY', 'CZE': 'CZ', 'DNK': 'DK', 'EST': 'EE',
    'FIN': 'FI', 'FRA': 'FR', 'DEU': 'DE', 'GRC': 'EL', 'HUN': 'HU',
    'ISL': 'IS', 'IRL': 'IE', 'ITA': 'IT', 'LVA': 'LV', 'LTU': 'LT',
    'LUX': 'LU', 'MLT': 'MT', 'MNE': 'ME', 'MKD': 'MK', 'NLD': 'NL',
    'NOR': 'NO', 'POL': 'PL', 'PRT': 'PT', 'ROU': 'RO', 'SRB': 'RS',
    'SVK': 'SK', 'SVN': 'SI', 'ESP': 'ES', 'SWE': 'SE', 'CHE': 'CH',
    'TUR': 'TR', 'GBR': 'UK'
}

def main():
    print("Chargement des données PPP...")
    df = pd.read_csv(RAW_FILE)
    
    print(f"Données brutes : {len(df)} lignes")
    print(f"Colonnes disponibles : {list(df.columns)}")
    
    # 1. Filtrage sur pays européens
    print("\nÉtape 1: Filtrage des pays européens...")
    df_filtered = df[df['REF_AREA'].isin(EUROPEAN_COUNTRIES)].copy()
    
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
    
    # 5. Sauvegarder le fichier nettoyé
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_cleaned.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    print(f"\n✓ Fichier nettoyé sauvegardé : {OUTPUT_FILE}")
if __name__ == "__main__":
    main()