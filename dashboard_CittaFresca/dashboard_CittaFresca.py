import streamlit as st
import geopandas as gpd
import osmnx as ox
import folium
from streamlit_folium import st_folium
import leafmap.foliumap as leafmap
import streamlit.components.v1 as components
import requests

# ── TITOLO ───────────────────────────────────────────────
st.title("Città Fresca")

# ── DIZIONARIO CITTÀ ─────────────────────────────────────
CITTA = {
    "Agrigento":      {"lat": 37.3111, "lon": 13.5765, "cod": "39202"},
    "Alessandria":    {"lat": 44.9124, "lon": 8.6151,  "cod": "43747"},
    "Ancona":         {"lat": 43.6158, "lon": 13.5189, "cod": "42499"},
    "Aosta":          {"lat": 45.7369, "lon": 7.3201,  "cod": "45916"},
    "Arezzo":         {"lat": 43.4633, "lon": 11.8798, "cod": "42414"},
    "Ascoli Piceno":  {"lat": 42.8535, "lon": 13.5749, "cod": "42176"},
    "Asti":           {"lat": 44.9003, "lon": 8.2064,  "cod": "43724"},
    "Avellino":       {"lat": 40.9148, "lon": 14.7904, "cod": "40857"},
    "Bari":           {"lat": 41.1177, "lon": 16.8719, "cod": "41038"},
    "Barletta":       {"lat": 41.3178, "lon": 16.2840, "cod": "41200"},
    "Belluno":        {"lat": 46.1399, "lon": 12.2159, "cod": "46834"},
    "Benevento":      {"lat": 41.1297, "lon": 14.7826, "cod": "41099"},
    "Bergamo":        {"lat": 45.6983, "lon": 9.6773,  "cod": "45681"},
    "Biella":         {"lat": 45.5628, "lon": 8.0530,  "cod": "45293"},
    "Bologna":        {"lat": 44.4949, "lon": 11.3426, "cod": "43172"},
    "Bolzano":        {"lat": 46.4983, "lon": 11.3548, "cod": "47207"},
    "Brescia":        {"lat": 45.5416, "lon": 10.2118, "cod": "45144"},
    "Brindisi":       {"lat": 40.6327, "lon": 17.9419, "cod": "40545"},
    "Cagliari":       {"lat": 39.2238, "lon": 9.1217,  "cod": "39837"},
    "Caltanissetta":  {"lat": 37.4903, "lon": 14.0627, "cod": "39221"},
    "Campobasso":     {"lat": 41.5603, "lon": 14.6622, "cod": "41361"},
    "Caserta":        {"lat": 41.0740, "lon": 14.3328, "cod": "41056"},
    "Catania":        {"lat": 37.5079, "lon": 15.0830, "cod": "39230"},
    "Catanzaro":      {"lat": 38.9098, "lon": 16.5877, "cod": "39727"},
    "Chieti":         {"lat": 42.3498, "lon": 14.1671, "cod": "41961"},
    "Como":           {"lat": 45.8081, "lon": 9.0852,  "cod": "46085"},
    "Cosenza":        {"lat": 39.3000, "lon": 16.2500, "cod": "39859"},
    "Cremona":        {"lat": 45.1333, "lon": 10.0222, "cod": "44189"},
    "Crotone":        {"lat": 39.0811, "lon": 17.1247, "cod": "39779"},
    "Cuneo":          {"lat": 44.3839, "lon": 7.5423,  "cod": "43083"},
    "Enna":           {"lat": 37.5659, "lon": 14.2791, "cod": "39245"},
    "Fermo":          {"lat": 43.1608, "lon": 13.7183, "cod": "42331"},
    "Ferrara":        {"lat": 44.8381, "lon": 11.6197, "cod": "43512"},
    "Firenze":        {"lat": 43.7696, "lon": 11.2558, "cod": "42602"},
    "Foggia":         {"lat": 41.4621, "lon": 15.5446, "cod": "41243"},
    "Forlì":          {"lat": 44.2227, "lon": 12.0408, "cod": "42907"},
    "Frosinone":      {"lat": 41.6401, "lon": 13.3436, "cod": "41419"},
    "Genova":         {"lat": 44.4056, "lon": 8.9463,  "cod": "44875"},
    "Gorizia":        {"lat": 45.9408, "lon": 13.6219, "cod": "179075"},
    "Grosseto":       {"lat": 42.7594, "lon": 11.1128, "cod": "42153"},
    "Imperia":        {"lat": 43.8877, "lon": 8.0294,  "cod": "42708"},
    "Isernia":        {"lat": 41.5952, "lon": 14.2338, "cod": "41385"},
    "La Spezia":      {"lat": 44.1024, "lon": 9.8240,  "cod": "42842"},
    "L'Aquila":       {"lat": 42.3498, "lon": 13.3995, "cod": "41842"},
    "Latina":         {"lat": 41.4676, "lon": 12.9035, "cod": "41289"},
    "Lecce":          {"lat": 40.3516, "lon": 18.1750, "cod": "40442"},
    "Lecco":          {"lat": 45.8566, "lon": 9.3969,  "cod": "46229"},
    "Livorno":        {"lat": 43.5479, "lon": 10.3149, "cod": "42481"},
    "Lodi":           {"lat": 45.3142, "lon": 9.5034,  "cod": "44665"},
    "Lucca":          {"lat": 43.8376, "lon": 10.4950, "cod": "42659"},
    "Macerata":       {"lat": 43.2989, "lon": 13.4531, "cod": "42394"},
    "Mantova":        {"lat": 45.1564, "lon": 10.7914, "cod": "44232"},
    "Massa":          {"lat": 44.0353, "lon": 10.1396, "cod": "42813"},
    "Matera":         {"lat": 40.6664, "lon": 16.6043, "cod": "40622"},
    "Messina":        {"lat": 38.1937, "lon": 15.5542, "cod": "39514"},
    "Milano":         {"lat": 45.4654, "lon": 9.1859,  "cod": "44915"},
    "Modena":         {"lat": 44.6471, "lon": 10.9252, "cod": "43336"},
    "Monza":          {"lat": 45.5845, "lon": 9.2744,  "cod": "45319"},
    "Napoli":         {"lat": 40.8518, "lon": 14.2681, "cod": "40767"},
    "Novara":         {"lat": 45.4459, "lon": 8.6218,  "cod": "44898"},
    "Nuoro":          {"lat": 40.3212, "lon": 9.3309,  "cod": "40387"},
    "Oristano":       {"lat": 39.9063, "lon": 8.5920,  "cod": "40125"},
    "Padova":         {"lat": 45.4064, "lon": 11.8768, "cod": "44836"},
    "Palermo":        {"lat": 38.1157, "lon": 13.3615, "cod": "39513"},
    "Parma":          {"lat": 44.8015, "lon": 10.3279, "cod": "43452"},
    "Pavia":          {"lat": 45.1847, "lon": 9.1582,  "cod": "44383"},
    "Perugia":        {"lat": 43.1122, "lon": 12.3888, "cod": "42278"},
    "Pesaro":         {"lat": 43.9111, "lon": 12.9136, "cod": "42672"},
    "Pescara":        {"lat": 42.4618, "lon": 14.2160, "cod": "42014"},
    "Piacenza":       {"lat": 45.0526, "lon": 9.6930,  "cod": "43981"},
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
    "Sassari":        {"lat": 40.7259, "lon": 8.5556,  "cod": "40683"},
    "Savona":         {"lat": 44.3069, "lon": 8.4826,  "cod": "43007"},
    "Siena":          {"lat": 43.3186, "lon": 11.3307, "cod": "42398"},
    "Siracusa":       {"lat": 37.0755, "lon": 15.2866, "cod": "39169"},
    "Sondrio":        {"lat": 46.1697, "lon": 9.8706,  "cod": "46963"},
    "Taranto":        {"lat": 40.4640, "lon": 17.2470, "cod": "40452"},
    "Teramo":         {"lat": 42.6589, "lon": 13.7036, "cod": "42107"},
    "Terni":          {"lat": 42.5636, "lon": 12.6430, "cod": "42064"},
    "Torino":         {"lat": 45.0703, "lon": 7.6869,  "cod": "43992"},
    "Trapani":        {"lat": 38.0176, "lon": 12.5136, "cod": "39404"},
    "Trento":         {"lat": 46.0748, "lon": 11.1217, "cod": "46663"},
    "Treviso":        {"lat": 45.6669, "lon": 12.2430, "cod": "45511"},
    "Trieste":        {"lat": 45.6495, "lon": 13.7768, "cod": "179180"},
    "Udine":          {"lat": 46.0626, "lon": 13.2348, "cod": "179272"},
    "Varese":         {"lat": 45.8206, "lon": 8.8257,  "cod": "46116"},
    "Venezia":        {"lat": 45.4408, "lon": 12.3155, "cod": "44741"},
    "Verbania":       {"lat": 45.9231, "lon": 8.5522,  "cod": "46498"},
    "Vercelli":       {"lat": 45.3198, "lon": 8.4237,  "cod": "1552703"},
    "Verona":         {"lat": 45.4386, "lon": 10.9928, "cod": "44830"},
    "Vibo Valentia":  {"lat": 38.6753, "lon": 16.0994, "cod": "39682"},
    "Vicenza":        {"lat": 45.5455, "lon": 11.5354, "cod": "45159"},
    "Viterbo":        {"lat": 42.4172, "lon": 12.1049, "cod": "41946"},
}

