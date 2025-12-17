# python
import pandas as pd
import numpy as np
from utils import EUROPEAN_COUNTRIES, EN_TO_FR
import os

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw",
                        "2023_europa_SalaireMedianParNiveauEducation.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "2023_europa_SalaireMedianParNiveaudEducation_cleaned.csv")


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
        'isced11', 'OBS_VALUE'
    ]]

    # Renommage pour simplifier
    df_filtered.columns = ['code_pays', 'pays', 'education_level', 'value']

    # Appliquer la traduction sur la colonne country_name du DataFrame final
    df_filtered['pays'] = (
        df_filtered['pays']
        .astype(str)
        .str.strip()
        .map(EN_TO_FR)
        .fillna(df_filtered['pays'])
    )


    # Convertir la valeur en numérique (au cas où elle serait en string)
    df_filtered['value'] = pd.to_numeric(df_filtered['value'], errors='coerce')

    # Normaliser les étiquettes d'éducation (prendre en compte underscore ou tiret)
    df_filtered['education_level'] = df_filtered['education_level'].astype(str).str.replace('_', '-', regex=False)

    # Pivot: une ligne par pays, colonnes pour chaque niveau d'éducation
    print("\nÉtape 3: Pivot des données...")
    df_pivot = df_filtered.pivot_table(
        index=['code_pays', 'pays'],
        columns='education_level',
        values='value',
        aggfunc='first'
    ).reset_index()

    # Aplatir les noms de colonnes
    df_pivot.columns.name = None

    # Renommer les colonnes pour obtenir les noms demandés
    col_map = {
        'ED0-2': 'salary_median_ED0-2',
        'ED3-4': 'salary_median_ED3-4',
        'ED5-8': 'salary_median_ED5-8'
    }
    # Appliquer le renommage là où les colonnes existent
    df_pivot = df_pivot.rename(columns={k: v for k, v in col_map.items() if k in df_pivot.columns})

    # S'assurer que les trois colonnes existent (même si certaines valeurs manquent)
    for target in ['salary_median_ED0-2', 'salary_median_ED3-4', 'salary_median_ED5-8']:
        if target not in df_pivot.columns:
            df_pivot[target] = pd.NA

    # Réordonner les colonnes: code_pays, pays, puis les 3 salaires
    final_columns = ['code_pays', 'pays', 'salary_median_ED0-2', 'salary_median_ED3-4', 'salary_median_ED5-8']
    df_final = df_pivot[final_columns]

    # Calcul de l'indicateur (salaire 5-8 - salaire 0-2) / salaire 5-8
    # Gestion des divisions par zéro et des valeurs manquantes
    df_final['salary_gap_ED5-8_vs_ED0-2'] = (
        df_final['salary_median_ED5-8'] - df_final['salary_median_ED0-2']
    ) / df_final['salary_median_ED5-8']

    # Remplacer infinis résultant de division par zéro par NA
    df_final['salary_gap_ED5-8_vs_ED0-2'] = df_final['salary_gap_ED5-8_vs_ED0-2'].replace([np.inf, -np.inf], pd.NA)

    # Si désiré, forcer NA quand dénominateur est nul ou manquant
    denom_zero_mask = df_final['salary_median_ED5-8'].fillna(0) == 0
    df_final.loc[denom_zero_mask, 'salary_gap_ED5-8_vs_ED0-2'] = pd.NA

    # Ajouter la nouvelle colonne à l'ordre final des colonnes
    final_columns.append('salary_gap_ED5-8_vs_ED0-2')
    df_final = df_final[final_columns]

    print(f"\nNombre de pays dans le dataset final : {len(df_final)}")
    print(f"Colonnes créées : {list(df_final.columns)}")

    print(df_final.head())

    # Sauvegarder le fichier nettoyé
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print(f"\n✓ Fichier nettoyé sauvegardé : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
