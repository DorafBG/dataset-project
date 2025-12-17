import pandas as pd
import os

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fichier_final.csv")

#Lecture avec pandas
df_salaire = pd.read_csv(os.path.join(OUTPUT_DIR, "2023_europa_salaireMedianParNiveaudEducation_cleaned.csv"))
df_transition = pd.read_csv(os.path.join(OUTPUT_DIR, "eurostat_transition_cleaned.csv"))
df_ppp = pd.read_csv(os.path.join(OUTPUT_DIR,"oecd_ppp_cleaned.csv"))
df_pisa = pd.read_csv(os.path.join(OUTPUT_DIR,"pisa_cleaned.csv"))

#Réduction dimentionnelle, faite dans les différentes fichers de traitement


#Vérification de conformité avec le schema


#Conversion des types de données non conformes


#Agrégation des différents dataframes
final = df_salaire.merge(df_transition, on=['code_pays', 'pays'], how='outer')
final = final.merge(df_ppp, on=['code_pays', 'pays'], how='outer')
final = final.merge(df_pisa, on=['code_pays', 'pays'], how='outer')


#Sauvegarder le fichier nettoyé
os.makedirs(OUTPUT_DIR, exist_ok=True)
final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"\n✓ Fichier nettoyé sauvegardé : {OUTPUT_FILE}")