# ── SELEZIONE CITTÀ ──────────────────────────────────────
città_selezionata = st.selectbox("Seleziona città", CITTA.keys())

LAT  = CITTA[città_selezionata]["lat"]
LON  = CITTA[città_selezionata]["lon"]
COD  = CITTA[città_selezionata]["cod"]

# ════════════════════════════════════════════════════════
# FUNZIONI DATI GEOGRAFICI
# ════════════════════════════════════════════════════════
address = st.text_input(
    'Dove sei? Inserisci l'indirizzo',
    placeholder="es. Via Roma 10, Padova"
)

ORS_API_KEY = st.secrets['ORS_API_KEY']

@st.cache_data
def geocode(query):
    parameters = {'api_key': ORS_API_KEY, 'text': query}
    try:
        response = requests.get(
            'https://api.openrouteservice.org/geocode/search',
            params=parameters,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        if data.get('features'):
            x, y = data['features'][0]['geometry']['coordinates']
            return (y, x)
        else:
            st.warning("⚠️ Nessun risultato trovato per questo indirizzo")
            return None
    except requests.RequestException as e:
        st.error(f"❌ Errore geocoding: {e}")
        return None

@st.cache_data
def get_boundary(COD):
    return ox.geocode_to_gdf(f'R{COD}', by_osmid=True)

@st.cache_data
def get_amenity(COD):
    polygon = get_boundary(COD).geometry.iloc[0]
    return ox.features.features_from_polygon(
        polygon=polygon,
        tags={'amenity': ['drinking_water', 'library', 'pharmacy', 'shelter']}
    )

@st.cache_data
def get_leisure(COD):
    polygon = get_boundary(COD).geometry.iloc[0]
    return ox.features.features_from_polygon(
        polygon=polygon,
        tags={'leisure': ['park', 'swimming_area', 'garden', 'swimming_pool']}
    )

# ── CARICAMENTO DATI ─────────────────────────────────────
boundary    = get_boundary(COD)
amenity_gdf = get_amenity(COD)
leisure_gdf = get_leisure(COD)

# ── PULIZIA COLONNE ──────────────────────────────────────
amenity_gdf = amenity_gdf.reset_index(level=[0, 1])[['amenity', 'name', 'geometry']]
leisure_gdf = leisure_gdf.reset_index(level=[0, 1])[['leisure', 'name', 'geometry']]

for gdf in [amenity_gdf, leisure_gdf]:
    for col in gdf.select_dtypes(include='object').columns:
        gdf[col] = gdf[col].apply(
            lambda x: x.encode('utf-8', errors='replace').decode('utf-8')
            if isinstance(x, str) else x
        )

# ── SPLIT PER TIPO ───────────────────────────────────────
wet_gdf_park     = leisure_gdf[leisure_gdf['leisure'] == 'park'].copy()
wet_gdf_swimming = leisure_gdf[leisure_gdf['leisure'] == 'swimming_area'].copy()
wet_gdf_garden   = leisure_gdf[leisure_gdf['leisure'] == 'garden'].copy()
wet_gdf_pool     = leisure_gdf[leisure_gdf['leisure'] == 'swimming_pool'].copy()
wet_gdf_drinking = amenity_gdf[amenity_gdf['amenity'] == 'drinking_water'].copy()
wet_gdf_library  = amenity_gdf[amenity_gdf['amenity'] == 'library'].copy()
wet_gdf_pharmacy = amenity_gdf[amenity_gdf['amenity'] == 'pharmacy'].copy()
wet_gdf_shelter  = amenity_gdf[amenity_gdf['amenity'] == 'shelter'].copy()

for gdf, fallback in [
    (wet_gdf_park,   "Parco senza nome"),
    (wet_gdf_garden, "Giardino senza nome"),
    (wet_gdf_pool,   "Piscina"),
]:
    gdf['_nome'] = gdf['name'].fillna(fallback) if 'name' in gdf.columns else fallback

def semplifica(gdf, tol=0.0001):
    gdf = gdf.copy()
    gdf['geometry'] = gdf['geometry'].simplify(tol, preserve_topology=True)
    return gdf

wet_gdf_park   = semplifica(wet_gdf_park)
wet_gdf_garden = semplifica(wet_gdf_garden)
wet_gdf_pool   = semplifica(wet_gdf_pool)

# ════════════════════════════════════════════════════════
# CHECKBOX SELEZIONE LAYER
# ════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(f"### 🗺️ Luoghi per affrontare il caldo a {città_selezionata}")
st.markdown("#### Seleziona i layer da visualizzare")

col1, col2 = st.columns(2)

with col1:
    show_park     = st.checkbox("🌳 Parchi",           value=True)
    show_garden   = st.checkbox("🌸 Giardini",         value=True)
    show_drinking = st.checkbox("💧 Fontanelle",       value=True)
    show_library  = st.checkbox("📚 Biblioteche",      value=True)

with col2:
    show_swimming = st.checkbox("🏊 Aree Nuoto",       value=True)
    show_pool     = st.checkbox("🏊 Piscine Pubbliche", value=True)
    show_pharmacy = st.checkbox("💊 Farmacie",         value=True)
    show_shelter  = st.checkbox("⛺ Ripari",            value=False)

# Avviso se nessun layer selezionato
if not any([show_park, show_garden, show_swimming, show_pool,
            show_drinking, show_library, show_pharmacy, show_shelter]):
    st.warning("⚠️ Seleziona almeno un layer per visualizzare la mappa")
    st.stop()

# ════════════════════════════════════════════════════════
# MAPPA
# ════════════════════════════════════════════════════════

mappa = leafmap.Map(width=1200, height=600)
mappa.add_basemap("CartoDB.Positron")
mappa.zoom_to_gdf(boundary)

# ── Dove sei ─────────────────────────────────────
if address:
    results = geocode(address)
    if results:
        folium.Marker(
            location=results,
            tooltip="Tu sei qui",
            icon=folium.Icon(color='red', icon='map-marker', prefix='fa')
        ).add_to(mappa)

        # Centra la mappa sul marker invece che sul confine comunale
        mappa.set_center(results[1], results[0], zoom=15)
    else:
        st.error('Nessun risultato per questo indirizzo')

# ── Confine comunale ─────────────────────────────────────
boundary.explore(
    m=mappa, name="Confine Comunale",
    tooltip=False, highlight=False,
    style_kwds={"color": "#e63946", "weight": 3,
                "fillOpacity": 0, "dashArray": "6 4"}
)

# ── Parchi ───────────────────────────────────────────────
if show_park and not wet_gdf_park.empty:
    wet_gdf_park.explore(
        m=mappa, name="🌳 Parchi",
        tooltip='_nome',
        tooltip_kwds={"sticky": True, "labels": False},
        style_kwds={"color": "#2d6a4f", "fillColor": "#52b788",
                    "fillOpacity": 0.5, "weight": 2}
    )

# ── Giardini ─────────────────────────────────────────────
if show_garden and not wet_gdf_garden.empty:
    wet_gdf_garden.explore(
        m=mappa, name="🌸 Giardini",
        tooltip='_nome',
        tooltip_kwds={"sticky": True, "labels": False},
        style_kwds={"color": "#7b2d8b", "fillColor": "#ce93d8",
                    "fillOpacity": 0.45, "weight": 2}
    )

# ── Aree nuoto ───────────────────────────────────────────
if show_swimming and not wet_gdf_swimming.empty:
    wet_gdf_swimming.explore(
        m=mappa, name="🏊 Aree Nuoto",
        style_kwds={"color": "#0077b6", "fillColor": "#90e0ef",
                    "fillOpacity": 0.6, "weight": 2}
    )

# ── Piscine ──────────────────────────────────────────────
if show_pool and not wet_gdf_pool.empty:
    wet_gdf_pool.explore(
        m=mappa, name="🏊 Piscine Pubbliche",
        tooltip='_nome',
        tooltip_kwds={"sticky": True, "labels": False},
        style_kwds={"color": "#0096c7", "fillColor": "#caf0f8",
                    "fillOpacity": 0.6, "weight": 2}
    )

# ── Fontanelle ───────────────────────────────────────────
if show_drinking and not wet_gdf_drinking.empty:
    drinking_c = wet_gdf_drinking.copy()
    drinking_c['geometry'] = wet_gdf_drinking.geometry.centroid
    for _, row in drinking_c.iterrows():
        if row.geometry.is_empty:
            continue
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            tooltip="Fontanella",
            icon=folium.Icon(color='cadetblue', icon='tint', prefix='fa')
        ).add_to(mappa)

