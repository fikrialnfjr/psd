import streamlit as st
from prediction import performPrediction
from map_view import show_map
from eda import show_eda

st.set_page_config(layout="wide", page_title="FSVA Intelligence", page_icon="🌾")

st.markdown("""
<style>
.section-header {
  display: flex;
  align-items: center;
  margin: 2rem 0 1.5rem;
}
.section-header .accent {
  width: 6px;
  height: 40px;
  background: linear-gradient(135deg, #A8E6CF, #C8E6C9);
  border-radius: 4px;
  margin-right: 0.75rem;
}
.section-header h2 {
  margin: 0;
  font-family: 'GlacialIndifference', sans-serif;
  font-size: 1.75rem;
  font-weight: 700;
  color: #213a2d;
}
</style>
""", unsafe_allow_html=True)

# Sidebar: branding & informasi
with st.sidebar:
    st.markdown("## 🌾 FSVA Intelligence 🌾")
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
<style>
.header-banner {
  padding: 1.5rem 2rem;
  border-radius: 12px;
  background: linear-gradient(135deg, #A8E6CF 0%, #C8E6C9 100%);
  color: #062917;
  text-align: center;
  box-shadow: 0 8px 20px rgba(0,0,0,0.1);
  font-family: 'GlacialIndifference', sans-serif;
  position: relative;
  overflow: hidden;
}
.header-banner::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(255,255,255,0.3), transparent 70%);
  transform: rotate(25deg);
}
.header-banner h1 {
  margin: 0;
  font-size: 2.5rem;
  font-weight: 800;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.15);
}
.header-banner p {
  margin: 0.5rem 0 0;
  font-size: 1rem;
  opacity: 0.85;
}
</style>

<div class="header-banner">
  <h1>🌾 FSVA Intelligence 🌾</h1>
  <p>Dashboard Interaktif dan Prediksi Ketahanan Pangan Indonesia</p>
</div>
""", unsafe_allow_html=True)


# Header 2 Map Ketahanan Pangan
st.markdown("")
st.markdown("""
<div class="section-header">
  <div class="accent"></div>
  <h2>🗺️ Map Ketahanan Pangan Kota/Kabupaten di Indonesia</h2>
</div>
""", unsafe_allow_html=True)
show_map()

# Header 2 Prediksi dan EDA
st.markdown("""
<div class="section-header">
  <div class="accent"></div>
  <h2>📊 Eksplorasi & Prediksi Ketahanan Pangan</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📈 Eksplorasi Data (EDA)", "🤖 Prediksi Ketahanan Pangan"])

with tab1:
    show_eda()

with tab2:
    performPrediction()
