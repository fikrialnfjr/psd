import streamlit as st
from prediction import performPrediction
from map_view import show_map
from eda import show_eda

st.set_page_config(layout="wide", page_title="FSVA Intelligence", page_icon="🌾")

# Sidebar: branding & informasi
with st.sidebar:
    st.markdown("## 🌾 FSVA Intelligence")
    st.caption("Dashboard Interaktif dan Prediksi Ketahanan Pangan Indonesia")

    st.markdown("""
    Aplikasi ini dirancang untuk:
    - **Memonitor** ketahanan pangan tiap wilayah
    - **Mengeksplorasi** trend rata-rata ketahanan pangan nasional dan indikator ketahanan pangan antar provinsi
    - **Memprediksi** status berdasarkan input indikator
    - **Memberikan rekomendasi** kebijakan berbasis data
    """)

    st.markdown("### ℹ️ Cara Menggunakan")
    st.info("""
    1. Telusuri dan klik wilayah pada peta untuk melihat detail indikator.
    2. Buka tab **Eksplorasi Data (EDA)** untuk:
        - Melihat **trend rata-rata skor komposit nasional** dari 2020–2024.
        - Menjelajahi **5 provinsi tertinggi** pada masing-masing indikator utama.
    3. Untuk memprediksi status ketahanan pangan suatu wilayah, buka tab **Prediksi Ketahanan Pangan** dan isi nilai indikatornya.
    4. Dapatkan hasil prediksi dan saran kebijakan berbasis data.
    """)

    st.markdown("---")
    st.markdown("#### 👨‍💻 Developer")
    st.markdown("""
    - **Fikri Alinfijar**  
    📧 fikrialnfjr@student.telkomuniversity.ac.id

    - **Muhammad Zaki Nur Rahman**  
    📧 zakinurrahman@student.telkomuniversity.ac.id

    - **Muhammad Fauzal Dwiansyah**  
    📧 anchaidris@student.telkomuniversity.ac.id

    - **Muhammad Faris Al Ghifari**  
    📧 farisalgi@student.telkomuniversity.ac.id
    """)

# Judul Aplikasi
st.markdown("""
<div style="padding: 1.2rem; border-radius: 12px; background: linear-gradient(to right, #C8E6C9, #A8E6CF); text-align: center; color: #254433;">
    <h1 style="margin-bottom: 0;">🌾 FSVA Intelligence 🌾</h1>
    <p style="margin-top: 0;">Dashboard Interaktif dan Prediksi Ketahanan Pangan Indonesia</p>
</div>
""", unsafe_allow_html=True)

# Header 2 Map Ketahanan Pangan
st.markdown("")
st.markdown("""
<div style='text-align: center; margin-bottom: 1rem;'>
    <h2>🗺️ Map Ketahanan Pangan Kota/Kabupaten di Indonesia</h2>
</div>
""", unsafe_allow_html=True)
show_map()

# Header 2 Prediksi dan EDA
st.markdown("""
<div style='text-align: center; margin-bottom: 1rem;'>
    <h2>📊 Eksplorasi & Prediksi Ketahanan Pangan</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Eksplorasi Data (EDA)", "🤖 Prediksi Ketahanan Pangan"])

with tab1:
    show_eda()

with tab2:
    performPrediction()
