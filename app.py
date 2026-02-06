import streamlit as st
import pandas as pd
import re
import folium
from streamlit_folium import st_folium
import plotly.express as px

st.set_page_config(page_title="Dashboard PBB Desa", layout="wide")

#SIDEBAR
st.sidebar.title("📍 Pilih Desa")

desa = st.sidebar.selectbox(
    "Desa",
    ["Girimukti", "Jatihurip", "Jatimulya", "Kebonjati", "Kotakaler", "Margamukti", "Mekarjaya", "Mulyasari", "Padasuka", "Rancamulya", "Sinarmulya", "Situ", "Talun"]
)

#KONFIGURASI PERDESA
DESA_CONFIG = {
    "Girimukti": {
        "file": "Data_pbb_girimukti.xlsx",
        "coords": {
            "BL BOJONGLOA": (-6.854545, 107.892548),
            "BL CIWARU": (-6.859631, 107.893494),
            "BL CIHONJE": (-6.850278, 107.899630),
            "BL CIHANYIR": (-6.845271, 107.882677),
            "BL CIBAROS": (-6.852445, 107.891989),
            "BL SUKALUYU": (-6.849713, 107.899360),
            "BL BINONG": (-6.849733, 107.883586),
            "JL RAYA GIRIMUKTI": (-6.851681, 107.899424),
            "BL JAMBAN": (-6.855669, 107.896548),
            "BL.BOJONGLOA": (-6.854266, 107.891165),
        }
    },
    "Jatihurip": {
        "file": "Data_pbb_jatihurip.xlsx",
        "coords": {
            "KO JATIHURIP KENCANA": (-6.812769, 107.921842),
            "JL DESA": (-6.823954, 107.925024),
            "BL GUNUNGKERUD": (-6.824471, 107.927172),
            "BL SINDANGMULYA": (-6.824888, 107.923880),
            "BL GADOG": (-6.820793, 107.929881),
            "KOMPLEK JATIHURIP": (-6.811540, 107.922201),
            "BL SINDANGSEHAT": (-6.820643, 107.928068),
            "BL SINDANGRENAH": (-6.813403, 107.924382),
            "BL CIAKAR": (-6.825077, 107.922751),
            "PERUM SINDANG AMANAH": (-6.821661, 107.928207),
        }
    },
    "Jatimulya": {
        "file": "Data_pbb_jatimulya.xlsx",
        "coords": {
            "Ko Asabri": (-6.812014, 107.908539),
            "Jl Prabu Gajah Agung": (-6.828306, 107.919279),
            "Bl Rancamulya": (-6.815333, 107.914125),
            "Jl Sindangtaman": (-6.813677, 107.909153),
            "Bl Santiong": (-6.824615, 107.913337),
            "Bl Sindangwangi": (-6.816572, 107.907228),
            "Bl Sindangtaman": (-6.812979, 107.907799),
            "Bl Randu": (-6.8222321, 107.911240),
            "Bl Cileuweng": (-6.824354, 107.916546),
            "Perum Banyu Biru": (-6.811902, 107.915200),
        }
    },
    "Kebonjati": {
        "file": "Data_pbb_kebonjati.xlsx",
        "coords": {
            "Bl Rahayu": (-6.827663,107.936037),
            "Jl Desa": (-6.829082,107.935672),
            "Jl Raya Bandung - Cirebon": (-6.833829,107.933172),
            "Bl Cimayor": (-6.833829,107.934762),
            "Bl Bojongjati": (-6.827397, 107.936043),
            "Bl Samoja": (-6.829819, 107.936437),
            "Bl Sukakerta": (-6.824670, 107.936199),
            "Bl Cikuningan": (-6.816214, 107.935626),
            "Bl Seren": (-6.822689, 107.938577),
            "Bl Giriharja": (-6.831321, 107.929995),
        }
    },
    "Kotakaler": {
        "file": "Data_pbb_kotakaler.xlsx",
        "coords": {
            "Jln Mayor AbdulRahman": (-6.837450, 107.928574),
            "Jl Mayor AbduRachman": (-6.843551, 107.925255),
            "Jl Tampomas": (-6.844464, 107.925651),
            "Jl Sebelas Afril": (-6.847528, 107.925663),
            "Bl Cipadung": (-6.844011, 107.928351),
            "Bl Ketib": (-6.842009, 107.929008),
            "Blok Dano": (-6.837085, 107.934987),
            "Jl Ketib": (-6.842942, 107.927846),
            "Ko Dano Permai": (-6.835666, 107.933052),
            "Blok Gorowong": (-6.845392, 107.932558),
        }
    },
    "Margamukti": {
        "file": "Data_pbb_margamukti.xlsx",
        "coords": {
            "JL SERMAMUHTAR": (-6.838716, 107.909258),
            "JL KALAPADUA": (-6.834550, 107.903190),
            "BL KALAPADUA": (-6.836018, 107.902324),
            "BL CIBAYAWAK": (-6.830763, 107.902394),
            "BL CIKILAT": (-6.832952, 107.908241),
            "BL BINGLU": (-6.830997, 107.899702),
            "BL RANCA": (-6.829450, 107.894476),
            "BL KERETEG": (-6.827686, 107.897739),  
            "BL CILIMUS": (-6.821328, 107.892235),
            "BL NAGOK": (-6.824978, 107.889805),
        }
    },
    "Mekarjaya": {
        "file": "Data_pbb_mekarjaya.xlsx",
        "coords": {
            "JL PRABU GAJAH AGUNG": (-6.835501, 107.917757),
            "PERUM VILL GARDEN": (-6.832940, 107.912915),
            "KO MEKARSARI": (-6.836690, 107.912786),
            "BL BENTENG": (-6.820062, 107.901756),
            "BL PANYIRAPAN": (-6.827167, 107.909285),
            "BL CISEMPUR": (-6.821627, 107.906541),
            "PERUM IBNU SINA": (-6.832082, 107.914448),
            "JL MEKARJAYA": (-6.824772, 107.905170),  
            "BUMI MEKARJAYA INDAH": (-6.832456, 107.910909),
            "PERUM MEKARSARI REGENCY ": (-6.834558, 107.912439),
        }
    },
    "Mulyasari": {
        "file": "Data_pbb_mulyasari.xlsx",
        "coords": {
            "BL NANGGEWER": (-6.838921, 107.899326),
            "BL BARANANGSIANG": (-6.832499, 107.894350),
            "BL GUNUNGMANIK": (6.834464, 107.893257),
            "BL KADUPUGUR": (-6.839834, 107.885598),
            "BL CINUNUK": (6.842187, 107.897200),
            "BL NAGKAPANDAK": (-6.840306, 107.884874),
            "BL PASIREURIH": (6.844036, 107.887749),
            "BL PASIRBULUH": (-6.837569, 107.886141),  
            "JL PASIRSANTEN": (-6.836940, 107.897140),
            "BL CINYINDANG SAWAH": (-6.833002, 107.889200),
        }
    },
    "Mulyasari": {
        "file": "Data_pbb_mulyasari.xlsx",
        "coords": {
            "BL NANGGEWER": (-6.838921, 107.899326),
            "BL BARANANGSIANG": (-6.832499, 107.894350),
            "BL GUNUNGMANIK": (-6.834464, 107.893257),
            "BL KADUPUGUR": (-6.839834, 107.885598),
            "BL CINUNUK": (-6.842187, 107.897200),
            "BL NAGKAPANDAK": (-6.840306, 107.884874),
            "BL PASIREURIH": (-6.844036, 107.887749),
            "BL PASIRBULUH": (-6.837569, 107.886141),  
            "JL PASIRSANTEN": (-6.836940, 107.897140),
            "BL CINYINDANG SAWAH": (-6.833002, 107.889200),
        }
    },
    "Padasuka": {
        "file": "Data_pbb_padasuka.xlsx",
        "coords": {
            "BL KUTAMAYA": (-6.844802, 107.907257),
            "JL RAYA PADASUKA": (-6.848042, 107.904650),
            "BL PANGJELERAN": (-6.851355, 107.909848),
            "BL CIPANGBUANGAN": (-6.854235, 107.901173),
            "BL NYANGENGGENG": (-6.854231, 107.900141),
            "BL BOJONGGAWUL": (-6.854183, 107.898569),
            "BL CAUMANGGALA": (-6.841187, 107.903616),
            "KP PANGJELERAN": (-6.849506, 107.905713),  
            "BL KUPA TONGGOH": (-6.850200, 107.900536),
            "KP CIBITUNG ": (-6.845586, 107.901975),
        }
    },
    "Rancamulya": {
        "file": "Data_pbb_rancamulya.xlsx",
        "coords": {
            "JL SUMEDANG-WADO ": (-6.846302, 107.940850),
            "JL DESA": (-6.846536, 107.936322),
            "JL RANCAMULYA DANO ": (-6.841820, 107.937514),
            "BL GARUNGGANG": (-6.841491, 107.937869),
            "BL RAMUGENCEL": (-6.854053, 107.932964),
            "BL TAMIANG": (-6.850965, 107.936059),
            "BL GOROWONG": (-6.842261, 107.942527),
            "BL BUDAKIR": (-6.846286, 107.938617), 
            "BL MUNCANG": (-6.847975, 107.946110),
            "BL CANGKUANG": (-6.851646, 107.938948),
        }
    },
    "Sinarmulya": {
        "file": "Data_pbb_sirnamulya.xlsx",
        "coords": {
            "BL GELEWING": (-6.838389, 107.876996),
            "BL CIWINDU": (-6.840776, 107.873184),
            "BL LEGOK": (-6.834720, 107.883965),
            "BL CIBAROS": (-6.840831, 107.876277),
            "BL BINONG": (-6.845828, 107.872871),
            "BL SAMURAT": (-6.834441, 107.869979),
            "BL PASIRKIBODAS": (-6.850052, 107.869736),
            "BL CIBITUNG": (-6.845272, 107.871499),  
            "BL KADUPUGUR": (-6.842518, 107.887960),
            "JL DESA": (-6.842156, 107.875957),
        }
    },
    "Situ": {
        "file": "Data_pbb_situ.xlsx",
        "coords": {
            "JL. PARABU GAJAH AGUNG": (-6.835787, 107.917025),
            "JL PRABU GAJAH AGUNG": (-6.832146, 107.926308),
            "BL KARAPYAK": (-6.834372, 107.918222),
            "JL PANGADUAN HEUBEUL": (-6.830716, 107.910840),
            "JL ANGGREK": (-6.833090, 107.923380),
            "BL ANGGREK": (-6.835535, 107.925218),
            "BL WAKAP": (-6.843901, 107.919900),
            "BL CIPEUTEUY": (-6.844512, 107.917615), 
            "JL SERMAMUHTAR": (-6.845581, 107.921925),
            "BL PANYINGKIRAN": (-6.844457, 107.923860),
        }
    },
    "Talun": {
        "file": "Data_pbb_talun.xlsx",
        "coords": {
            " BL TALUN KIDUL": (-6.854846, 107.930058),
            "BL TEGALSARI": (-6.848999, 107.930364),
            "JL SEBELAS APRIL": (-6.848258, 107.929235),
            "BL TALUN TENGAH": (-6.849081, 107.927955),
            "JL TALUN KIDUL": (-6.853235, 107.926938),
            "JL TALUN": (-6.848857, 107.925701),
            "JL TALUN KALER": (-6.848605, 107.926492),
            "BL SUKALUYU": (-6.851428, 107.925034),
            "TALUN KIDUL": (-6.852504, 107.929049),
            "LINGK.TALUN KIDUL": (-6.853657, 107.928240),
        }
    },
}

