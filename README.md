# Construction d’un dataset sur la reproduction sociale en Europe

But: projet visant à construire un dataset synthétique sur la reproduction sociale en Europe à partir de plusieurs sources ouvertes (possibilité d’ajouter d’autres sources ensuite).

## Objectif
Assembler et harmoniser plusieurs indicateurs liés à la mobilité/reproduction sociale (résultats scolaires et lien intergénérationnel) pour un jeu de données comparatif par pays européens.

## Sources de données (préliminaire)
- Classement PISA 2025 (niveau d'études / performance scolaire) — filtrer sur pays européens ciblés  
    https://data-explorer.oecd.org/vis?pg=0&bp=true&snb=7&tm=PISA&vw=tb&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_GOV_INT%40DF_GOV_SPS_2025&df[ag]=OECD.GOV.GIP&df[vs]=1.0&dq=A.......&pd=2012%2C&to[TIME_PERIOD]=false
- Réussite au baccalauréat en France selon l’origine sociale (données par origine sociale)  
    https://www.data.gouv.fr/datasets/reussite-au-baccalaureat-selon-lorigine-sociale/
- Réussite au GCSE (Royaume‑Uni) en fonction du FSM (Free School Meals — proxy d'origine sociale)  
    https://explore-education-statistics.service.gov.uk/find-statistics/key-stage-4-performance/2024-25#explore-data-and-files
- Pourcentage de la réussite scolaire par rapport à celle des parents (Eurostat, indicateur intergénérationnel) — filtrer par pays européens  
    https://ec.europa.eu/eurostat/databrowser/view/ilc_igtp01/default/table

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