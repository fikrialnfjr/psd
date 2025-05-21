import streamlit as st
import streamlit.components.v1 as components
import os

# Path ke file HTML peta yang sudah ada di folder
LOCAL_HTML_PATH = "peta_komposit_per_wilayah.html"

def show_map():
    # Cek eksistensi file
    if not os.path.exists(LOCAL_HTML_PATH):
        st.error(f"❌ File peta tidak ditemukan: {LOCAL_HTML_PATH}")
        return

    try:
        # Baca HTML
        with open(LOCAL_HTML_PATH, "r", encoding="utf-8") as f:
            html_data = f.read()

        # Tampilkan
        components.html(
            html_data,
            height=700,
            scrolling=True  # bisa diganti False jika tidak ingin scroll bar
        )
    except Exception as e:
        st.error(f"❌ Gagal menampilkan peta: {e}")