config = DESA_CONFIG[desa]

#LOAD DATA
df = pd.read_excel(config["file"])
df["PBB"] = pd.to_numeric(df["PBB"], errors="coerce")
df = df.dropna(subset=["Jalan OP", "PBB"])

#NORMALISASI DAN KOORDINAT
def norm(s: str):
    s = str(s).lower()
    s = re.sub(r"[^a-z0-9 ]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

coords_norm = {norm(k): v for k, v in config["coords"].items()}

def attach_coord(jalan_op: str):
    j = norm(jalan_op)
    for key, (lat, lon) in coords_norm.items():
        if key.replace(" ", "") in j.replace(" ", ""):
            return lat, lon
    return None, None

#INSIGHT TOP 10
top10 = (
    df.groupby("Jalan OP", as_index=False)
      .agg(
          total_pbb=("PBB", "sum"),
          jumlah_record=("PBB", "count"),
          
      )
      .sort_values("total_pbb", ascending=False)
      .head(10)
)

top10[["lat", "lon"]] = top10["Jalan OP"].apply(
    lambda x: pd.Series(attach_coord(x))
)

#UI
st.title(f"📊 Dashboard PBB Desa {desa}")
st.caption("Top 10 Jalan dengan Total PBB Terbesar")

# KPI
c1, c2, c3 = st.columns(3)
c1.metric("Total Record", f"{len(df):,}")
c2.metric("Total Jalan Unik", f"{df['Jalan OP'].nunique():,}")
c3.metric("Total PBB", f"{df['PBB'].sum():,.0f}")

st.divider()

#TABEL & GRAFIK
def format_rupiah(x):
    return f"Rp {x:,.0f}".replace(",", ".")

left, right = st.columns([1.2, 1])

with left:
    st.subheader("🏆 Top 10 Jalan")

    top10_display = top10.copy()
    top10_display["total_pbb"] = top10_display["total_pbb"].apply(format_rupiah)

    st.dataframe(top10_display, use_container_width=True)


with right:
    st.subheader("📈 Grafik Total PBB")

    top10_sorted = top10.sort_values("total_pbb", ascending=True)

    fig = px.bar(
        top10_sorted,
        x="total_pbb",
        y="Jalan OP",
        orientation="h",
        text=top10_sorted["total_pbb"].apply(format_rupiah)
    )

    fig.update_traces(textposition="outside")
    fig.update_yaxes(autorange="reversed") 
    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)



