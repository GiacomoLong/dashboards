import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, date, timedelta
import geopandas as gpd
import osmnx as ox
import os
import folium
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap
import streamlit.components.v1 as components
import time

#Titolo
st.title("Analisi del clima estivo e luoghi per affrontare il caldo")

#capoluoghi di provincia (latitudine, longitudine, codice openstreetmap)
CITTA = {
    "Agrigento":      {"lat": 37.3111, "lon": 13.5765, "cod": "39202"},
    "Alessandria":    {"lat": 44.9124, "lon": 8.6151, "cod": "43747"},
    "Ancona":         {"lat": 43.6158, "lon": 13.5189, "cod": "42499"},
    "Aosta":          {"lat": 45.7369, "lon": 7.3201, "cod": "45916"},
    "Arezzo":         {"lat": 43.4633, "lon": 11.8798, "cod": "42414"},
    "Ascoli Piceno":  {"lat": 42.8535, "lon": 13.5749, "cod": "42176"},
    "Asti":           {"lat": 44.9003, "lon": 8.2064, "cod": "43724"},
    "Avellino":       {"lat": 40.9148, "lon": 14.7904, "cod": "40857"},
    "Bari":           {"lat": 41.1177, "lon": 16.8719, "cod": "41038"},
    "Barletta":       {"lat": 41.3178, "lon": 16.2840, "cod": "41200"},
    "Belluno":        {"lat": 46.1399, "lon": 12.2159, "cod": "46834"},
    "Benevento":      {"lat": 41.1297, "lon": 14.7826, "cod": "41099"},
    "Bergamo":        {"lat": 45.6983, "lon": 9.6773, "cod": "45681"},
    "Biella":         {"lat": 45.5628, "lon": 8.0530, "cod": "45293"},
    "Bologna":        {"lat": 44.4949, "lon": 11.3426, "cod": "43172"},
    "Bolzano":        {"lat": 46.4983, "lon": 11.3548, "cod": "47207"},
    "Brescia":        {"lat": 45.5416, "lon": 10.2118, "cod": "45144"},
    "Brindisi":       {"lat": 40.6327, "lon": 17.9419, "cod": "40545"},
    "Cagliari":       {"lat": 39.2238, "lon": 9.1217, "cod": "39837"},
    "Caltanissetta":  {"lat": 37.4903, "lon": 14.0627, "cod": "39221"},
    "Campobasso":     {"lat": 41.5603, "lon": 14.6622, "cod": "41361"},
    "Caserta":        {"lat": 41.0740, "lon": 14.3328, "cod": "41056"},
    "Catania":        {"lat": 37.5079, "lon": 15.0830, "cod": "39230"},
    "Catanzaro":      {"lat": 38.9098, "lon": 16.5877, "cod": "39727"},
    "Chieti":         {"lat": 42.3498, "lon": 14.1671, "cod": "41961"},
    "Como":           {"lat": 45.8081, "lon": 9.0852, "cod": "46085"},
    "Cosenza":        {"lat": 39.3000, "lon": 16.2500, "cod": "39859"},
    "Cremona":        {"lat": 45.1333, "lon": 10.0222, "cod": "44189"},
    "Crotone":        {"lat": 39.0811, "lon": 17.1247, "cod": "39779"},
    "Cuneo":          {"lat": 44.3839, "lon": 7.5423, "cod": "43083"},
    "Enna":           {"lat": 37.5659, "lon": 14.2791, "cod": "39245"},
    "Fermo":          {"lat": 43.1608, "lon": 13.7183, "cod": "42331"},
    "Ferrara":        {"lat": 44.8381, "lon": 11.6197, "cod": "43512"},
    "Firenze":        {"lat": 43.7696, "lon": 11.2558, "cod": "42602"},
    "Foggia":         {"lat": 41.4621, "lon": 15.5446, "cod": "41243"},
    "Forlì":          {"lat": 44.2227, "lon": 12.0408, "cod": "42907"},
    "Frosinone":      {"lat": 41.6401, "lon": 13.3436, "cod": "41419"},
    "Genova":         {"lat": 44.4056, "lon": 8.9463, "cod": "44875"},
    "Gorizia":        {"lat": 45.9408, "lon": 13.6219, "cod": "179075"},
    "Grosseto":       {"lat": 42.7594, "lon": 11.1128, "cod": "42153"},
    "Imperia":        {"lat": 43.8877, "lon": 8.0294, "cod": "42708"},
    "Isernia":        {"lat": 41.5952, "lon": 14.2338, "cod": "41385"},
    "La Spezia":      {"lat": 44.1024, "lon": 9.8240, "cod": "42842"},
    "L'Aquila":       {"lat": 42.3498, "lon": 13.3995, "cod": "41842"},
    "Latina":         {"lat": 41.4676, "lon": 12.9035, "cod": "41289"},
    "Lecce":          {"lat": 40.3516, "lon": 18.1750, "cod": "40442"},
    "Lecco":          {"lat": 45.8566, "lon": 9.3969, "cod": "46229"},
    "Livorno":        {"lat": 43.5479, "lon": 10.3149, "cod": "42481"},
    "Lodi":           {"lat": 45.3142, "lon": 9.5034, "cod": "44665"},
    "Lucca":          {"lat": 43.8376, "lon": 10.4950, "cod": "42659"},
    "Macerata":       {"lat": 43.2989, "lon": 13.4531, "cod": "42394"},
    "Mantova":        {"lat": 45.1564, "lon": 10.7914, "cod": "44232"},
    "Massa":          {"lat": 44.0353, "lon": 10.1396, "cod": "42813"},
    "Matera":         {"lat": 40.6664, "lon": 16.6043, "cod": "40622"},
    "Messina":        {"lat": 38.1937, "lon": 15.5542, "cod": "39514"},
    "Milano":         {"lat": 45.4654, "lon": 9.1859, "cod": "44915"},
    "Modena":         {"lat": 44.6471, "lon": 10.9252, "cod": "43336"},
    "Monza":          {"lat": 45.5845, "lon": 9.2744, "cod": "45319"},
    "Napoli":         {"lat": 40.8518, "lon": 14.2681, "cod": "40767"},
    "Novara":         {"lat": 45.4459, "lon": 8.6218, "cod": "44898"},
    "Nuoro":          {"lat": 40.3212, "lon": 9.3309, "cod": "40387"},
    "Oristano":       {"lat": 39.9063, "lon": 8.5920, "cod": "40125"},
    "Padova":         {"lat": 45.4064, "lon": 11.8768, "cod": "44836"},
    "Palermo":        {"lat": 38.1157, "lon": 13.3615, "cod": "39513"},
    "Parma":          {"lat": 44.8015, "lon": 10.3279, "cod": "43452"},
    "Pavia":          {"lat": 45.1847, "lon": 9.1582, "cod": "44383"},
    "Perugia":        {"lat": 43.1122, "lon": 12.3888, "cod": "42278"},
    "Pesaro":         {"lat": 43.9111, "lon": 12.9136, "cod": "42672"},
    "Pescara":        {"lat": 42.4618, "lon": 14.2160, "cod": "42014"},
    "Piacenza":       {"lat": 45.0526, "lon": 9.6930, "cod": "43981"},
    "Pisa":           {"lat": 43.7228, "lon": 10.4017, "cod": "42527"},
    "Pistoia":        {"lat": 43.9305, "lon": 10.9109, "cod": "42722"},
    "Pordenone":      {"lat": 45.9564, "lon": 12.6615, "cod": "179205"},
    "Potenza":        {"lat": 40.6396, "lon": 15.8056, "cod": "40613"},
    "Prato":          {"lat": 43.8777, "lon": 11.1023, "cod": "280245"},
    "Ragusa":         {"lat": 36.9269, "lon": 14.7255, "cod": "39162"},
    "Ravenna":        {"lat": 44.4184, "lon": 12.2035, "cod": "42955"},
    "Reggio Calabria":{"lat": 38.1096, "lon": 15.6470, "cod": "39503"},
    "Reggio Emilia":  {"lat": 44.6989, "lon": 10.6297, "cod": "43415"},
    "Rieti":          {"lat": 42.4048, "lon": 12.8628, "cod": "41957"},
    "Rimini":         {"lat": 44.0678, "lon": 12.5695, "cod": "42791"},
    "Roma":           {"lat": 41.8933, "lon": 12.4829, "cod": "41485"},
    "Rovigo":         {"lat": 45.0693, "lon": 11.7899, "cod": "44024"},
    "Salerno":        {"lat": 40.6824, "lon": 14.7681, "cod": "40671"},
    "Sassari":        {"lat": 40.7259, "lon": 8.5556, "cod": "40683"},
    "Savona":         {"lat": 44.3069, "lon": 8.4826, "cod": "43007"},
    "Siena":          {"lat": 43.3186, "lon": 11.3307, "cod": "42398"},
    "Siracusa":       {"lat": 37.0755, "lon": 15.2866, "cod": "39169"},
    "Sondrio":        {"lat": 46.1697, "lon": 9.8706, "cod": "46963"},
    "Taranto":        {"lat": 40.4640, "lon": 17.2470, "cod": "40452"},
    "Teramo":         {"lat": 42.6589, "lon": 13.7036, "cod": "42107"},
    "Terni":          {"lat": 42.5636, "lon": 12.6430, "cod": "42064"},
    "Torino":         {"lat": 45.0703, "lon": 7.6869, "cod": "43992"},
    "Trapani":        {"lat": 38.0176, "lon": 12.5136, "cod": "39404"},
    "Trento":         {"lat": 46.0748, "lon": 11.1217, "cod": "46663"},
    "Treviso":        {"lat": 45.6669, "lon": 12.2430, "cod": "45511"},
    "Trieste":        {"lat": 45.6495, "lon": 13.7768, "cod": "179180"},
    "Udine":          {"lat": 46.0626, "lon": 13.2348, "cod": "179272"},
    "Varese":         {"lat": 45.8206, "lon": 8.8257, "cod": "46116"},
    "Venezia":        {"lat": 45.4408, "lon": 12.3155, "cod": "44741"},
    "Verbania":       {"lat": 45.9231, "lon": 8.5522, "cod": "46498"},
    "Vercelli":       {"lat": 45.3198, "lon": 8.4237, "cod": "1552703"},
    "Verona":         {"lat": 45.4386, "lon": 10.9928, "cod": "44830"},
    "Vibo Valentia":  {"lat": 38.6753, "lon": 16.0994, "cod": "39682"},
    "Vicenza":        {"lat": 45.5455, "lon": 11.5354, "cod": "45159"},
    "Viterbo":        {"lat": 42.4172, "lon": 12.1049, "cod": "41946"},
}

