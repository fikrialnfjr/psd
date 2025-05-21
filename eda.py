import streamlit as st
import pandas as pd
import plotly.express as px

def show_eda():
    # ===================== TREND KOMPOSIT NASIONAL =====================
    st.markdown("### Trend Rata-Rata Komposit Nasional (2020–2024)")
    trend_df = pd.read_csv("trend fsva.csv")

    fig_trend = px.line(
        trend_df,
        x="Tahun",
        y="Komposit",
        markers=True,
        title="Rata-Rata Skor Komposit Nasional per Tahun",
        labels={"Komposit": "Rata-Rata Komposit", "Tahun": "Tahun"},
        text="Komposit"  # untuk menampilkan nilai
    )

    fig_trend.update_traces(
        line=dict(color="#9DC08B"),
        marker=dict(color="#9DC08B"),
        textposition="top center",
        mode="lines+markers+text"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    with st.expander("Penjelasan Trend Komposit"):
        st.markdown("""
        Skor komposit menggambarkan tingkat ketahanan pangan suatu wilayah berdasarkan berbagai indikator seperti 
        kemiskinan, stunting, air bersih, pendidikan, dan lainnya.

        - Rentang skor berkisar antara **1 (Sangat Rentan)** hingga **6 (Sangat Tahan)**.
        - Pada 2020–2021 rata-rata nasional stabil di **5.05**.
        - Sedikit penurunan terjadi di 2022 (**5.04**) namun kembali naik menjadi **5.17** di 2023 dan **5.21** di 2024.
        - Artinya, secara umum ketahanan pangan nasional **mengalami peningkatan bertahap** dalam 5 tahun terakhir.
        - Namun peningkatan kecil juga menunjukkan bahwa **masih ada wilayah rentan** yang perlu diperkuat.
        """)

    # ===================== EKSPLORASI PER PROVINSI =====================
    st.markdown("### Eksplorasi 5 Provinsi Tertinggi per Indikator")

    df = pd.read_csv("fsva.csv")
    df["Provinsi"] = df["Wilayah"].apply(lambda x: x.split("-")[0].strip().title())

    indikator_cols = [
        "NCPR", "Kemiskinan (%)", "Pengeluaran Pangan (%)",
        "Tanpa Listrik (%)", "Tanpa Air Bersih (%)", "Lama Sekolah Perempuan (tahun)",
        "Rasio Tenaga Kesehatan", "Angka Harapan Hidup (tahun)", "Stunting (%)"
    ]
    df_mean = df.groupby("Provinsi")[indikator_cols].mean().reset_index()

    def render_chart(col, indikator, penjelasan):
        with col:
            df_sorted = df_mean.sort_values(by=indikator, ascending=False).head(5).reset_index(drop=True)
            warna_biru = ["#3C7E45", "#709F73", "#9BBA98", "#C4D4BC", "#EDEEDF"]
            df_sorted["warna"] = warna_biru[:len(df_sorted)]

            fig = px.bar(
                df_sorted,
                x=indikator,
                y="Provinsi",
                orientation="h",
                color="warna",
                color_discrete_map="identity",
                title=f"5 Provinsi Tertinggi - {indikator}",
                labels={indikator: indikator, "Provinsi": "Provinsi"},
                height=400
            )

            fig.update_layout(coloraxis_showscale=False)
            fig.update_yaxes(categoryorder='total ascending')
            st.plotly_chart(fig, use_container_width=True)

            with st.expander(f"Penjelasan {indikator}"):
                st.markdown(penjelasan)

    # ================= Baris 1 =================
    with st.container():
        col1, col2, col3 = st.columns(3)
        render_chart(col1, "NCPR", """
            **NCPR (Normative Consumption Production Ratio)** mengukur perbandingan antara kebutuhan konsumsi pangan normatif penduduk 
            dengan ketersediaan produksi pangan lokal (beras, jagung, ubi, sagu).

            - **NCPR > 1** artinya kebutuhan konsumsi lebih tinggi daripada produksi, atau wilayah mengalami **defisit pangan**.
            - **Semakin tinggi** NCPR → makin besar ketergantungan terhadap distribusi dari luar wilayah.
            - Nilai ideal adalah **< 1**, karena menunjukkan ketersediaan pangan cukup atau surplus.
        """)
        render_chart(col2, "Kemiskinan (%)", """
            **Kemiskinan (%)** menunjukkan persentase penduduk yang hidup di bawah garis kemiskinan nasional.

            - Semakin tinggi nilai ini, semakin banyak penduduk yang **tidak mampu membeli pangan bergizi dan layak**.
            - Kemiskinan sangat berkaitan dengan **kerentanan terhadap kelaparan dan malnutrisi**.
            - Indikator ini mencerminkan keterjangkauan ekonomi terhadap pangan.
        """)
        render_chart(col3, "Pengeluaran Pangan (%)", """
            **Pengeluaran Pangan (%)** adalah persentase pengeluaran rumah tangga untuk kebutuhan pangan dari total pengeluaran.

            - Nilai yang tinggi menunjukkan **ketergantungan ekonomi terhadap pangan sangat besar**.
            - Ketika terlalu besar, **kebutuhan lain seperti pendidikan, kesehatan, dan tempat tinggal bisa terabaikan**.
            - Biasanya menunjukkan **kerentanan terhadap inflasi harga pangan**.
        """)

    # ================= Baris 2 =================
    with st.container():
        col1, col2, col3 = st.columns(3)
        render_chart(col1, "Tanpa Listrik (%)", """
            Persentase rumah tangga yang **tidak memiliki akses terhadap listrik**.

            - Listrik diperlukan untuk **penyimpanan makanan (kulkas), penerangan, serta akses informasi gizi dan kesehatan**.
            - Wilayah tanpa listrik juga berpotensi memiliki **akses terbatas ke layanan publik dan pendidikan**.
            - Merupakan indikator **kerentanan infrastruktur dasar**.
        """)
        render_chart(col2, "Tanpa Air Bersih (%)", """
            Persentase rumah tangga **tanpa akses ke sumber air bersih yang terlindung** (sumur terlindung, pipa bersih, dll).

            - Air bersih penting untuk **memasak, minum, dan sanitasi**.
            - Tanpa air bersih → risiko penyakit meningkat → **pemanfaatan pangan tidak optimal**.
            - Salah satu indikator utama dalam menilai **ketahanan pangan berbasis sanitasi**.
        """)
        render_chart(col3, "Lama Sekolah Perempuan (tahun)", """
            Rata-rata lama sekolah perempuan usia dewasa di suatu wilayah.

            - Perempuan dengan pendidikan lebih tinggi memiliki **kemampuan lebih baik dalam merawat keluarga dan memilih pangan bergizi**.
            - Korelasi kuat dengan **penurunan stunting, peningkatan kesehatan keluarga**, dan pengelolaan anggaran rumah tangga.
        """)

    # ================= Baris 3 =================
    with st.container():
        col1, col2, col3 = st.columns(3)
        render_chart(col1, "Rasio Tenaga Kesehatan", """
            Perbandingan antara jumlah penduduk dengan jumlah tenaga kesehatan (dokter, perawat, bidan).

            - **Semakin tinggi rasio**, berarti **tenaga kesehatan terbatas** untuk melayani masyarakat.
            - Wilayah ini rawan **kurangnya penyuluhan gizi, imunisasi, dan layanan kesehatan dasar**.
            - Mempengaruhi **efektivitas pemanfaatan pangan untuk mencegah gizi buruk**.
        """)
        render_chart(col2, "Angka Harapan Hidup (tahun)", """
            Estimasi rata-rata usia hidup penduduk dari sejak lahir.

            - Semakin tinggi, menandakan **tingkat kesejahteraan, layanan kesehatan, dan gizi yang baik**.
            - Wilayah dengan harapan hidup tinggi menunjukkan **manfaat jangka panjang dari sistem pangan yang stabil**.
        """)
        render_chart(col3, "Stunting (%)", """
            Persentase balita yang mengalami **stunting** (tinggi badan lebih pendek dari standar usianya).

            - Merupakan indikator **gizi kronis jangka panjang**.
            - Mencerminkan **kualitas pangan, kebersihan, sanitasi, dan pola asuh**.
            - Nilai tinggi mengindikasikan kegagalan sistem ketahanan pangan dan gizi anak.
        """)
