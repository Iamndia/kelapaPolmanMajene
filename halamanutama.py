import streamlit as st

st.set_page_config(
    page_title="Kelapa Sulbar",
    # initial_sidebar_state="auto"
)
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

st.title("Selamat Datang di Aplikasi Potensi Kelapa Sulawesi Barat")
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
    background-color: #020249B9;
    }
    header {visibility: hidden;}
    .css-1y4p8pa.e1fqkh3o0 {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)