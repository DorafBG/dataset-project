import pandas as pd
import os

# Le script cherche le fichier dans le même dossier que lui
dossier_actuel = os.path.dirname(os.path.abspath(__file__))
nom_fichier = "fichier_faux.csv"
chemin_csv = os.path.join(dossier_actuel, nom_fichier)

def verifier_csv(file_path, schema):
    if not os.path.exists(file_path):
        return [f"Erreur : Le fichier '{nom_fichier}' est introuvable dans {dossier_actuel}"]
    
    df = pd.read_csv(file_path)
    erreurs = []

    for field in schema['fields']:
        col = field['name']
        constraints = field.get('constraints', {})
        
        if col not in df.columns:
            erreurs.append(f"Colonne manquante : '{col}'")
            continue

        if constraints.get('required') and df[col].isnull().any():
            erreurs.append(f"Valeurs manquantes dans '{col}'")

        if constraints.get('unique') and df[col].duplicated().any():
            erreurs.append(f"Doublons dans '{col}'")

        if field['type'] == 'string' and 'pattern' in constraints:
            masque_invalide = ~df[col].astype(str).str.match(constraints['pattern'], na=True)
            if masque_invalide.any():
                erreurs.append(f"Format incorrect pour '{col}'")

        elif field['type'] == 'number' and not pd.api.types.is_numeric_dtype(df[col]):
            erreurs.append(f"La colonne '{col}' doit etre numerique")

    return erreurs

try:
    # Lecture pour generer le schema dynamiquement
    df_temp = pd.read_csv(chemin_csv)
    
    schema_donnees = {
      "fields": [
        {"name": "code_pays", "type": "string", "constraints": {"required": True, "pattern": "^[A-Z]{2}$"}},
        {"name": "pays", "type": "string", "constraints": {"required": True, "unique": True}},
        *([{"name": c, "type": "number", "constraints": {"required": False}} 
           for c in df_temp.columns if c not in ['code_pays', 'pays']])
      ]
    }

    resultats = verifier_csv(chemin_csv, schema_donnees)

    if not resultats:
        print(f"Succes : {nom_fichier} est conforme.")
    else:
        print(f"{len(resultats)} erreur(s) trouvee(s) :")
        for e in resultats:
            print(e)

except FileNotFoundError:
    print(f"Erreur : Placez '{nom_fichier}' dans le dossier : {dossier_actuel}")
except Exception as e:
    print(f"Erreur : {e}")