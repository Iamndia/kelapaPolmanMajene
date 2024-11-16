import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import folium 
from streamlit_folium import st_folium
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score



st.title("Hasil Clustering Kelapa Polewali Mandar dan Majene")
st.markdown("<hr>", unsafe_allow_html=True)

# Sidebar Title yang Terpusat
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 24px; color: #FFFFFFFF; font-weight: bold; font-family: Arial;">
        Kelapa Polewali Mandar dan Majene
    </div> <hr>
    """, 
    unsafe_allow_html=True
)
st.sidebar.page_link("halamanutama.py", label="Halamana Utama")
st.sidebar.page_link("pages/kelapa.py", label="Kelapa Kecamatan ")
# Garis pemisah
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Membaca dataset dari file Excel
df = pd.read_excel("kelapaKecamatan.xlsx")
x = df.iloc[:, [4, 5]].values

st.header("Isi Dataset")
# st.write(df)
st.markdown(df.to_html(classes='styled-table'), unsafe_allow_html=True)


# Elbow method untuk menentukan jumlah cluster yang tepat
clusters = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(x)
    clusters.append(kmeans.inertia_)

# Plot Elbow
st.subheader("Elbow Method")
fig1, ax1 = plt.subplots(figsize=(12, 8))
sns.lineplot(x=list(range(1, 11)), y=clusters, ax=ax1)
ax1.set_title("Mencari Elbow")
ax1.set_xlabel("Clusters")
ax1.set_ylabel("Inertia")
st.pyplot(fig1)

# Normalisasi data
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

st.sidebar.subheader("Nilai jumlah K")
clust = st.sidebar.slider("Pilih Jumlah Cluster ", 2, 10, 3, 1)

# Proses K-Means Clustering dengan jumlah cluster berdasarkan slider
kmeans = KMeans(n_clusters=clust, init='k-means++', random_state=42)
df['Cluster'] = kmeans.fit_predict(x_scaled)
# Menghitung Metrik Evaluasi
silhouette_avg = silhouette_score(x_scaled, df['Cluster'])
calinski_harabasz = calinski_harabasz_score(x_scaled, df['Cluster'])
davies_bouldin = davies_bouldin_score(x_scaled, df['Cluster'])

# Menampilkan Metrik Evaluasi di Sidebar
st.sidebar.subheader("Metrik Evaluasi Clustering")
st.sidebar.metric(label="Silhouette Score", value=round(silhouette_avg, 3))
st.sidebar.metric(label="Calinski-Harabasz Index", value=round(calinski_harabasz, 3))
st.sidebar.metric(label="Davies-Bouldin Index", value=round(davies_bouldin, 3))

# Mengubah nama kolom untuk lebih rapi
df.columns = df.columns.str.strip()

# Membagi hasil clustering ke dalam tiga kategori: Rendah, Sedang, Tinggi
cluster_labels = ['Rendah', 'Sedang', 'Tinggi']
clusters_split = np.array_split(range(clust), 3)

cluster_mapping = {}
for idx, split in enumerate(clusters_split):
    for cluster_id in split:
        cluster_mapping[cluster_id] = cluster_labels[idx]

# Mapping cluster numerik ke kategori
df['Cluster'] = df['Cluster'].map(cluster_mapping)

# Mapping warna berdasarkan cluster
cluster_colors = {'Rendah': 'green', 'Sedang': 'blue', 'Tinggi': 'red'}

# Membuat plot scatter
st.subheader("Plot Clustering")
fig2, ax2 = plt.subplots(figsize=(20, 6))
sns.scatterplot(x='Kecamatan', y='PRODUKTIVITAS (Kg/Ha/Thn)', hue='Cluster', palette=cluster_colors, s=150, data=df, ax=ax2)
ax2.set_title("Hasil Clustering")
ax2.set_xlabel("Kecamatan")
ax2.set_ylabel("PRODUKTIVITAS (Kg/Ha/Thn)")
st.pyplot(fig2)

st.header("Hasil Cluster")
# st.write(df)
st.markdown(df.to_html(classes='styled-table'), unsafe_allow_html=True)

# Menampilkan Peta dengan hasil pengelompokan
st.subheader("Peta Hasil Pengelompokan")
map_loc = folium.Map(location=[df['latitude'].mean(), df['longtitude'].mean()], zoom_start=8)
for idx, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longtitude']], 
        tooltip=f"Kecamatan {row['Kecamatan']} (Cluster: {row['Cluster']})",
        icon=folium.Icon(color=cluster_colors[row['Cluster']])
    ).add_to(map_loc)
st_folium(map_loc, width=700)

# Custom CSS untuk mengubah warna latar belakang
st.markdown(
    """
    <style>
    body {
        background-color: #020249FF;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }
    .stApp {
        background-color: #02023EFF;
    }
    [data-testid="stSidebarContent"] {
    background-color: #04046BB9;
    }
    .st.sidebar.title{
    text-align: center; 
    font-weight: bold; 
    font-style: italic;
    color: #4CAF50; 
    font-family: "Courier New", Courier, monospace; font-size: 28px;
    }
    .styled-table {
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 12px;
        text-align: left;
        width: 100%;
    }
    .styled-table thead tr {
        background-color: #009879;
        color: #ffffff;
        text-align: center;
    }
    header {visibility: hidden;}
    .css-1y4p8pa.e1fqkh3o0 {visibility: hidden;}
    
    </style>
    """,
    unsafe_allow_html=True
)
