import pandas as pd
from utils import EUROPEAN_COUNTRIES_ISO3, ISO3_TO_ISO2
import os

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_FILE = os.path.join(PROJECT_ROOT, "data", "raw", "2022_oecd_pisa.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "pisa_cleaned.csv")


def main():
    print("Chargement des données PISA...")
    data = pd.read_csv(RAW_FILE)
    
    print(f"Données brutes : {len(data)} lignes")
    
    # Extraire ISO3 depuis REF_AREA (déjà en ISO3 normalement)
    data['code_pays_iso3'] = data['REF_AREA'].str[:3]

    # Convertir ISO3 → ISO2 pour filtrer
    data['code_pays_iso2'] = data['code_pays_iso3'].map(ISO3_TO_ISO2)

    # Filtrer les pays européens : garder uniquement ceux présents dans le mapping
    data_europe = data[data['code_pays_iso2'].notna()].copy()
    
    print(f"Après filtrage européen : {len(data_europe)} lignes")

    # Mesures PISA d'intérêt
    measures_to_keep = ['PEE_PISA_R', 'PEE_PISA_VMSEB', 'PEE_PISA_M']
    filtered_data = data_europe[data_europe['MEASURE'].isin(measures_to_keep)].copy()
    
    print(f"Après filtrage des mesures : {len(filtered_data)} lignes")

    # Mapping des mesures
    measure_mapping = {
        'PEE_PISA_R': 'score_lecture_pisa',
        'PEE_PISA_VMSEB': 'variance_maths_pisa',
        'PEE_PISA_M': 'score_maths_pisa'
    }
    filtered_data['measure_short'] = filtered_data['MEASURE'].map(measure_mapping)

    # Pivot table : 1 pays = 1 ligne
    pivot_data = filtered_data.pivot_table(
        index=['code_pays_iso2', 'Zone de référence'],
        columns='measure_short',
        values='OBS_VALUE',
        aggfunc='first'
    ).reset_index()

    pivot_data.columns.name = None

    pivot_data = pivot_data.rename(columns={
        'code_pays_iso2': 'code_pays',
        'Zone de référence': 'pays'
    })

    # Réordonner les colonnes
    columns_order = [
        'pays', 'code_pays',
        'score_maths_pisa', 'score_lecture_pisa', 'variance_maths_pisa'
    ]
    pivot_data = pivot_data[columns_order]

    pivot_data = pivot_data.sort_values('pays').reset_index(drop=True)

    # Affichage
    print("\nAperçu des données traitées :")
    print(pivot_data.head(10))
    print(f"\nNombre total de pays européens : {len(pivot_data)}")

    print("\nListe des pays européens conservés :")
    print(pivot_data[['pays', 'code_pays']].to_string(index=False))

    print("\nInformations sur les colonnes :")
    print(pivot_data.info())

    print("\nStatistiques descriptives :")
    print(pivot_data.describe())

    # Sauvegarde
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    pivot_data.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print(f"\n✓ Fichier nettoyé sauvegardé : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
