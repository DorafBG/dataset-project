import pandas as pd
import os
import json

# Chemins des fichiers (relatifs au script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "fichier_final.csv")
SCHEMA_FILE = os.path.join(SCRIPT_DIR, "schema", "tableSchema.JSON")


def verifier_conformite_schema(file_path, schema_path):
    """
    Vérifie la conformité d'un fichier CSV par rapport à un schéma JSON.
    Retourne une liste d'erreurs (vide si conforme).
    """
    if not os.path.exists(schema_path):
        return [f"Erreur : Le schéma '{schema_path}' est introuvable"]
    
    if not os.path.exists(file_path):
        return [f"Erreur : Le fichier '{file_path}' est introuvable"]
    
    # Charger le schéma JSON
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)
    
    # Charger le CSV
    df = pd.read_csv(file_path)
    erreurs = []

    # Vérifier chaque champ du schéma
    for field in schema['fields']:
        col = field['name']
        constraints = field.get('constraints', {})
        
        # Vérifier présence de la colonne
        if col not in df.columns:
            erreurs.append(f"Colonne manquante : '{col}'")
            continue

        # Vérifier les valeurs requises
        if constraints.get('required') and df[col].isnull().any():
            erreurs.append(f"Valeurs manquantes dans '{col}'")

        # Vérifier l'unicité
        if constraints.get('unique') and df[col].duplicated().any():
            erreurs.append(f"Doublons dans '{col}'")

        # Vérifier les patterns pour les strings
        if field['type'] == 'string' and 'pattern' in constraints:
            masque_invalide = ~df[col].astype(str).str.match(constraints['pattern'], na=True)
            if masque_invalide.any():
                erreurs.append(f"Format incorrect pour '{col}' (pattern attendu: {constraints['pattern']})")

        # Vérifier les types numériques
        elif field['type'] == 'number' and not pd.api.types.is_numeric_dtype(df[col]):
            erreurs.append(f"La colonne '{col}' doit être numérique")

    return erreurs


def main():
    print("Chargement des fichiers nettoyés...")
    
    # Lecture avec pandas
    df_salaire = pd.read_csv(os.path.join(OUTPUT_DIR, "europa_SalaireMedianParNiveaudEducation_cleaned.csv"))
    df_transition = pd.read_csv(os.path.join(OUTPUT_DIR, "eurostat_transition_cleaned.csv"))
    df_ppp = pd.read_csv(os.path.join(OUTPUT_DIR,"oecd_ppp_cleaned.csv"))
    df_pisa = pd.read_csv(os.path.join(OUTPUT_DIR,"pisa_cleaned.csv"))
    
    print(f"Salaires : {len(df_salaire)} lignes")
    print(f"Transition : {len(df_transition)} lignes")
    print(f"PPP : {len(df_ppp)} lignes")
    print(f"PISA : {len(df_pisa)} lignes")

    # Agrégation des différents dataframes
    print("\nFusion des dataframes...")
    final = df_salaire.merge(df_transition, on=['code_pays', 'pays'], how='outer')
    final = final.merge(df_ppp, on=['code_pays', 'pays'], how='outer')
    final = final.merge(df_pisa, on=['code_pays', 'pays'], how='outer')
    
    print(f"Dataset final : {len(final)} lignes, {len(final.columns)} colonnes")

    # Sauvegarder le fichier nettoyé
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

    print(f"\nFichier final sauvegardé : {OUTPUT_FILE}")

    # Vérification de conformité du fichier genere avec le schema
    print("\n=== Vérification de conformité avec le schéma ===")
    erreurs = verifier_conformite_schema(OUTPUT_FILE, SCHEMA_FILE)
    
    if not erreurs:
        print("Le fichier est conforme au schéma.")
    else:
        print(f"⚠ {len(erreurs)} erreur(s) de conformité détectée(s) :")
        for erreur in erreurs:
            print(f"  - {erreur}")
        print("\n⚠ ATTENTION : Le fichier généré ne respecte pas le schéma défini.")
    

    print(f"\nPipeline terminé avec succès.")

if __name__ == "__main__":
    main()