# Selezione città
città_selezionata = st.selectbox(
    "Seleziona città",
    CITTA.keys()
)

#Parametri
LAT = CITTA[città_selezionata]["lat"]
LON = CITTA[città_selezionata]["lon"]
COD = CITTA[città_selezionata]["cod"]
OGGI = date.today()
ANNI = 10
FINESTRA = 15
now = datetime.now()

#Funzioni richiesta dati
@st.cache_data(ttl=1800)
def meteo_citta(LAT, LON):
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,"
        "weather_code,wind_speed_10m"
        "&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max"
        "&timezone=Europe%2FRome"
        "&forecast_days=1"
    )
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.error(f"Errore API meteo: {e}")
        return None

@st.cache_data(ttl=1800)
def dati_orari(LAT, LON):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&hourly=temperature_2m"
        "&timezone=Europe%2FRome"
        "&forecast_days=1"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        st.error(f"Errore API: {e}")
        return None

@st.cache_data(ttl=86400)
def profilo_medio_storico(anni, LAT, LON):
    """Una sola chiamata API — nessun CSV, nessun loop."""
    start = (OGGI.replace(year=OGGI.year - anni)).strftime("%Y-%m-%d")
    end   = (OGGI - timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={LAT}&longitude={LON}"
        f"&start_date={start}&end_date={end}"
        "&hourly=temperature_2m"
        "&timezone=Europe%2FRome"
    )
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()

        df = pd.DataFrame({
            "ora":    data["hourly"]["time"],
            "t_aria": data["hourly"]["temperature_2m"],
        })
        df["ora"] = pd.to_datetime(df["ora"])
        df = df[
            (df["ora"].dt.month == OGGI.month) &
            (df["ora"].dt.day   == OGGI.day)
        ]
        df["hour"] = df["ora"].dt.hour
        profilo = df.groupby("hour")["t_aria"].mean().round(1).reset_index()
        profilo.columns = ["hour", "t_media_storica"]
        return profilo

    except Exception as e:
        st.error(f"Errore: {e}")
        return None

