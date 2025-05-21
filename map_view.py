import streamlit as st
import streamlit.components.v1 as components
import os

def show_map():
    html_path = "peta_komposit_per_wilayah.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_data = f.read()

        components.html(html_data, height=700, scrolling=False)

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.error("❌ File peta tidak ditemukan. Jalankan generate_map.py terlebih dahulu.")
