from nettoyage import treat_europa_transition
from nettoyage import treat_ppp
from nettoyage import treat_PISA
from nettoyage import treat_SalaireMedianParNiveauEducation

def main():
    treat_europa_transition.main()
    treat_ppp.main()
    treat_PISA.main()
    treat_SalaireMedianParNiveauEducation.main()
    print("\n✓ Tous les scripts de traitement des données ont été exécutés avec succès.")

if __name__ == "__main__":
    main()