@st.cache_data(ttl=86400)
def media_storica_finestra(anni, finestra, LAT, LON):
    """Una sola chiamata API — nessun CSV, nessun loop."""
    start = (
        OGGI.replace(year=OGGI.year - anni) - timedelta(days=finestra)
    ).strftime("%Y-%m-%d")
    end = (OGGI - timedelta(days=1)).strftime("%Y-%m-%d")

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={LAT}&longitude={LON}"
        f"&start_date={start}&end_date={end}"
        "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean"
        "&timezone=Europe%2FRome"
    )
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()

        df = pd.DataFrame({
            "data":    data["daily"]["time"],
            "t_max":   data["daily"]["temperature_2m_max"],
            "t_min":   data["daily"]["temperature_2m_min"],
            "t_media": data["daily"]["temperature_2m_mean"],
        })
        df["data"] = pd.to_datetime(df["data"])
        df["offset_vs_oggi"] = df["data"].apply(
            lambda d: (
                d - pd.Timestamp(OGGI.replace(year=d.year))
            ).days
        )
        df = df[df["offset_vs_oggi"].between(-finestra, finestra)]
        profilo = (
            df.groupby("offset_vs_oggi")[["t_max", "t_min", "t_media"]]
            .mean().round(1).reset_index()
        )
        profilo.rename(columns={"offset_vs_oggi": "offset_gg"}, inplace=True)
        profilo["data"] = profilo["offset_gg"].apply(
            lambda x: OGGI + timedelta(days=x)
        )
        return profilo

    except Exception as e:
        st.error(f"Errore: {e}")
        return None
        
