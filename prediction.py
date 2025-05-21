import streamlit as st
import joblib
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import html
import re

load_dotenv()

# ——— LOAD API & INISIALISASI LLM —————————
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    streaming=True
)

template = """
Anda adalah seorang ahli ketahanan pangan dan kebijakan publik.

Berikut adalah indikator dari suatu daerah yang belum memenuhi batas aman:

{context}

Berikan saran kebijakan yang rinci dan dapat diimplementasikan oleh pemerintah daerah untuk memperbaiki kondisi tersebut. 

Sertakan:
- Dampak jika tidak diperbaiki
- Intervensi yang bisa dilakukan pemerintah
- Contoh konkrit jika ada

Gunakan bahasa yang mudah dipahami oleh pemangku kebijakan daerah.

Note: 
1. **NCPR (Normative Consumption Production Ratio)** – menunjukkan rasio antara konsumsi pangan normatif dan produksi pangan lokal. Nilai tinggi menandakan defisit produksi lokal.
2. **Persentase Kemiskinan** – mencerminkan daya beli masyarakat. Makin tinggi nilainya, makin sulit masyarakat menjangkau pangan.
3. **Proporsi Pengeluaran untuk Pangan** – semakin tinggi proporsi ini, semakin besar tekanan ekonomi rumah tangga untuk mencukupi pangan dasar.
4. **Persentase Rumah Tangga Tanpa Listrik** – mewakili keterbatasan infrastruktur dasar yang berdampak pada akses pangan dan kualitas hidup.
5. **Persentase Rumah Tangga Tanpa Akses Air Bersih** – sangat berpengaruh pada keamanan pangan dan kesehatan keluarga.
6. **Lama Sekolah Perempuan** – digunakan sebagai proksi untuk kualitas pengelolaan pangan dalam rumah tangga dan status gizi anak.
7. **Rasio Penduduk per Tenaga Kesehatan** – mengukur akses layanan kesehatan. Semakin kecil rasio, semakin baik pelayanan dan pemantauan gizi (semakin sedikit jumlah penduduk yang ditangani oleh satu tenaga kesehatan).
8. **Angka Harapan Hidup** – mencerminkan kondisi kesehatan umum masyarakat.
9. **Prevalensi Stunting Balita** – indikator langsung dari pemanfaatan pangan dan status gizi anak di wilayah tersebut.
"""
prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(llm=llm, prompt=prompt)

# ——— WARNA UNTUK SETIAP KOMPOSIT —————————
komposit_colors = {
    1: "#a50026",
    2: "#d73027",
    3: "#f46d43",
    4: "#fdae61",
    5: "#a6d96a",
    6: "#1a9850"
}

# ——— FUNGSI MUAT MODEL —————————————
def load_model(model_choice):
    if model_choice == "SVM":
        model_file = "best_svm_model.pkl"
    elif model_choice == "Random Forest":
        model_file = "random_forest_classifier_best_with_smote.pkl"
    else:
        st.error("Model tidak valid!")
        return None
    return joblib.load(model_file)

