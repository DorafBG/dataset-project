import pandas as pd
import os

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "2019_2023_europa_transition_of_educational_attainment_level_europa_eu_ilc_igtp01.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "eurostat_transition_cleaned.csv")

# Liste des pays européens à garder (codes ISO2)
EUROPEAN_COUNTRIES = [
    'AL', 'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 
    'FI', 'FR', 'HR', 'HU', 'IE', 'IS', 'IT', 'LT', 'LU', 'LV', 'ME', 'MK', 
    'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'RS', 'SE', 'SI', 'SK', 'TR', 'UK', 'XK'
]

def main():
    print("Chargement des données...")
    df = pd.read_csv(RAW_FILE)
    
    print(f"Données brutes : {len(df)} lignes")
    
    # 1. Filtrage sur sex='T' (Total) et pays européens
    print("\nÉtape 1: Filtrage sex='T' et pays européens...")
    df_filtered = df[
        (df['sex'] == 'T') & 
        (df['geo'].isin(EUROPEAN_COUNTRIES))
    ].copy()
    
    print(f"Après filtrage : {len(df_filtered)} lignes")
    
    # 2. Sélection des colonnes utiles
    df_filtered = df_filtered[[
        'geo', 'Geopolitical entity (reporting)', 
        'TIME_PERIOD', 'trans1g', 'isced11', 'OBS_VALUE'
    ]]
    
    # Renommage pour simplifier
    df_filtered.columns = ['country_code', 'country_name', 'year', 'origin_level', 'destination_level', 'value']
    
    # 3. Séparer les données 2019 et 2023
    print("\nÉtape 2: Séparation des données 2019 et 2023...")
    df_2019 = df_filtered[df_filtered['year'] == 2019].copy()
    df_2023 = df_filtered[df_filtered['year'] == 2023].copy()
    
    print(f"Données 2019 : {len(df_2019)} lignes")
    print(f"Données 2023 : {len(df_2023)} lignes")
    
    # 4. Création des noms de colonnes pour le pivot
    print("\nÉtape 3: Pivot des données...")
    
    # Simplifier les codes origin et destination
    origin_map = {
        'FED0-2': '0-2',
        'FED3_4': '3-4', 
        'FED5_6': '5-6', 
        'FED5_8': '5-8', 
    }
    
    dest_map = {
        'ED0-2': '0-2',
        'ED3_4': '3-4',
        'ED5-8': '5-8'
    }
    
    # Appliquer les mappings pour 2019 et 2023
    for df_temp in [df_2019, df_2023]:
        df_temp['origin_simple'] = df_temp['origin_level'].map(origin_map)
        df_temp['dest_simple'] = df_temp['destination_level'].map(dest_map)
        df_temp['column_name'] = 'From_' + df_temp['origin_simple'] + '_To_' + df_temp['dest_simple']
    
    # 5. Pivoter les données séparément
    df_pivot_2019 = df_2019.pivot_table(
        index=['country_code', 'country_name'],
        columns='column_name',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    df_pivot_2023 = df_2023.pivot_table(
        index=['country_code', 'country_name'],
        columns='column_name',
        values='value',
        aggfunc='first'
    ).reset_index()
    
    # Aplatir les noms de colonnes
    df_pivot_2019.columns.name = None
    df_pivot_2023.columns.name = None
    
    print(f"Pays avec données 2019 : {len(df_pivot_2019)}")
    print(f"Pays avec données 2023 : {len(df_pivot_2023)}")
    
    # 6. Fusionner et compléter les données manquantes
    print("\nÉtape 4: Fusion et complétion des données...")
    
    # Merger les deux datasets
    df_merged = df_pivot_2023.merge(
        df_pivot_2019, 
        on=['country_code', 'country_name'], 
        how='outer',
        suffixes=('', '_2019')
    )
    
    # Liste des colonnes de données (excluant country_code et country_name)
    data_columns = [col for col in df_pivot_2023.columns if col not in ['country_code', 'country_name']]
    
    # Pour chaque colonne de données, compléter avec 2019 si 2023 est manquant
    for col in data_columns:
        col_2019 = col + '_2019'
        if col_2019 in df_merged.columns:
            # Identifier où 2023 est manquant
            mask_missing = df_merged[col].isna()
            # Compléter avec 2019
            df_merged.loc[mask_missing, col] = df_merged.loc[mask_missing, col_2019]
    
    # Supprimer les colonnes _2019
    df_merged = df_merged[[col for col in df_merged.columns if not col.endswith('_2019')]]
    
    df_pivot = df_merged
    
    print(f"\nNombre de pays dans le dataset final : {len(df_pivot)}")
    print(f"Colonnes créées : {list(df_pivot.columns)}")
    
    # 7. Sauvegarder le fichier nettoyé
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_pivot.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    print(f"\n✓ Fichier nettoyé sauvegardé : {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