@st.cache_data(ttl=3600)
def dati_ultimi_15gg(LAT, LON):
    start = (OGGI - timedelta(days=FINESTRA)).strftime("%Y-%m-%d")
    end = (OGGI - timedelta(days=1)).strftime("%Y-%m-%d")
    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={LAT}&longitude={LON}"
        f"&start_date={start}&end_date={end}"
        "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean"
        "&timezone=Europe%2FRome"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame({
            "data": data["daily"]["time"],
            "t_max": data["daily"]["temperature_2m_max"],
            "t_min": data["daily"]["temperature_2m_min"],
            "t_media": data["daily"]["temperature_2m_mean"],
        })
        df["data"] = pd.to_datetime(df["data"])
        return df
    except Exception as e:
        return None

@st.cache_data(ttl=1800)
def dati_oggi(LAT, LON):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean"
        "&timezone=Europe%2FRome"
        "&forecast_days=1"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        df = pd.DataFrame({
            "data": data["daily"]["time"],
            "t_max": data["daily"]["temperature_2m_max"],
            "t_min": data["daily"]["temperature_2m_min"],
            "t_media": data["daily"]["temperature_2m_mean"],
        })
        df["data"] = pd.to_datetime(df["data"])
        return df
    except Exception as e:
        return None

#Sottotitolo
st.title("Analisi del clima estivo e luoghi per affrontare il caldo")
st.subheader(f"Clima estivo di {città_selezionata}")
st.markdown("---")

#Divisione in colonne
col_analisi, col_grafico = st.columns([1, 2])

#Colonna sx: analisi temperature
with col_analisi:
    st.markdown("### 🌡️ Analisi delle temperature")
    meteo_data = meteo_citta(LAT, LON)
    if meteo_data:
        cur = meteo_data['current']
        day = meteo_data['daily']
        temp = cur['temperature_2m']
        app_temp = cur['apparent_temperature']
        humidity = cur['relative_humidity_2m']
        weather_code = cur['weather_code']
        tem_max = day['temperature_2m_max'][0]
        tem_min = day['temperature_2m_min'][0]
        app_temp_max = day['apparent_temperature_max'][0]

        st.metric("Temperatura attuale", f"{temp} °C")
        st.metric("Temperatura percepita", f"{app_temp} °C")
        st.metric("Umidità relativa", f"{humidity} %")
        st.metric("Temp. massima prevista", f"{tem_max} °C")
        st.metric("Temp. minima prevista", f"{tem_min} °C")
        st.metric("Percepita massima prevista", f"{app_temp_max} °C")