# ——— FUNGSI UTAMA —————————————
def performPrediction():
    # 1) Form input
    with st.form("prediction_form"):
        model_choice = st.selectbox("**Pilih Model**", ("SVM", "Random Forest"))
        st.write("**Masukkan Nilai Variabel Kota/Kabupaten Anda**")
        col1, col2, col3 = st.columns(3)
        with col1:
            NCPR = st.number_input('NCPR', value=0.0)
            Tanpa_Listrik = st.number_input('Tanpa Listrik (%)', value=0.0)
            Rasio_Tenaga_Kesehatan = st.number_input('Rasio Tenaga Kesehatan', value=0.0)
        with col2:
            Kemiskinan = st.number_input('Kemiskinan (%)', value=0.0)
            Tanpa_Air_Bersih = st.number_input('Tanpa Air Bersih (%)', value=0.0)
            Angka_Harapan_Hidup = st.number_input('Angka Harapan Hidup (tahun)', value=0.0)
        with col3:
            Pengeluaran_Pangan = st.number_input('Pengeluaran Pangan (%)', value=0.0)
            Lama_Sekolah_Perempuan = st.number_input('Lama Sekolah Perempuan (tahun)', value=0.0)
            Stunting = st.number_input('Stunting (%)', value=0.0)

        submitted = st.form_submit_button("Lakukan Prediksi")

    # 2) Proses ketika submit
    if submitted:
        # validasi input wajib, tapi hanya tunjukkan yang belum diisi
        missing_fields = []
        if Lama_Sekolah_Perempuan <= 0:
            missing_fields.append("**`Lama Sekolah Perempuan (tahun)`**")
        if Angka_Harapan_Hidup <= 0:
            missing_fields.append("**`Angka Harapan Hidup (tahun)`**")
        if Rasio_Tenaga_Kesehatan <= 0:
            missing_fields.append("**`Rasio Tenaga Kesehatan`**")

        if missing_fields:
            # format string: "A dan B" atau "A, B, dan C"
            if len(missing_fields) == 1:
                fields_str = missing_fields[0]
            else:
                fields_str = ", ".join(missing_fields[:-1]) + " dan " + missing_fields[-1]

            st.warning(f"⚠️ Mohon isi nilai untuk: {fields_str}.")
            return

        # siapkan dataframe
        user_data = {
            'NCPR': NCPR,
            'Kemiskinan (%)': Kemiskinan,
            'Pengeluaran Pangan (%)': Pengeluaran_Pangan,
            'Tanpa Listrik (%)': Tanpa_Listrik,
            'Tanpa Air Bersih (%)': Tanpa_Air_Bersih,
            'Lama Sekolah Perempuan (tahun)': Lama_Sekolah_Perempuan,
            'Rasio Tenaga Kesehatan': Rasio_Tenaga_Kesehatan,
            'Angka Harapan Hidup (tahun)': Angka_Harapan_Hidup,
            'Stunting (%)': Stunting
        }
        df = pd.DataFrame([user_data])

        # muat dan prediksi
        model_dict = load_model(model_choice)
        if model_dict:
            scaler = model_dict["scaler"]
            model = model_dict["model"]
            X_scaled = scaler.transform(df)
            pred = model.predict(X_scaled)[0]

            desc = {
                1: "Sangat Rentan",
                2: "Rentan",
                3: "Agak Rentan",
                4: "Agak Tahan",
                5: "Tahan",
                6: "Sangat Tahan"
            }.get(pred, "N/A")

            message = f"Hasil Prediksi Status Ketahanan Pangan: {pred} ({desc})"
            color = komposit_colors.get(pred, "#d1e7dd")

            # simpan ke session_state
            st.session_state["prediction_message"] = message
            st.session_state["prediction_color"] = color

            # siapkan rekomendasi threshold
            thresholds = {
                'NCPR': 0.75,
                'Kemiskinan (%)': 15,
                'Pengeluaran Pangan (%)': 20,
                'Tanpa Listrik (%)': 20,
                'Tanpa Air Bersih (%)': 40,
                'Lama Sekolah Perempuan (tahun)': 9,
                'Rasio Tenaga Kesehatan': 10,
                'Angka Harapan Hidup (tahun)': 67,
                'Stunting (%)': 29
            }
            recs = []
            for var, th in thresholds.items():
                val = user_data[var]
                if var in ['Lama Sekolah Perempuan (tahun)', 'Angka Harapan Hidup (tahun)']:
                    if val < th:
                        recs.append(f"{var}: {val} (disarankan ≥ {th})")
                else:
                    if val > th:
                        recs.append(f"{var}: {val} (disarankan ≤ {th})")
            st.session_state["recommendations"] = recs

    # 3) Render ulang hasil prediksi tepat di BAWAH form
    if "prediction_message" in st.session_state:
        st.markdown(
            f'''
            <div style="
                background-color: {st.session_state["prediction_color"]};
                padding: 0.75rem 1.25rem;
                border-radius: 0.25rem;
                color: white;
                font-weight: 600;
                font-size: 1rem;
            ">
                {st.session_state["prediction_message"]}
            </div>
            ''',
            unsafe_allow_html=True
        )
        st.markdown("")

    # 4) Tampilkan rekomendasi threshold dan tombol LLM
    if st.session_state.get("recommendations"):
        text_recs = "\n".join(f"- {r}" for r in st.session_state["recommendations"])
        st.info(
            f"**Catatan: Untuk meningkatkan ketahanan pangan, perhatikan nilai-nilai berikut:**\n\n"
            f"{text_recs}"
        )

        if st.button("Meminta Saran dari LLM"):
            ctx = "\n".join(st.session_state["recommendations"])
            with st.spinner("Sedang menghasilkan saran kebijakan..."):
                sug = llm_chain.run(context=ctx)
                st.session_state["llm_suggestion"] = sug

    # 5) Render ulang saran LLM jika ada
    if "llm_suggestion" in st.session_state:
        raw = st.session_state["llm_suggestion"]

        # 1) Escape HTML agar aman
        escaped = html.escape(raw)

        # 2) Markdown → HTML: bold **…**, italic *…*
        escaped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)


        # 3) Split per baris
        lines = escaped.split("\n")
        html_parts = []
        in_list = False

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("* "):
                # buka <ul> sekali saja
                if not in_list:
                    html_parts.append("<ul>")
                    in_list = True
                # isi <li>
                item = stripped[2:].strip()
                html_parts.append(f"<li>{item}</li>")
            else:
                # tutup list jika terbuka
                if in_list:
                    html_parts.append("</ul>")
                    in_list = False
                # jika kosong, skip
                if not stripped:
                    continue
                # jika judul/dibuat tebal manual (misal baris **Judul**:)
                html_parts.append(f"<p>{stripped}</p>")

        # tutup list di akhir jika perlu
        if in_list:
            html_parts.append("</ul>")

        safe = "\n".join(html_parts)

        # 4) Suntik CSS sekali saja
        st.markdown(
            """
            <style>
              .suggestion-card {
                background-color: #f7f7f7;
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                font-family: Arial, sans-serif;
                font-size: 15px;
                color: #333;
                line-height: 1.6;
                max-width: 800px;
                margin: 1.5rem auto;
              }
              .suggestion-card h4 {
                margin-top: 0;
                margin-bottom: 1rem;
                font-size: 1.2rem;
              }
              .suggestion-card ul {
                margin-left: 1.2rem;
                margin-bottom: 1rem;
              }
            </style>
            """,
            unsafe_allow_html=True
        )

        # 5) Render card—tinggi div akan otomatis sesuai isi
        st.markdown(
            f"""
            <div class="suggestion-card">
              {safe}
            </div>
            """,
            unsafe_allow_html=True
        )