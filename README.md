# Construction d’un dataset sur la reproduction sociale en Europe

But: projet visant à construire un dataset synthétique sur la reproduction sociale en Europe à partir de plusieurs sources ouvertes (possibilité d’ajouter d’autres sources ensuite).

## Objectif
Assembler et harmoniser plusieurs indicateurs liés à la mobilité/reproduction sociale (résultats scolaires et lien intergénérationnel) pour un jeu de données comparatif par pays européens.

## Sources de données (préliminaire)
- Classement PISA 2022 (niveau d'études / performance scolaire) — filtrer sur pays européens ciblés  
    https://data-explorer.oecd.org/vis?pg=0&bp=true&snb=7&tm=PISA&vw=tb&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_GOV_INT%40DF_GOV_SPS_2025&df[ag]=OECD.GOV.GIP&df[vs]=1.0&dq=A.......&pd=2012%2C&to[TIME_PERIOD]=false **(2022_oecd_pisa.csv)**
- Pourcentage de la réussite scolaire par rapport à celle des parents (Eurostat, indicateur intergénérationnel selon les différents niveau d'éducation) 
    https://ec.europa.eu/eurostat/databrowser/view/ilc_igtp01/default/table **(2019_2023_europa_transition_of_educational_attainment_level_europa_eu_ilc_igtp01.csv.csv)**
- PPP (pouvoir d'achat) par pays d'Europe en 2023
    https://data-explorer.oecd.org/vis?fs[0]=Topic%2C1%7CEconomy%23ECO%23%7CPrices%23ECO_PRI%23&pg=20&fc=Topic&bp=true&snb=32&vw=tb&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_PPP%40DF_PPP&df[ag]=OECD.SDD.TPS&df[vs]=1.0&pd=2023%2C2023&dq=.A.PPP...OECD&to[TIME_PERIOD]=false&ly[rw]=REF_AREA **(2023_oecd_PPP.csv)**
- Salaire médian en fonction du niveau d'éducation en 2023
    https://ec.europa.eu/eurostat/databrowser/view/ilc_di08__custom_19201270/default/table **(2023_europa_salaireMedianParNiveaudEducation.csv)**


Remarque : certaines sources proposent l’export direct en CSV/Excel (voir onglet/tables pour trier et exporter).

## Méthodologie (prévue)
1. Télécharger les fichiers sources (bruts) et stocker sous data/raw/.  
2. Filtrer les séries temporelles et limiter aux pays européens d'intérêt.  
3. Harmoniser les identifiants pays (ISO2/ISO3) et les années de référence.  
4. Normaliser les indicateurs (p. ex. scores PISA, taux de réussite en %), documenter les définitions.  
5. Joindre les tables par pays × année en conservant métadonnées et provenance.  
6. Produire un fichier final data/processed/reproduction_sociale_europe.csv et un fichier de métadonnées data/processed/README_METADATA.md.  
7. Versionner les étapes de nettoyage dans scripts/ (ex : notebooks ou scripts R/Python) et enregistrer les transformations dans changelog.

## Structure
- README.md (celui-ci)  
- data/raw/ (sources originales)  
- data/processed/ (fichiers nettoyés et jeu final)  
- scripts/ (scripts de nettoyage et d'agrégation)  
- docs/ (notes méthodologiques, licences, sources)