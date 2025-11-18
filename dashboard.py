import streamlit as st
import pandas as pd
import plotly.express as px

# ======================
#   CONFIGURACIÓN
# ======================
st.set_page_config(page_title="IMDb Top 1000", layout="wide")

st.title("🎬 Análisis IMDb Top 1000")
st.write("Dashboard interactivo - Proyecto Final Minería de Datos")

# ======================
#   CARGA DEL DATASET
# ======================
try:
    df = pd.read_csv("imdb_clean.csv")
except FileNotFoundError:
    st.error("❌ Error: No se encontró el archivo 'imdb_clean.csv'. Ejecutá antes el script de limpieza.")
    st.stop()

# ======================
#   FILTRO LATERAL
# ======================
st.sidebar.header("Filtros")

genres = sorted(df["main_genre"].unique())
genre_filter = st.sidebar.selectbox("Seleccionar género:", ["Todos"] + genres)

if genre_filter != "Todos":
    df_filtered = df[df["main_genre"] == genre_filter]
else:
    df_filtered = df.copy()

st.sidebar.write(f"Películas filtradas: **{df_filtered.shape[0]}**")

# ======================
#   GRÁFICO 1 - TOP RATING
# ======================
st.header("⭐ Top 10 películas con mejor rating IMDb")

top_rating = df_filtered.sort_values(by="imdb_rating", ascending=False).head(10)

fig1 = px.bar(
    top_rating,
    x="imdb_rating",
    y="title",
    orientation="h",
    title="Top 10 por Rating IMDb",
    labels={"imdb_rating": "Rating IMDb", "title": "Título"}
)

fig1.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig1)

# ======================
#   GRÁFICO 2 - PELÍCULAS POR DÉCADA
# ======================
st.header("🎞 Distribución de películas por década")

decade_count = df_filtered["decade"].dropna().value_counts().sort_index()

fig2 = px.bar(
    x=decade_count.index,
    y=decade_count.values,
    title="Cantidad de Películas por Década",
    labels={"x": "Década", "y": "Cantidad"}
)

st.plotly_chart(fig2)

# ======================
#   GRÁFICO 3 - REVENUE PROMEDIO POR GÉNERO (TOP 10)
# ======================
st.header("💰 Top 10 Géneros con Mayor Revenue Promedio")

revenue_genre = (
    df_filtered.groupby("main_genre")["revenue"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

revenue_genre.columns = ["Género", "Revenue Promedio"]

fig3 = px.bar(
    revenue_genre,
    x="Revenue Promedio",
    y="Género",
    orientation="h",
    title="Top 10 Géneros con Mayor Ganancia Promedio",
)

fig3.update_xaxes(tickprefix="$", tickformat=",.0f")
st.plotly_chart(fig3)

# ======================
#   TABLA
# ======================
st.header("📋 Vista previa de datos filtrados")
st.dataframe(df_filtered.head(20))

# ======================
#   CONCLUSIONES AUTOMÁTICAS
# ======================
st.header("📌 Conclusiones del análisis")

# Mejor película
best_movie = df_filtered.loc[df_filtered["imdb_rating"].idxmax()]

# Década preferida
most_decade = decade_count.idxmax() if len(decade_count) > 0 else "N/A"

# Género de mayor revenue
top_genre_rev = revenue_genre.iloc[0]["Género"] if len(revenue_genre) > 0 else "N/A"

st.write(f"""
### 🔍 Hallazgos principales

- 🏆 **Película mejor calificada:**  
  **{best_movie['title']}** con **{best_movie['imdb_rating']} puntos IMDb**.

- 📅 **Década con más películas:**  
  **{int(most_decade)}**.

- 💸 **Género con mayor revenue promedio:**  
  **{top_genre_rev}**.

Las conclusiones se actualizan automáticamente según el género seleccionado en el filtro lateral.
""")

