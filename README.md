# Éducation en Afrique — Projet Capstone Data Analytics

Analyse des indicateurs de développement liés à l'éducation (alphabétisation, scolarisation, dépenses publiques) pour les 54 pays d'Afrique, inspirée des World Development Indicators (WDI) de la Banque Mondiale. Projet réalisé dans le cadre d'un stage — cycle complet : collecte → nettoyage → analyse → visualisation (Power BI) → restitution.

## Contenu du dépôt

| Fichier | Description |
|---|---|
| `Africa_Education_Dataset.xlsx` | Jeu de données nettoyé (source pour Power BI) — onglets `Data`, `Data_Dictionary`, `Region_Summary`, `Cleaning_Log` |
| `Visusalisations.pbix` | Tableau de bord Power BI interactif (3 pages) |
| `Rapport_Final_Education_Afrique.pdf` | Rapport final : objectif, dataset, nettoyage, méthodologie, résultats, insights, recommandations |


## Aperçu du tableau de bord

**Page 1 — Vue d'ensemble** : 5 cartes KPI, alphabétisation moyenne par région, répartition des pays par catégorie d'alphabétisation.
**Page 2 — Alphabétisation et genre** : comparaison hommes/femmes par pays, écart de genre par région, table détaillée.
**Page 3 — Investissement et richesse** : dépenses d'éducation vs alphabétisation, PIB par habitant vs alphabétisation, table détaillée.

Filtres disponibles : Region, GDP_per_capita_Category, Literacy_Category.

## Sources de données

Les indicateurs ont été compilés à partir de publications citant elles-mêmes la Banque Mondiale, l'UNESCO et le FMI comme sources primaires :

- **Alphabétisation des adultes** (total/H/F) — UNESCO Institute for Statistics / CIA World Factbook
- **Dépenses publiques d'éducation** (% du PIB) — Banque Mondiale (WDI)
- **Scolarisation primaire et secondaire brute** — UNESCO
- **Population** — Nations Unies / recensements officiels
- **PIB par habitant (PPA)** — FMI, World Economic Outlook


## Méthodologie de nettoyage (résumé)

- Dédoublonnage par pays (clé unique), harmonisation des noms de pays
- Valeurs manquantes imputées par la médiane régionale, tracées dans `Data_Estimated_Flag`
- Colonnes calculées : `Literacy_Gender_Gap_pp`, `Enrollment_Drop_Primary_to_Secondary_pp`, `Out_of_School_Risk_Index`, catégories (`Literacy_Category`, `Education_Investment_Category`, `GDP_per_capita_Category`)

Détail complet dans le rapport PDF (section 3) et l'onglet `Cleaning_Log` du classeur.

## Principaux résultats

- Alphabétisation moyenne Afrique : **68,5 %** (Afrique australe 81,9 % vs Afrique de l'Ouest 55,2 %)
- Écart de genre moyen : **12,3 points**, jusqu'à 19 points en Afrique de l'Ouest
- Corrélation dépenses éducation ↔ alphabétisation : **modérée (~0,27)**
- Corrélation PIB/habitant ↔ alphabétisation : **plus forte (~0,59)**
- **11 pays sur 54** en situation critique (alphabétisation < 50 %)



