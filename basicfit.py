import json
import pandas as pd
import streamlit as st
import plotly.express as px

from streamlit_folium import folium_static
from utils import (markdown)
from map import Map

st.set_page_config(
    page_title="Basic fit Dashboard",
    layout="wide",
    #page_icon=st.image("https://www.promenadesdebretigny.fr/wp-content/uploads/2019/06/basic-fit.png")
)

st.title("Dashboard Basic-fit")

#Sidebar
file = st.sidebar.file_uploader(":orange[Importer votre fichier Basic fit :]")
#file = st.sidebar.file_uploader("$$\color{white} Importer votre fichier Basic fit :$$")
if file is None: 
    st.info("Importer votre fichier BasicFit dans la barre latéral à gauche")
    st.stop() 
else: 
    try:
        df = pd.DataFrame(json.load(file)["visits"]).assign(date=lambda x: x.date + " " + x.time).drop(
                "time", axis=1
            ).astype({"date": "datetime64"}).set_index("date").assign(
                club=lambda x: x.club.str.lstrip("Basic-Fit")
            ).assign(dow= lambda x: x.index.day_name())
        st.sidebar.success("Fichier correctement importé")
    except:
        st.error(
            "Mauvais fichier importé. Veuiller importer le fichier json de l'application basic-fit/mes données."
            )
        st.sidebar.error("Erreur dans l'importation du fichier !")
        st.stop()


col1, col2, col3 = st.columns(3)
col1.metric(label="Nombre d'entraînements", value=df.shape[0])
col2.metric(label="Nombre de basic-fit différents", value=len(df["club"].unique()))
close_days = (pd.to_datetime("2021-06-09") - pd.to_datetime("2020-10-29")).days
col3.metric(label="Nombre d'entraînements par semaine", value=round(7/(((df.index[0] - df.index[-1]).days-close_days)/(df.shape[0]+10)), 2))

st.write("\n")
st.plotly_chart(
    px.bar(
        df.groupby("club").size().to_frame().rename(
            columns={0 : "visites"}
            ).sort_values("visites", ascending=False).query("visites>2"), y="visites", text_auto=True,
            title = "Top des basic-fit les plus visités", color_discrete_sequence=["black"]
            ), use_container_width=True
)

col1, col2 = st.columns(2)
col1.write("**Entrainements les plus tôts :**")
col1.dataframe(
    df.sort_values(
        "date", key=lambda x: x.map(lambda x: x.time()),ascending=True
    ).head(3)
)
col2.write("**Entrainements les plus tardifs :**")
col2.dataframe(
    df.sort_values(
        "date", key=lambda x: x.map(lambda x: x.time()),ascending=False
    ).head(3)
)

st.plotly_chart(
    px.bar(df.groupby("dow").count().rename(
        columns={"club" : "nb_training"}
        ).loc[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],:],
        y="nb_training", text_auto=True, title= "Entraînements par jour de la semaine",
        color_discrete_sequence = ["black"]*7
    ), use_container_width=True
)

#Histogramme du nbr entraînement par heure la semaine et le week end

st.plotly_chart(
    px.histogram(
        df.assign(we=[i*"Week-end"+(not i)*"Semaine" for i in list(df["dow"].isin(['Saturday', 'Sunday']))]).set_index(
            df.index.hour
        ).reset_index(names="hour").groupby(["hour","we"]).size().to_frame(name="count").reset_index(),
        x="hour", y="count", text_auto=True, title= "Entraînements par heure le week-end ou la semaine",
        color="we", barmode="group", nbins=17, color_discrete_map={"Semaine": "orange", "Week-end": "black"}, labels={"hour": "Heure", "we": ""}
        ).update_layout(yaxis_title="Nombre d'entraînements"), use_container_width=True
)

mapper=Map()
result = mapper.map(df["club"].unique().tolist())
#Affichage des basic fit non placés
if result[1]:
    for erreur in result[1]:
        st.write(erreur)
#Affichage de la carte
markdown("Points de tous les basic-fit visités",size="20px")
def print_map(map):
    from streamlit_folium import st_folium
    st_folium(map, width=650, height=650)

print_map(result[0])