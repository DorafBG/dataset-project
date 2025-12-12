import pandas as pd

# Charger les données brutes OCDE PISA
data = pd.read_csv(r'C:\Louis\Cours\IIM\Ingénierie_Des_Données\Projet\dataset-project\data\raw\2022_oecd_pisa.csv')

# Mapping ISO3 → ISO2 (pays européens uniquement)
iso3_to_iso2_europe = {
    "ALB": "AL", "DEU": "DE", "AND": "AD", "AUT": "AT",
    "BEL": "BE", "BLR": "BY", "BIH": "BA", "BGR": "BG",
    "CYP": "CY", "HRV": "HR", "DNK": "DK", "ESP": "ES",
    "EST": "EE", "FIN": "FI", "FRA": "FR", "GRC": "GR",
    "HUN": "HU", "IRL": "IE", "ISL": "IS", "ITA": "IT",
    "XKX": "XK",  # Kosovo (code ISO non officiel, utilisé par OSCE/UE)
    "LVA": "LV", "LIE": "LI", "LTU": "LT", "LUX": "LU",
    "MLT": "MT", "MDA": "MD", "MNE": "ME", "NLD": "NL",
    "NOR": "NO", "POL": "PL", "PRT": "PT", "CZE": "CZ",
    "ROU": "RO", "GBR": "GB", "SRB": "RS", "SVK": "SK",
    "SVN": "SI", "SWE": "SE", "CHE": "CH", "MKD": "MK",
    "UKR": "UA", "TUR": "TR"
}

# Extraire ISO3 depuis REF_AREA (déjà en ISO3 normalement)
data['code_pays_iso3'] = data['REF_AREA'].str[:3]

# Convertir ISO3 → ISO2 pour filtrer
data['code_pays_iso2'] = data['code_pays_iso3'].map(iso3_to_iso2_europe)

# Filtrer les pays européens : garder uniquement ceux présents dans le mapping
data_europe = data[data['code_pays_iso2'].notna()].copy()

# Mesures PISA d'intérêt
measures_to_keep = ['PEE_PISA_R', 'PEE_PISA_VMSEB', 'PEE_PISA_M']
filtered_data = data_europe[data_europe['MEASURE'].isin(measures_to_keep)].copy()

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
print("Aperçu des données traitées :")
print(pivot_data.head(10))
print(f"\nNombre total de pays européens : {len(pivot_data)}")

print("\nListe des pays européens conservés :")
print(pivot_data[['pays', 'code_pays']].to_string(index=False))

print("\nInformations sur les colonnes :")
print(pivot_data.info())

print("\nStatistiques descriptives :")
print(pivot_data.describe())

# Sauvegarde
output_path = r'C:\Louis\Cours\IIM\Ingénierie_Des_Données\Projet\dataset-project\data\processed\pisa_traite.csv'
pivot_data.to_csv(output_path, index=False, encoding='utf-8')

print(f"\nDonnées sauvegardées dans : {output_path}")
