import pandas as pd
import numpy as np

df = pd.read_csv("imdb.csv")
# ---------------------------------------------------------
# 1. RENOMBRADO DE COLUMNAS
# ---------------------------------------------------------
df = df.rename(columns={
    "Series_Title": "title",
    "Released_Year": "year",
    "Runtime": "runtime",
    "Genre": "genre",
    "IMDB_Rating": "imdb_rating",
    "Meta_score": "metascore",
    "No_of_Votes": "votes",
    "Gross": "revenue",
    "Certificate": "certificate"
})

# ---------------------------------------------------------
# 2. ELIMINAR DUPLICADOS Y NULOS
# ---------------------------------------------------------
df.drop_duplicates(subset=["title"], inplace=True)

df.dropna(subset=["title", "imdb_rating"], inplace=True)

# ---------------------------------------------------------
# 3. TRANSFORMACIÓN DE TIPOS
# ---------------------------------------------------------

# Año a numérico
df["year"] = pd.to_numeric(df["year"], errors="coerce")

# Duración: “142 min” → 142
df["runtime"] = df["runtime"].astype(str).str.replace(" min", "", regex=False)
df["runtime"] = pd.to_numeric(df["runtime"], errors="coerce")

# Revenue: limpiar "$" y comas
df["revenue"] = (
    df["revenue"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

# Rating a numérico
df["imdb_rating"] = pd.to_numeric(df["imdb_rating"], errors="coerce")

# ---------------------------------------------------------
# 4. VARIABLES DERIVADAS
# ---------------------------------------------------------

# Género principal
df["main_genre"] = df["genre"].str.split(",").str[0].str.strip()

# Lista de géneros para filtros múltiples en Streamlit
df["genre_list"] = df["genre"].str.split(",").apply(lambda x: [g.strip() for g in x])

# Década
df["decade"] = (df["year"] // 10) * 10

# ---------------------------------------------------------
# 5. GUARDAR RESULTADO
# ---------------------------------------------------------
df.to_csv("imdb_clean.csv", index=False)

print("✔ Proceso KDD completo. Archivo: imdb_clean.csv")
print(f"Registros finales: {df.shape[0]}")

