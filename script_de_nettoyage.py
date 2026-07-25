# -*- coding: utf-8 -*-
"""
Étape 2 — Nettoyage des données
Projet : Éducation en Afrique — Capstone Data Analytics

Prend africa_education_raw.csv (généré par 01_collecte_donnees.py) et applique :
  1. Dédoublonnage par pays
  2. Imputation des valeurs manquantes par médiane régionale (avec traçabilité)
  3. Standardisation des formats (types, arrondis, unités)
  4. Création des colonnes calculées utilisées dans le tableau de bord Power BI

Dépendances : pandas, numpy  ->  pip install pandas numpy
Sortie : africa_education_clean.csv (dans le même dossier que ce script)
"""
import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(SCRIPT_DIR, "africa_education_raw.csv")
CLEAN_PATH = os.path.join(SCRIPT_DIR, "africa_education_clean.csv")

df = pd.read_csv(RAW_PATH)

print("Forme initiale :", df.shape)
print("\nValeurs manquantes par colonne :\n", df.isna().sum())
print("\nDoublons (pays) :", df["Country"].duplicated().sum())

# ------------------------------------------------------------------
# 1. Dédoublonnage (clé = Country)
# ------------------------------------------------------------------
df = df.drop_duplicates(subset=["Country"])

# 2. Standardisation des noms de pays : déjà harmonisée à la collecte
#    (ex. "Ivory Coast" plutôt que "Côte d'Ivoire", "DR Congo" plutôt que "RD Congo")

# ------------------------------------------------------------------
# 3. Imputation des valeurs manquantes par médiane régionale
#    Chaque imputation est tracée dans Data_Estimated_Flag pour transparence
# ------------------------------------------------------------------
numeric_cols = [
    "Literacy_Rate_Total_pct", "Literacy_Rate_Male_pct", "Literacy_Rate_Female_pct",
    "Literacy_Gender_Gap_pp", "Edu_Spending_pct_GDP",
    "Primary_Enrollment_pct_gross", "Secondary_Enrollment_pct_gross",
]

df["Data_Estimated_Flag"] = ""

for col in numeric_cols:
    missing_before = df[col].isna()
    df[col] = df.groupby("Region")[col].transform(lambda x: x.fillna(x.median()))
    df[col] = df[col].fillna(df[col].median())  # filet de sécurité si région entière manquante
    newly_filled = missing_before & df[col].notna()
    df.loc[newly_filled, "Data_Estimated_Flag"] = (
        df.loc[newly_filled, "Data_Estimated_Flag"] + col.replace("_pct", "").replace("_gross", "") + ";"
    )

for col in numeric_cols:
    df[col] = df[col].round(1)

# Population et PIB : conversion en entiers
df["Population_2023"] = df["Population_2023"].astype(int)

gdp_missing = df["GDP_PPP_per_capita_USD"].isna()
df["GDP_PPP_per_capita_USD"] = df.groupby("Region")["GDP_PPP_per_capita_USD"].transform(lambda x: x.fillna(x.median()))
df["GDP_PPP_per_capita_USD"] = df["GDP_PPP_per_capita_USD"].fillna(df["GDP_PPP_per_capita_USD"].median())
df.loc[gdp_missing, "Data_Estimated_Flag"] = df.loc[gdp_missing, "Data_Estimated_Flag"] + "GDP_PPP_per_capita;"
df["GDP_PPP_per_capita_USD"] = df["GDP_PPP_per_capita_USD"].astype(int)

df["Literacy_Year"] = df["Literacy_Year"].fillna(df["Literacy_Year"].median()).astype(int)

# ------------------------------------------------------------------
# 4. Colonnes calculées
# ------------------------------------------------------------------
df["Out_of_School_Risk_Index"] = (100 - df["Primary_Enrollment_pct_gross"].clip(upper=100)).round(1)
df["Enrollment_Drop_Primary_to_Secondary_pp"] = (
    df["Primary_Enrollment_pct_gross"] - df["Secondary_Enrollment_pct_gross"]
).round(1)

df["Literacy_Category"] = pd.cut(
    df["Literacy_Rate_Total_pct"], bins=[0, 50, 70, 85, 100],
    labels=["Critical (<50%)", "Low (50-70%)", "Moderate (70-85%)", "High (85%+)"],
)
df["Education_Investment_Category"] = pd.cut(
    df["Edu_Spending_pct_GDP"], bins=[0, 2, 4, 6, 20],
    labels=["Low (<2%)", "Moderate (2-4%)", "Good (4-6%)", "High (6%+)"],
)
df["GDP_per_capita_Category"] = pd.cut(
    df["GDP_PPP_per_capita_USD"], bins=[0, 2000, 5000, 10000, 50000],
    labels=["Low income (<$2k)", "Lower-middle ($2-5k)", "Upper-middle ($5-10k)", "High (>$10k)"],
)

df["Population_Millions"] = (df["Population_2023"] / 1_000_000).round(2)

# ------------------------------------------------------------------
# 5. Réorganisation et export
# ------------------------------------------------------------------
cols_order = [
    "Country", "Region", "Population_2023", "Population_Millions",
    "GDP_PPP_per_capita_USD", "GDP_per_capita_Category",
    "Literacy_Rate_Total_pct", "Literacy_Rate_Male_pct", "Literacy_Rate_Female_pct",
    "Literacy_Gender_Gap_pp", "Literacy_Category", "Literacy_Year",
    "Edu_Spending_pct_GDP", "Education_Investment_Category",
    "Primary_Enrollment_pct_gross", "Secondary_Enrollment_pct_gross",
    "Enrollment_Drop_Primary_to_Secondary_pp", "Out_of_School_Risk_Index",
    "Data_Estimated_Flag",
]
df = df[cols_order].sort_values("Country").reset_index(drop=True)

df.to_csv(CLEAN_PATH, index=False)

print("\nForme finale :", df.shape)
print("Lignes avec au moins une valeur imputée :", (df["Data_Estimated_Flag"] != "").sum())
print(f"\nFichier nettoyé écrit : {CLEAN_PATH}")
