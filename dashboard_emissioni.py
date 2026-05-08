import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import leafmap.foliumap as leafmap

st.set_page_config(page_title='Dashboard', layout='wide')

st.title('Emissioni in Italia')

data_url = 'https://github.com/GiacomoLong/dashboards/releases/download/emissioni/'

acid_file = 'Acid_tot.xlsx'
ghg_file = 'GHG_TOT.xlsx'
nh3_file = 'NH3_tot.xlsx'
ozono_file = 'Ozono_tot.xlsx'
pm25_file = 'PM25_tot.xlsx'

regioni_file = 'Reg01012026_g_WGS84.shp'
acid_map = 'acid_map.shp'
ghg_map = 'ghg_map.shp'
nh3_map = 'nh3_map.shp'
ozono_map = 'ozono_map.shp'
pm25_map = 'pm25_map.shp'

@st.cache_data
def read_gdf(url):
    gdf = gpd.read_file(url)
    return gdf

@st.cache_data
def read_excel(url):
    df = pd.read_excel(url)
    return df
     
gpkg_url_regioni = data_url + regioni_file
gpkg_url_acid = data_url + acid_map
gpkg_url_ghg = data_url + ghg_map
gpkg_url_nh3 = data_url + nh3_map
gpkg_url_ozono = data_url + ozono_map
gpkg_url_pm25 = data_url + pm25_map

excel_url_acid = data_url + acid_file
excel_url_ghg = data_url + ghg_file
excel_url_nh3 = data_url + nh3_file
excel_url_ozono = data_url + ozono_file
excel_url_pm25 = data_url + pm25_file

regioni_gdf = read_gdf(gpkg_url_regioni)
Acid_gdf = read_gdf(gpkg_url_acid)
GHG_gdf = read_gdf(gpkg_url_ghg)
NH3_gdf = read_gdf(gpkg_url_nh3)
Ozono_gdf = read_gdf(gpkg_url_ozono)
PM25_gdf = read_gdf(gpkg_url_pm25)

Acid_df = read_excel(excel_url_acid)
GHG_df = read_excel(excel_url_ghg)
NH3_df = read_excel(excel_url_nh3)
Ozono_df = read_excel(excel_url_ozono)
PM25_df = read_excel(excel_url_pm25)

#Creazione scelte
col1, col2, col3 = st.columns(3)

#Creazione selection box inquinante
inquinanti = ['Acid', 'GHG', 'NH3', 'Ozono', 'PM25']
inquinante_selezionato = col1.selectbox('Seleziona un inquinante', inquinanti)

#regioni_gdf = regioni_gdf.to_crs(epsg=4326)

#Creazione selection box regione
regioni = regioni_gdf.DEN_REG.values
regione_selezionata = col2.selectbox('Seleziona una regione', regioni)
reg_select = regioni_gdf[regioni_gdf['DEN_REG'] == regione_selezionata]
reg_select = reg_select.to_crs(epsg=4326)

#Creazione selection box anno
anni = ['1990', '1995', '2000', '2005', '2010', '2015', '2017', '2019', '2021']
anno_selezionato = col3.selectbox('Seleziona un anno', anni)

colonna_inquinante = inquinante_selezionato + '_' + anno_selezionato

#Preparazione dati Acid
Acid_gdf = Acid_gdf.to_crs(epsg=4326)

#Preparazione dati GHG
GHG_gdf = GHG_gdf.to_crs(epsg=4326)

#Preparazione dati NH3
NH3_gdf = NH3_gdf.to_crs(epsg=4326)

#Preparazione dati Ozono
Ozono_gdf = Ozono_gdf.to_crs(epsg=4326)

#Preparazione dati PM25
PM25_gdf = PM25_gdf.to_crs(epsg=4326)

if inquinante_selezionato == 'Acid':
    inquinante_selezionato_gdf = Acid_gdf
    inquinante_selezionato_df = Acid_df
    st.subheader(f"Analisi delle emissioni di sostanze acide in Italia")
elif inquinante_selezionato == 'GHG':
    inquinante_selezionato_gdf = GHG_gdf
    inquinante_selezionato_df = GHG_df
    st.subheader(f"Analisi delle emissioni di gas serra (misurate in CO2 equivalente) in Italia")
elif inquinante_selezionato == 'NH3':
    inquinante_selezionato_gdf = NH3_gdf
    inquinante_selezionato_df = NH3_df
    st.subheader(f"Analisi delle emissioni di ammoniaca in agricoltura in Italia")