#Colonna dx: grafico monitoraggio temperature
with col_grafico:
    st.markdown("### 📈 Grafico monitoraggio temperature")

    grafico = st.radio(
        label="Seleziona grafico",
        options=["📈 Temperatura oraria oggi", "📅 Ultimi 15 giorni vs media storica"],
        horizontal=True,
    )

    if grafico == "📈 Temperatura oraria oggi":
        data = dati_orari(LAT, LON)
        if data:
            df = pd.DataFrame({
                "ora": data["hourly"]["time"],
                "t_aria": data["hourly"]["temperature_2m"],
            })
            df["ora"] = pd.to_datetime(df["ora"])
            df["tipo"] = df["ora"].apply(lambda x: "reale" if x <= now else "previsione")

            df_reale = df[df["tipo"] == "reale"]
            df_previsione = df[df["tipo"] == "previsione"]
            giunzione = pd.concat([df_reale.iloc[[-1]], df_previsione.iloc[[0]]]) \
                if not df_reale.empty and not df_previsione.empty else pd.DataFrame()

            fig, ax = plt.subplots(figsize=(10, 4))
            if not df_reale.empty:
                ax.plot(df_reale["ora"].dt.strftime("%H:%M"), df_reale["t_aria"],
                        marker='o', linestyle='-', color='firebrick',
                        linewidth=2, markersize=5, markerfacecolor='white',
                        markeredgewidth=2, label="Reale")
            if not giunzione.empty:
                ax.plot(giunzione["ora"].dt.strftime("%H:%M"), giunzione["t_aria"],
                        linestyle='-', color='firebrick', linewidth=2, alpha=0.4)
            if not df_previsione.empty:
                ax.plot(df_previsione["ora"].dt.strftime("%H:%M"), df_previsione["t_aria"],
                        marker='o', linestyle='--', color='firebrick',
                        linewidth=2, markersize=5, markerfacecolor='white',
                        markeredgewidth=2, alpha=0.6, label="Previsione")
            profilo = profilo_medio_storico(10, LAT, LON)
            if profilo is not None:
                ax.plot([f"{h:02d}:00" for h in profilo["hour"]],
                        profilo["t_media_storica"].tolist(),
                        linestyle='-.', color='steelblue', linewidth=1.5,
                        alpha=0.8, label="Media storica (10 anni)")
            ax.axvline(x=now.strftime("%H:%M"), color='gray',
                       linestyle=':', linewidth=1.5, label="Ora attuale")
            ax.set_xlabel("Orario", fontsize=11)
            ax.set_ylabel("Temperatura (°C)", fontsize=11)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, linestyle='--', alpha=0.4)
            ax.legend(fontsize=9)
            st.pyplot(fig)

    elif grafico == "📅 Ultimi 15 giorni vs media storica":
        df_recente = dati_ultimi_15gg(LAT, LON)
        df_oggi_ = dati_oggi(LAT, LON)
        df_storico = media_storica_finestra(ANNI, FINESTRA, LAT,LON)

        if df_recente is not None and df_oggi_ is not None and df_storico is not None:
            df_completo = pd.concat([df_recente, df_oggi_], ignore_index=True)
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.fill_between(df_storico["data"], df_storico["t_min"], df_storico["t_max"],
                            alpha=0.15, color='steelblue', label="Range storico (min–max)")
            ax.plot(df_storico["data"], df_storico["t_media"],
                    linestyle='-.', color='steelblue', linewidth=1.5,
                    alpha=0.8, label="Media storica (10 anni)")
            ax.plot(df_completo["data"], df_completo["t_media"],
                    linestyle='-', color='firebrick', linewidth=2,
                    marker='o', markersize=5, markerfacecolor='white',
                    markeredgewidth=2, label="Temp. media (15gg + oggi)")
            ax.fill_between(df_completo["data"], df_completo["t_min"], df_completo["t_max"],
                            alpha=0.15, color='firebrick', label="Range giornaliero")
            t_oggi = df_oggi_["t_media"].values[0]
            ax.scatter(pd.Timestamp(OGGI), t_oggi, color='firebrick',
                       s=80, zorder=5, label=f"Oggi ({t_oggi}°C)")
            ax.axvline(x=pd.Timestamp(OGGI), color='gray', linestyle=':', linewidth=1.5)
            ax.set_xlabel("Data", fontsize=11)
            ax.set_ylabel("Temperatura (°C)", fontsize=11)
            ax.tick_params(axis='x', rotation=45)
            ax.grid(True, linestyle='--', alpha=0.4)
            ax.legend(loc="upper left", fontsize=9)
            st.pyplot(fig)

#Mappa luoghi per affrontare il caldo
st.markdown("---")
st.markdown(f"### 🗺️ Luoghi per affrontare il caldo a {città_selezionata}")

# Funzioni per dati geografici
@st.cache_data
def get_boundary(COD):
    return ox.geocode_to_gdf(f'R{COD}', by_osmid=True)

@st.cache_data
def get_amenity(COD):
    polygon = get_boundary(COD).geometry.iloc[0]
    return ox.features.features_from_polygon(
        polygon=polygon,
        tags={'amenity': ['drinking_water']}
    )

@st.cache_data
def get_leisure(COD):
    polygon = get_boundary(COD).geometry.iloc[0] 
    return ox.features.features_from_polygon(
        polygon=polygon,
        tags={'leisure': ['park', 'swimming_area']}
    )