st.divider()

#GIS
st.subheader("🗺️ Peta GIS")

valid_map = top10.dropna(subset=["lat", "lon"])

if valid_map.empty:
    st.warning("Tidak ada data koordinat yang cocok.")
else:
    m = folium.Map(
        location=[valid_map["lat"].mean(), valid_map["lon"].mean()],
        zoom_start=13
    )

    for _, row in valid_map.iterrows():
        popup = f"""
        <b>{row['Jalan OP']}</b><br>
        Total PBB: {row['total_pbb']:,.0f}<br>
        Jumlah Record: {row['jumlah_record']}
        
        """
        folium.Marker(
            [row["lat"], row["lon"]],
            popup=popup,
            tooltip=row["Jalan OP"],
            icon=folium.Icon(color="red", icon="map-marker", prefix="fa")
        ).add_to(m)

    st_folium(m, width=1200, height=500)

st.divider()

#VALIDASI KOORDINAT
st.subheader("✅ Jalan Tanpa Koordinat")
missing = top10[top10["lat"].isna()][["Jalan OP", "total_pbb"]]

if missing.empty:
    st.success("Semua Top 10 jalan punya koordinat ✅")
else:
    st.warning("Beberapa jalan belum punya koordinat:")
    st.dataframe(missing, use_container_width=True)

st.divider()

#DATA SEMUA
st.subheader(f"📄 Data Lengkap PBB Desa {desa}")
st.dataframe(
    df.sort_values("PBB", ascending=False),
    use_container_width=True
)