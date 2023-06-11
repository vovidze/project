import streamlit as st
import pandas as pd
import seaborn as sns
import sqlite3
import plotly.express as px
import folium
import random
from google_images_search import GoogleImagesSearch
from pydub import AudioSegment
from pydub.playback import play

realtor_data = pd.read_csv('realtor-data.csv')
zip_data = pd.read_csv('zips.txt', sep=',', names=['ZIP', 'LAT', 'LNG'])

realtor_data['zip_code'] = realtor_data['zip_code'].astype(str).str.split('.').str[0].str.zfill(5)

realtor_data = realtor_data.dropna()

random_realtor_data = realtor_data.sample(n=1000, random_state=42)

merged_data = pd.merge(random_realtor_data, zip_data, left_on='zip_code', right_on='ZIP', how='left')
merged_data['LAT'] = merged_data['LAT'].astype(float)
merged_data['LNG'] = merged_data['LNG'].astype(float)

map = folium.Map(location=[merged_data['LAT'].mean(), merged_data['LNG'].mean()], zoom_start=10)

for index, row in merged_data.iterrows():
    lat = row['LAT']
    lng = row['LNG']
    popup_info = f"Status: {row['status']}<br>" \
                 f"Beds: {row['bed']}<br>" \
                 f"Baths: {row['bath']}<br>" \
                 f"Acre Lot: {row['acre_lot']}<br>" \
                 f"City: {row['city']}<br>" \
                 f"State: {row['state']}<br>" \
                 f"Zip Code: {row['zip_code']}<br>" \
                 f"House Size: {row['house_size']}<br>" \
                 f"Previous Sold Date: {row['prev_sold_date']}<br>" \
                 f"Price: {row['price']}"
    marker = folium.Marker(location=[lat, lng], popup=popup_info)
    marker.add_to(map)

map_html = map.get_root().render()

st.markdown('<h1>Карта недвижимости</h1>', unsafe_allow_html=True)
st.write('Так как вхождений более 300к, то я решил использовать для визуализации первую 1000, так как иначе программа компилировалась очень долго, а карта отображалась с задержками.')
st.write("На каждой метке вы можете видеть данные по каждому объявлению. Чтобы получить визуализацию всех вхождений, достаточно убрать условие про 1000 вхождений.")
st.components.v1.html(map_html, height=500)

realtor_data = pd.read_csv('/Users/vovidze/Downloads/realtor-data.csv')

realtor_data = realtor_data.dropna()

realtor_data['bed'] = realtor_data['bed'].astype(int)

conn = sqlite3.connect(':memory:')
realtor_data.to_sql('realtor_data', conn, index=False)

states = sorted(realtor_data['state'].unique())
bedrooms = sorted(realtor_data['bed'].unique())

bedrooms = [int(bedroom) for bedroom in bedrooms]

selected_state = st.sidebar.selectbox('Выберите штат', states)

selected_bedroom = st.sidebar.slider('Выберите количество спален', min_value=min(bedrooms), max_value=max(bedrooms))

filtered_data = pd.read_sql_query(
    f"SELECT * FROM realtor_data WHERE state = '{selected_state}' AND bed = {selected_bedroom}",
    conn
)

st.subheader('Графики')
st.write("Теперь в зависимости от выбранных вами фильтров вы увидите графики по заданным критериям. Для реализации этого я использовал базу данных SQLite")

st.subheader('Гистограмма цен')
fig = px.histogram(filtered_data, x='price')
st.plotly_chart(fig)

st.subheader('График размера дома в зависимости от цены')
fig = px.scatter(filtered_data, x='price', y='house_size')
st.plotly_chart(fig)


API_KEY = "AIzaSyCbVB-LRygkCRuor15-CjkznowQTQFSrmQ"
CX = "0593d40f21bd744c4"

def get_first_image(query):
    gis = GoogleImagesSearch(API_KEY, CX)
    search_params = {
        "q": query,
        "num": 1,
        "safe": "high",
        "fileType": "jpg|png"
    }
    gis.search(search_params)
    if gis.results():
        image_url = gis.results()[0].url
        return image_url
    return None

state = st.sidebar.selectbox("Выберите штат для поиска фото", realtor_data["state"].unique())

beds = st.sidebar.slider("Выберите количество спален для поиска фото", min_value=int(realtor_data["bed"].min()), max_value=int(realtor_data["bed"].max()), key="beds_slider")

query = f"дом {state} {beds} спальни"

image_url = get_first_image(query)

st.write("Теперь прошу выбрать новые показатели (или такие же) во второй паре фильтров. Найдем с помощью API Google, как выглядит недвижимость по запросу \"дом {state} {beds} спальни\"")

if image_url:
    st.image(image_url, caption="Первая найденная картинка", use_column_width=True)
else:
    st.write("Картинка не найдена")

st.write("Ура! Вы подобрали для себя идеальную недвижимость!")

if st.button("Отпразднуем!"):
    audio_file = open('Music.mp3', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes)