boundary   = get_boundary(COD)
amenity_gdf = get_amenity(COD)
leisure_gdf = get_leisure(COD)

amenity_gdf = amenity_gdf.reset_index(level=[0, 1])[['amenity', 'geometry']]
leisure_gdf = leisure_gdf.reset_index(level=[0, 1])[['leisure', 'name', 'geometry']]

# Sanitizza nomi per evitare errori encoding
for col in leisure_gdf.select_dtypes(include='object').columns:
    leisure_gdf[col] = leisure_gdf[col].apply(
        lambda x: x.encode('utf-8', errors='replace').decode('utf-8') if isinstance(x, str) else x
    )

wet_gdf_park     = leisure_gdf[leisure_gdf['leisure'] == 'park'].copy()
wet_gdf_swimming = leisure_gdf[leisure_gdf['leisure'] == 'swimming_area'].copy()
wet_gdf_drinking = amenity_gdf[amenity_gdf['amenity'] == 'drinking_water'].copy()

wet_gdf_park['_nome'] = wet_gdf_park['name'].fillna('Parco senza nome') \
    if 'name' in wet_gdf_park.columns else 'Parco'

# Mappa
mappa = leafmap.Map(width=1200, height=550)
mappa.add_basemap("CartoDB.Positron")
mappa.zoom_to_gdf(boundary)

boundary.explore(
    m=mappa, name="Confine Comunale",
    tooltip=False, highlight=False,
    style_kwds={"color": "#e63946", "weight": 3, "fillOpacity": 0, "dashArray": "6 4"}
)

if not wet_gdf_park.empty:
    wet_gdf_park.explore(
        m=mappa, name="🌳 Parchi",
        tooltip='_nome',
        tooltip_kwds={"sticky": True, "labels": False},
        style_kwds={"color": "#2d6a4f", "fillColor": "#52b788", "fillOpacity": 0.5, "weight": 2}
    )

if not wet_gdf_swimming.empty:
    wet_gdf_swimming.explore(
        m=mappa, name="🏊 Aree Nuoto",
        style_kwds={"color": "#0077b6", "fillColor": "#90e0ef", "fillOpacity": 0.6, "weight": 2}
    )

if not wet_gdf_drinking.empty:
    drinking_centroid = wet_gdf_drinking.copy()
    drinking_centroid['geometry'] = wet_gdf_drinking.geometry.centroid
    for _, row in drinking_centroid.iterrows():
        if row.geometry.is_empty:
            continue
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            tooltip="Fontanella",
            icon=folium.Icon(color='cadetblue', icon='tint', prefix='fa')
        ).add_to(mappa)

folium.LayerControl(collapsed=False).add_to(mappa)

# Leggenda
legenda_html = """
<div style="
    position: fixed; bottom: 30px; left: 30px;
    background: white; border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    padding: 16px 20px; z-index: 1000;
    font-family: 'Segoe UI', sans-serif; min-width: 180px;">
    <div style="font-weight:700; font-size:14px; margin-bottom:10px;
                color:#333; border-bottom:2px solid #eee; padding-bottom:6px;">
        🗺️ Legenda
    </div>
    <div style="display:flex; align-items:center; margin-bottom:8px;">
        <div style="width:28px; height:4px; background:#e63946; border-radius:2px;
                    margin-right:10px; border:1px dashed #e63946;"></div>
        <span style="font-size:13px; color:#444;">Confine Comunale</span>
    </div>
    <div style="display:flex; align-items:center; margin-bottom:8px;">
        <div style="width:28px; height:16px; background:#52b788; border-radius:4px;
                    margin-right:10px; border:2px solid #2d6a4f;"></div>
        <span style="font-size:13px; color:#444;">🌳 Parchi</span>
    </div>
    <div style="display:flex; align-items:center; margin-bottom:8px;">
        <div style="width:28px; height:16px; background:#90e0ef; border-radius:4px;
                    margin-right:10px; border:2px solid #0077b6;"></div>
        <span style="font-size:13px; color:#444;">🏊 Aree Nuoto</span>
    </div>
    <div style="display:flex; align-items:center;">
        <span style="font-size:18px; margin-right:8px;">💧</span>
        <span style="font-size:13px; color:#444;">Fontanelle</span>
    </div>
</div>
"""
mappa.get_root().html.add_child(folium.Element(legenda_html))

html_content = mappa._repr_html_()
components.html(html_content, width=1200, height=550, scrolling=False)
