import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title="ChemLab",
    page_icon="⚛️",
    layout="wide"
)

# ==========================
# LOAD DATA PERIODIK
# ==========================
@st.cache_data
def load_elements():
    url = "https://raw.githubusercontent.com/Bowserinator/Periodic-Table-JSON/master/PeriodicTableJSON.json"

    data = requests.get(url).json()["elements"]

    elements = []

    for e in data:
        elements.append({
            "number": e["number"],
            "symbol": e["symbol"],
            "name": e["name"],
            "category": e.get("category",""),
            "atomic_mass": e.get("atomic_mass",""),
            "xpos": e["xpos"],
            "ypos": e["ypos"]
        })

    return pd.DataFrame(elements)

# ==========================
# SIDEBAR
# ==========================
menu = st.sidebar.radio(
    "Menu",
    [
        "⚛️ Tabel Periodik",
        "🧪 Pembuatan Larutan",
        "💧 Pengenceran"
    ]
)

# ==========================
# TABEL PERIODIK
# ==========================
if menu == "⚛️ Tabel Periodik":

    st.title("⚛️ Tabel Periodik Unsur")

    df = load_elements()

    warna = {
        "alkali metal":"#ff6666",
        "alkaline earth metal":"#ffdead",
        "transition metal":"#ffc0c0",
        "post-transition metal":"#cccccc",
        "metalloid":"#cccc99",
        "nonmetal":"#a0ffa0",
        "halogen":"#ffff99",
        "noble gas":"#c0ffff",
        "lanthanide":"#ffbfff",
        "actinide":"#ff99cc"
    }

   st.markdown("""
<style>

.periodic-table{
    display:grid;
    grid-template-columns:repeat(18,60px);
    gap:4px;
}

.element{
    height:60px;
    border-radius:8px;
    text-align:center;
    padding:4px;
    color:black;
    font-weight:bold;
}

.number{
    font-size:10px;
}

.symbol{
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

html = '<div class="periodic-table">'

for periode in range(1,8):

    for golongan in range(1,19):

        match = df[
            (df["xpos"] == golongan)
            &
            (df["ypos"] == periode)
        ]

        if not match.empty:

            unsur = match.iloc[0]

            warna_unsur = warna.get(
                str(unsur["category"]).lower(),
                "#eeeeee"
            )

            html += f"""
            <div class="element"
            style="background:{warna_unsur}">
                <div class="number">
                    {unsur['number']}
                </div>

                <div class="symbol">
                    {unsur['symbol']}
                </div>
            </div>
            """

        else:
            html += "<div></div>"

html += "</div>"

st.markdown(
    html,
    unsafe_allow_html=True
)

                else:
                    st.write("")

    st.divider()

    st.subheader("Cari Unsur")

    cari = st.text_input(
        "Masukkan simbol unsur"
    )

    if cari:

        hasil = df[
            df["symbol"].str.upper()
            ==
            cari.upper()
        ]

        if not hasil.empty:

            unsur = hasil.iloc[0]

            st.success(
                f"{unsur['name']} ({unsur['symbol']})"
            )

            st.write(
                "Nomor Atom:",
                unsur["number"]
            )

            st.write(
                "Massa Atom:",
                unsur["atomic_mass"]
            )

            st.write(
                "Kategori:",
                unsur["category"]
            )

# ==========================
# PEMBUATAN LARUTAN
# ==========================
elif menu == "🧪 Pembuatan Larutan":

    st.title("🧪 Pembuatan Larutan")

    tab1, tab2 = st.tabs([
        "Molaritas",
        "Normalitas"
    ])

    # MOLARITAS
    with tab1:

        st.latex(
            r"M=\frac{m}{Mr}\times\frac{1000}{V}"
        )

        M = st.number_input(
            "Molaritas (M)",
            min_value=0.0
        )

        Mr = st.number_input(
            "Mr",
            min_value=0.0
        )

        V = st.number_input(
            "Volume (mL)",
            min_value=0.1
        )

        if st.button(
            "Hitung Massa"
        ):

            massa = (
                M * Mr * V
            ) / 1000

            st.success(
                f"Massa zat = {massa:.4f} gram"
            )

    # NORMALITAS
    with tab2:

        st.latex(
            r"N=\frac{m}{Mr\times valensi}\times\frac{1000}{V}"
        )

        N = st.number_input(
            "Normalitas",
            min_value=0.0
        )

        Mr2 = st.number_input(
            "Mr Zat",
            min_value=0.0
        )

        valensi = st.number_input(
            "Valensi",
            min_value=1
        )

        V2 = st.number_input(
            "Volume Larutan (mL)",
            min_value=0.1
        )

        if st.button(
            "Hitung Massa Normalitas"
        ):

            massa = (
                N *
                Mr2 *
                valensi *
                V2
            ) / 1000

            st.success(
                f"Massa zat = {massa:.4f} gram"
            )

# ==========================
# PENGENCERAN
# ==========================
elif menu == "💧 Pengenceran":

    st.title("💧 Pengenceran Larutan")

    st.latex(
        r"M_1V_1=M_2V_2"
    )

    M1 = st.number_input(
        "M1",
        min_value=0.0
    )

    M2 = st.number_input(
        "M2",
        min_value=0.0
    )

    V2 = st.number_input(
        "V2 (mL)",
        min_value=0.1
    )

    if st.button(
        "Hitung V1"
    ):

        if M1 > 0:

            V1 = (
                M2 * V2
            ) / M1

            st.success(
                f"V1 = {V1:.2f} mL"
            )

            st.info(
                f"Tambahkan pelarut hingga volume akhir {V2:.2f} mL"
            )