elif inquinante_selezionato == 'Ozono':
    inquinante_selezionato_gdf = Ozono_gdf
    inquinante_selezionato_df = Ozono_df
    st.subheader(f"Analisi delle emissioni di Ozono troposferico in Italia")
elif inquinante_selezionato == 'PM25':
    inquinante_selezionato_gdf = PM25_gdf
    inquinante_selezionato_df = PM25_df
    st.subheader(f"Analisi delle emissioni di particolato fine (PM2.5) in Italia")

inquinante_selezionato_gdf[colonna_inquinante] = pd.to_numeric(inquinante_selezionato_gdf[colonna_inquinante], errors='coerce').fillna(0)

with st.container():
    #separazione colonne
    col1_2, col2_2 = st.columns(2)

    with col1_2:

        anno = int(anno_selezionato)
        st.text(f"Grafico a barre delle emissioni nell'anno {anno_selezionato} per tutte le regioni")
        media_nazionale = inquinante_selezionato_df[anno].mean()
        inquinante_selezionato_df.loc['Media Italia'] = media_nazionale
        inquinante_selezionato_df.loc['Media Italia', 'DEN_REG'] = 'Media Italia'
        df_ordinato = inquinante_selezionato_df.sort_values(by=anno, ascending=True)
        colori = ['firebrick' if n == regione_selezionata else 'lightgrey' for n in df_ordinato['DEN_REG']]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df_ordinato['DEN_REG'], df_ordinato[anno], color=colori)
        ax.axhline(media_nazionale, color='red', linestyle='--', label='Media Nazionale')
        ax.set_title(f'Emissioni per regione ({anno_selezionato})', fontsize=14, pad=15)
        ax.set_xlabel('Regione', fontsize=12)
        ax.set_ylabel('Emissioni (ton)', fontsize=12)
        ax.set_xticklabels(df_ordinato['DEN_REG'], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)


    with col2_2:
        st.text(f"Mappa delle emissioni in Italia per l'anno {anno_selezionato}")
        #creazione mappa
        m = leafmap.Map(
        layers_control=True,
        #draw_control=False,
        #measure_control=False,
        #fullscreen_control=False
    )
        m.add_data(
            data=inquinante_selezionato_gdf,
            column=colonna_inquinante,
            scheme='Quantiles',
            cmap='Reds',
            k=5,
            layer_name='Emissioni {colonna_inquinante}',
            legend_title=f'{inquinante_selezionato} ({anno_selezionato})'
        )
        m.add_gdf(
        gdf=reg_select,
        layer_name='selected',
        zoom_to_layer=False,
        info_mode=None,
        style={'color': 'yellow', 'fill': None, 'weight': 2}
    )
        m_streamlit = m.to_streamlit(1200, 800)

with st.container():
    
    #separazione colonne
    col1_3, col2_3 = st.columns(2)
    
    with col1_3:
        st.text(f"Grafico delle emissioni in {regione_selezionata}")
        df_filtrato = inquinante_selezionato_df[inquinante_selezionato_df['DEN_REG'] == regione_selezionata].reset_index(drop=True)
        #st.write(df_filtrato.head())
        anni = [1990, 1995, 2000, 2005, 2010, 2015, 2017, 2019, 2021]
        valori = df_filtrato[anni].iloc[0].values
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(anni, valori, marker='o', linestyle='-', color='firebrick', 
                linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
        ax.set_title(f'Trend: {regione_selezionata}', fontsize=14, pad=15)
        ax.set_xlabel('Anno', fontsize=12)
        ax.set_ylabel('Emissioni (ton)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

    with col2_3:
        st.text_area(
            "Performance delle regioni in Italia",
            value=f"La regione {regione_selezionata} ha registrato emissioni pari a {int(df_filtrato[anno].iloc[0])} tonnellate nel {anno_selezionato}. \nLa media nazionale per questo inquinante è di {int(media_nazionale)} tonnellate. \nLa regione peggiore: {df_ordinato['DEN_REG'].iloc[-1]} con {int(df_ordinato[anno].iloc[-1])} tonnellate. \nLa regione migliore: {df_ordinato['DEN_REG'].iloc[0]} con {int(df_ordinato[anno].iloc[0])} tonnellate.",
            height=200
        )
    

    
    