# ── Biblioteche ──────────────────────────────────────────
if show_library and not wet_gdf_library.empty:
    library_c = wet_gdf_library.copy()
    library_c['geometry'] = wet_gdf_library.geometry.centroid
    for _, row in library_c.iterrows():
        if row.geometry.is_empty:
            continue
        nome = row.get('name', 'Biblioteca')
        if str(nome) == 'nan':
            nome = 'Biblioteca'
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            tooltip=nome,
            icon=folium.Icon(color='purple', icon='book', prefix='fa')
        ).add_to(mappa)

# ── Farmacie ─────────────────────────────────────────────
if show_pharmacy and not wet_gdf_pharmacy.empty:
    pharmacy_c = wet_gdf_pharmacy.copy()
    pharmacy_c['geometry'] = wet_gdf_pharmacy.geometry.centroid
    for _, row in pharmacy_c.iterrows():
        if row.geometry.is_empty:
            continue
        nome = row.get('name', 'Farmacia')
        if str(nome) == 'nan':
            nome = 'Farmacia'
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            tooltip=nome,
            icon=folium.Icon(color='green', icon='plus-square', prefix='fa')
        ).add_to(mappa)

# ── Ripari ───────────────────────────────────────────────
if show_shelter and not wet_gdf_shelter.empty:
    shelter_c = wet_gdf_shelter.copy()
    shelter_c['geometry'] = wet_gdf_shelter.geometry.centroid
    for _, row in shelter_c.iterrows():
        if row.geometry.is_empty:
            continue
        folium.Marker(
            location=[row.geometry.y, row.geometry.x],
            tooltip="Riparo",
            icon=folium.Icon(color='orange', icon='home', prefix='fa')
        ).add_to(mappa)

# ── Toggle layer ─────────────────────────────────────────
folium.LayerControl(collapsed=False).add_to(mappa)

html_content = mappa._repr_html_()
components.html(html_content, width=1200, height=600, scrolling=False)
