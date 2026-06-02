import streamlit as st
import pandas as pd
import joblib
import time
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Sistem Rekomendasi Karir Industri AI Vinix 7",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Animasi splash screen hanya saat pertama kali buka
if "first_load" not in st.session_state:
    st.session_state["first_load"] = True
    components.html("""
    <script>
    (function () {
        const parent = window.parent;
        const doc    = parent.document;

        // Buat elemen overlay splash
        const splash = doc.createElement('div');
        splash.id = 'vinix-splash';
        splash.innerHTML = `
            <div class="splash-bg"></div>
            <div class="splash-content">
                <div class="splash-logo">
                    <div class="logo-ring ring-1"></div>
                    <div class="logo-ring ring-2"></div>
                    <img src="data:image/jpeg;base64,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" class="logo-img" alt="Vinix7" />
                </div>
                <div class="splash-sub">AI Career Intelligence System</div>
                <div class="splash-bar-wrap">
                    <div class="splash-bar"></div>
                </div>
                <div class="splash-loading-text">Memuat sistem analisis karir...</div>
            </div>
        `;

        // Inject CSS
        const style = doc.createElement('style');
        style.textContent = `
            #vinix-splash {
                position: fixed;
                inset: 0;
                z-index: 9999999;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            }

            .splash-bg {
                position: absolute;
                inset: 0;
                background: #050a14;
                background-image:
                    radial-gradient(ellipse 80% 60% at 50% -10%, rgba(10,132,255,0.35) 0%, transparent 70%),
                    radial-gradient(ellipse 50% 40% at 80% 100%, rgba(48,209,88,0.15) 0%, transparent 60%);
            }

            .splash-content {
                position: relative;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0;
                animation: splashFadeIn 0.6s ease forwards;
            }

            @keyframes splashFadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to   { opacity: 1; transform: translateY(0); }
            }

            /* Logo animasi cincin berputar */
            .splash-logo {
                position: relative;
                width: 90px;
                height: 90px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 28px;
            }

            .logo-ring {
                position: absolute;
                border-radius: 50%;
                border: 2px solid transparent;
            }
            .ring-1 {
                width: 90px; height: 90px;
                border-top-color: #0a84ff;
                border-right-color: rgba(10,132,255,0.3);
                animation: spinRing 1.4s linear infinite;
            }
            .ring-2 {
                width: 68px; height: 68px;
                border-bottom-color: #30d158;
                border-left-color: rgba(48,209,88,0.3);
                animation: spinRing 1.0s linear infinite reverse;
            }
            .ring-3 {
                width: 46px; height: 46px;
                border-top-color: rgba(255,159,10,0.8);
                border-right-color: rgba(255,159,10,0.2);
                animation: spinRing 1.8s linear infinite;
            }
            .logo-img {
                width: 110px;
                height: 110px;
                object-fit: contain;
                border-radius: 18px;
                position: relative;
                z-index: 2;
                animation: pulseStar 2s ease-in-out infinite;
                filter: drop-shadow(0 0 18px rgba(10,132,255,0.5));
            }

            @keyframes spinRing {
                to { transform: rotate(360deg); }
            }
            @keyframes pulseStar {
                0%, 100% { opacity: 1;   transform: scale(1); }
                50%       { opacity: 0.6; transform: scale(0.85); }
            }

            .splash-title {
                font-size: 3.2rem;
                font-weight: 900;
                letter-spacing: 0.35em;
                color: #ffffff;
                text-shadow: 0 0 40px rgba(10,132,255,0.6);
                margin-bottom: 8px;
            }

            .splash-sub {
                font-size: 0.85rem;
                font-weight: 400;
                letter-spacing: 0.25em;
                text-transform: uppercase;
                color: rgba(255,255,255,0.45);
                margin-bottom: 40px;
            }

            /* Progress bar */
            .splash-bar-wrap {
                width: 200px;
                height: 3px;
                background: rgba(255,255,255,0.1);
                border-radius: 99px;
                overflow: hidden;
                margin-bottom: 16px;
            }
            .splash-bar {
                height: 100%;
                width: 0%;
                background: linear-gradient(90deg, #0a84ff, #30d158);
                border-radius: 99px;
                animation: fillBar 2.2s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            @keyframes fillBar {
                0%   { width: 0%; }
                60%  { width: 75%; }
                85%  { width: 90%; }
                100% { width: 100%; }
            }

            .splash-loading-text {
                font-size: 0.78rem;
                color: rgba(255,255,255,0.3);
                letter-spacing: 0.05em;
                animation: blinkText 1.2s ease-in-out infinite;
            }
            @keyframes blinkText {
                0%, 100% { opacity: 0.3; }
                50%       { opacity: 0.7; }
            }

            /* Animasi keluar */
            #vinix-splash.hiding {
                animation: splashOut 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
            }
            @keyframes splashOut {
                0%   { opacity: 1; transform: scale(1); }
                100% { opacity: 0; transform: scale(1.04); }
            }
        `;

        doc.head.appendChild(style);
        doc.body.appendChild(splash);

        // Scroll ke atas
        parent.scrollTo({ top: 0, behavior: 'instant' });

        // Hilangkan splash setelah 2.8 detik
        setTimeout(() => {
            splash.classList.add('hiding');
            setTimeout(() => splash.remove(), 700);
        }, 2800);
    })();
    </script>
    """, height=0)

# ==========================================
# 2. CSS (PERBAIKAN: Hapus warna hardcode #ffffff,
#    gunakan CSS var() agar adaptif light/dark mode)
# ==========================================
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Background adaptif Streamlit */
    .stApp {
        background-image: radial-gradient(circle at 50% 0%, rgba(128,128,128,0.1) 0%, transparent 80%) !important;
    }

    /* PERBAIKAN: Teks mengikuti tema, bukan hardcode */
    h1, h2, h3, h4, p, label,
    .stMarkdown, .stText, .st-bb, .st-at, .stAlert p {
        color: var(--text-color) !important;
    }

    @keyframes zoomOutLoad {
        0%   { opacity: 0; transform: scale(1.04); }
        100% { opacity: 1; transform: scale(1); }
    }

    .main .block-container {
        padding: 3rem 4rem;
        animation: zoomOutLoad 0.6s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    }

    div[data-testid="stForm"] {
        background: rgba(128,128,128,0.08) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 28px;
        border: 1px solid rgba(128,128,128,0.15);
        box-shadow: 0 20px 60px rgba(0,0,0,0.05), inset 0 1px 0 rgba(255,255,255,0.2);
        padding: 3rem;
        margin-top: 1.5rem;
    }

    div[data-testid="stAlert"] {
        background: rgba(10,132,255,0.1) !important;
        backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(10,132,255,0.2);
        margin-bottom: 1.5rem;
    }

    /* Info box kompak satu baris */
    .compact-info {
        background: rgba(10,132,255,0.1);
        border: 1px solid rgba(10,132,255,0.2);
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        color: var(--text-color);
        line-height: 1.4;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: 2px;
        text-align: center;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        background: rgba(128,128,128,0.15) !important;
        backdrop-filter: blur(15px);
        border-radius: 14px !important;
        border: 1px solid rgba(128,128,128,0.2) !important;
        transition: all 0.3s ease;
    }

    input[aria-label="IPK Terakhir"] {
        text-align: center !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #0a84ff !important;
        box-shadow: 0 0 0 2px rgba(10,132,255,0.3) !important;
        background: rgba(128,128,128,0.25) !important;
    }

    .section-divider {
        border-top: 1px dashed rgba(128,128,128,0.3);
        margin: 2.5rem 0;
    }

    /* PERBAIKAN: Mencegah konflik passive touch event di mobile pada slider */
    div[data-testid="stSlider"],
    div[data-testid="stSlider"] > div,
    div[data-testid="stSlider"] [role="slider"],
    div[data-testid="stSlider"] [data-baseweb="slider"] {
        touch-action: none !important;
    }

    /* PERBAIKAN: Kolom kartu full-height agar equalizer bekerja */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
    }
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] > div {
        flex: 1;
        display: flex;
        flex-direction: column;
        min-height: 0;
    }

    .glass-card {
        background: rgba(128,128,128,0.06);
        backdrop-filter: blur(35px);
        -webkit-backdrop-filter: blur(35px);
        border-radius: 28px;
        padding: 40px;
        margin-bottom: 25px;
        border: 1px solid rgba(128,128,128,0.15);
        box-shadow: 0 15px 40px rgba(0,0,0,0.06), inset 0 1px 1px rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: zoomOutLoad 0.6s ease-out forwards;
        flex: 1;
        display: flex;
        flex-direction: column;
        box-sizing: border-box; /* PERBAIKAN: Mencegah overflow padding */
        min-height: 0;
    }

    .glass-card:hover {
        transform: translateY(-10px) scale(1.01);
        box-shadow: 0 25px 60px rgba(0,0,0,0.1), inset 0 1px 1px rgba(255,255,255,0.4);
        background: rgba(128,128,128,0.1);
        border: 1px solid rgba(128,128,128,0.2);
    }

    /* PERBAIKAN: Hapus color:#ffffff, gunakan inherit agar adaptif */
    .glass-card h3 {
        margin-top: 0;
        font-weight: 800;
        letter-spacing: -0.7px;
        font-size: 1.5rem;
        color: inherit !important;
        min-height: 3.8rem; /* pastikan score sejajar saat judul bisa dua baris */
        line-height: 1.2;
    }

    .card-body {
        flex: 1;
        display: flex;
        flex-direction: column;
    } /* PERBAIKAN: Wrapper isi kartu agar next-steps bisa auto ke bawah */

    .proper-title {
        opacity: 0.6;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }

    .proper-description {
        opacity: 0.85;
        font-size: 0.95rem;
        margin-top: 15px;
        line-height: 1.6;
    }

    /* PERBAIKAN: margin-top: auto mendorong box ke bawah kartu */
    .next-steps {
        background: rgba(128,128,128,0.1);
        border-radius: 12px;
        padding: 15px;
        margin-top: auto;
        border: 1px solid rgba(128,128,128,0.1);
    }
    .next-steps h5 { font-weight: 700; margin-top: 0; margin-bottom: 8px; }
    .next-steps ul  { list-style-type: disc; padding-left: 1.2rem; opacity: 0.85; font-size: 0.85rem; margin-bottom: 0; }

    div.stButton > button:first-child {
        background: #0a84ff;
        color: white !important;
        border: none;
        border-radius: 18px;
        padding: 1rem 2.5rem;
        font-size: 1.2rem;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(10,132,255,0.2);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        letter-spacing: -0.2px;
        margin-top: 1rem;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 10px 30px rgba(10,132,255,0.35);
        background: #007aff;
    }

    /* PERBAIKAN: Pesan validasi error */
    .validation-error {
        background: rgba(255, 59, 48, 0.12);
        border: 1px solid rgba(255, 59, 48, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        color: #ff3b30 !important;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    h1 {
        text-align: center;
        font-weight: 800;
        margin-bottom: 0.4rem;
        letter-spacing: -1.5px;
        font-size: 2.5rem;
    }

    .ai-badge {
        text-align: center;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #0a84ff !important;
        background: rgba(10,132,255,0.1);
        border: 1px solid rgba(10,132,255,0.25);
        border-radius: 99px;
        display: inline-block;
        padding: 4px 20px;
        margin: 0 auto 0.6rem auto;
        width: fit-content;
        left: 50%;
        position: relative;
        transform: translateX(-50%);
    }

    .subtitle {
        text-align: center;
        opacity: 0.6;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 3rem;
    }

    /* Custom IPK stepper — tombol pill terpisah */
    div[data-testid="stForm"] div.stButton > button[kind="secondaryFormSubmit"] {
        background: rgba(128,128,128,0.15) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(128,128,128,0.2) !important;
        border-radius: 12px !important;
        color: var(--text-color) !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        padding: 6px 0 !important;
        margin-top: 0 !important;
        box-shadow: none !important;
        transition: background 0.2s ease, border-color 0.2s ease;
        width: 100%;
    }
    div[data-testid="stForm"] div.stButton > button[kind="secondaryFormSubmit"]:hover {
        background: rgba(10,132,255,0.18) !important;
        border-color: rgba(10,132,255,0.4) !important;
        transform: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. LOAD MODEL (PERBAIKAN: Pesan error lebih informatif)
# ==========================================
@st.cache_resource(show_spinner=False)
def load_assets():
    required_files = [
        "model_lightgbm_vinix.pkl",
        "label_encoder_vinix.pkl",
        "fitur_model_vinix.pkl",
    ]
    missing = [f for f in required_files if not __import__("os").path.exists(f)]
    if missing:
        st.error(
            f"**File model tidak ditemukan:** `{'`, `'.join(missing)}`\n\n"
            "Pastikan file `.pkl` berada di direktori yang sama dengan `app.py`."
        )
        st.stop()
    try:
        model   = joblib.load("model_lightgbm_vinix.pkl")
        le      = joblib.load("label_encoder_vinix.pkl")
        fitur   = joblib.load("fitur_model_vinix.pkl")
        return model, le, fitur
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        st.stop()

model, label_encoder, fitur_blueprint = load_assets()


# ==========================================
# 4. FUNGSI HELPER
# ==========================================
def scale_to_15(val_100: float) -> float:
    """Ubah skala 1-100 (input user) menjadi 1-15 (skala latih model) secara linier."""
    return 1.0 + (float(val_100) - 1.0) * (14.0 / 99.0)


def map_jurusan(x: str) -> str:
    x = str(x).lower().strip()
    if x in ("nan", "none", "-", ""):
        return "Lainnya"
    if any(k in x for k in ["teknik", "informatika", "sistem", "komputer", "data",
                              "statistika", "matematika", "sains", "fisika", "it"]):
        return "STEM_Tech"
    if any(k in x for k in ["psikologi", "sastra", "hukum", "sosiologi", "hubungan"]):
        return "Soshum"
    if any(k in x for k in ["manajemen", "komunikasi", "ilmu komunikasi",
                              "bisnis", "ekonomi", "akuntansi"]):
        return "Bisnis_Komunikasi"
    if any(k in x for k in ["desain", "dkv", "seni", "visual"]):
        return "Seni_Kreatif"
    return "Lainnya"


def map_dream_job(x: str) -> str:
    x = str(x).lower().strip()
    if x in ("nan", "none", "-", ""):
        return "Industri Lainnya"
    if any(k in x for k in ["data", "software", "engineer", "developer",
                              "it", "tech", "programmer"]):
        return "Tech Data Engineering"
    if any(k in x for k in ["marketing", "content", "creative", "desain",
                              "writer", "copywriter"]):
        return "Creative Marketing"
    if any(k in x for k in ["finance", "bank", "analyst", "audit",
                              "akuntan", "invest"]):
        return "Finance Banking"
    if any(k in x for k in ["manager", "bisnis", "hr", "consultant",
                              "sales", "operasi"]):
        return "Business Management"
    return "Industri Lainnya"


def parse_magang(x: str) -> int:
    """Kembalikan 1 jika pernah magang, 0 jika belum."""
    return 0 if str(x).lower().strip() in ("-", "tidak", "belum", "none", "nan", "") else 1


def parse_semester(raw: str) -> int:
    """PERBAIKAN: Parsing semester dengan error handling eksplisit."""
    if raw == "Lulus (Alumni)":
        return 9
    try:
        return int(raw.replace("Semester ", "").strip())
    except ValueError:
        return 7  # fallback ke Semester 7


def detect_archetype(scores: dict) -> tuple[str, str, str]:
    """Deteksi archetype berdasarkan pola skor M1-M9 (Anti-Bug)."""
    if not scores:
        return "🔍 The Adaptive Explorer", "#bf5af2", "Data tidak ditemukan."
        
    total = sum(scores.values())
    avg   = total / len(scores)
    
    # CARA PALING AMAN: Cari nilai berdasarkan awalan "M1", "M2", dst.
    # str(k).upper() memastikan tidak ada masalah huruf besar/kecil
    m1 = next((v for k, v in scores.items() if "M1" in str(k).upper()), 50)
    m2 = next((v for k, v in scores.items() if "M2" in str(k).upper()), 50)
    m4 = next((v for k, v in scores.items() if "M4" in str(k).upper()), 50)
    m7 = next((v for k, v in scores.items() if "M7" in str(k).upper()), 50)
    m8 = next((v for k, v in scores.items() if "M8" in str(k).upper()), 50)
    
    # LOGIKA PENENTUAN ARCHETYPE
    if avg >= 70 and m8 >= 70 and m4 >= 70:
        return "🌟 The Visionary Leader", "#0a84ff", (
            "Anda memiliki visi kuat dan dorongan kepemimpinan yang tinggi. "
            "Kombinasi ambisi, passion, dan branding menjadikan Anda kandidat "
            "unggul untuk posisi strategis."
        )
    if m2 >= 70 and m1 >= 60:
        return "⚙️ The Result Driver", "#30d158", (
            "Profil Anda menonjol di sisi teknis dan eksekusi. Anda berorientasi "
            "hasil, andal dalam hard-skills, dan konsisten dalam penyelesaian tugas."
        )
    if m4 >= 70 and m7 >= 60:
        return "🎨 The Creative Innovator", "#ff9f0a", (
            "Passion yang tinggi dikombinasikan kemampuan personal branding yang kuat. "
            "Anda cocok di lingkungan yang menghargai ide segar dan ekspresi diri."
        )
        
    return "🔍 The Adaptive Explorer", "#bf5af2", (
        "Profil Anda menunjukkan fleksibilitas tinggi dan kemampuan adaptasi lintas "
        "domain. Kekuatan Anda ada di kemampuan menjembatani berbagai bidang."
    )


def hitung_kesiapan(scores: dict, ipk: float, magang: int,
                    interview: int, bahasa: int) -> tuple[int, str, str]:
    """Hitung skor kesiapan kerja keseluruhan (0-100) beserta label & warna."""
    avg_m = sum(scores.values()) / len(scores)
    skor  = (
        avg_m * 0.45
        + (ipk / 4.0 * 100) * 0.15
        + magang * 15
        + (interview / 5 * 100) * 0.15
        + (bahasa   / 5 * 100) * 0.10
    )
    skor = min(100, max(0, skor))
    if skor >= 75:
        return int(skor), "Sangat Siap", "#30d158"
    if skor >= 55:
        return int(skor), "Siap Masuk Industri", "#0a84ff"
    if skor >= 40:
        return int(skor), "Hampir Siap", "#ff9f0a"
    return int(skor), "Perlu Persiapan Lebih", "#ff3b30"


# ── Inisialisasi session state ──────────────────────────────────────────────
if "riwayat" not in st.session_state:
    st.session_state["riwayat"] = []
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None


# ── Sidebar navigasi ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div style="font-size:1.6rem;font-weight:900;letter-spacing:0.1em;
                    background:linear-gradient(135deg,#0a84ff,#30d158);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            VINIX 7
        </div>
        <div style="font-size:0.7rem;opacity:0.5;letter-spacing:0.2em;text-transform:uppercase;
                    margin-top:2px;">AI Career System</div>
    </div>
    <hr style="border:none;border-top:1px solid rgba(128,128,128,0.2);margin:0.8rem 0 1.2rem;">
    """, unsafe_allow_html=True)

    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = "🏠  Beranda & Analisis"

    page = st.radio(
        "Navigasi",
        ["🏠  Beranda & Analisis", "📊  Dashboard Hasil", "📋  Riwayat Sesi", "ℹ️  Tentang Sistem"],
        label_visibility="collapsed",
        key="nav_page"
    )

    st.markdown("<hr style='border:none;border-top:1px solid rgba(128,128,128,0.15);'>", unsafe_allow_html=True)
    n_riwayat = len(st.session_state["riwayat"])
    st.markdown(
        f"<div style='font-size:0.78rem;opacity:0.5;text-align:center;'>"
        f"Sesi ini: <strong>{n_riwayat}</strong> analisis tersimpan</div>",
        unsafe_allow_html=True,
    )
    if n_riwayat > 0 and st.button("🗑️ Hapus Semua Riwayat", use_container_width=True):
        st.session_state["riwayat"] = []
        st.session_state["last_result"] = None
        st.rerun()

# ==========================================
# 5. DATA DESKRIPSI INDUSTRI
# ==========================================
DESKRIPSI_MAP = {
    "Bidang Tech dan Digital": {
        "deskripsi": (
            "Profil menunjukkan ketertarikan kuat pada inovasi teknologi dan "
            "pemecahan masalah kompleks. Anda nyaman dengan adaptasi cepat dan "
            "efisiensi berbasis data."
        ),
        "steps": [
            "Lengkapi profil LinkedIn dengan kata kunci teknis (Git, Python, Agile).",
            "Bangun proyek portofolio yang relevan dengan posisi Tech yang diincar.",
            "Jajaki koneksi ke komunitas tech profesional.",
        ],
    },
    "Industri Kreatif dan Proyek": {
        "deskripsi": (
            "Model melihat bakat kuat dalam komunikasi visual, narasi, dan "
            "manajemen proyek dinamis. Lingkungan fleksibel dengan orisinalitas "
            "ide sangat sesuai dengan profil Anda."
        ),
        "steps": [
            "Perbarui portofolio karya Anda (Behance, Dribbble, Website).",
            "Ikuti tren terbaru industri Kreatif (AI Art, TikTok trends).",
            "Bangun koneksi dengan pekerja proyek dan Agency untuk kolaborasi.",
        ],
    },
    "Industri Konvensional Terstruktur": {
        "deskripsi": (
            "Skor menunjukkan etika kerja tinggi, menyukai kestabilan, dan unggul "
            "dalam prosedur yang jelas. Industri ini menawarkan jenjang karir yang pasti."
        ),
        "steps": [
            "Fokus pada sertifikasi soft skills komunikasi profesional.",
            "Tingkatkan kemampuan administrasi digital (Excel / Google Workspace).",
            "Jajaki peluang koneksi melalui jaringan Alumni di perusahaan besar.",
        ],
    },
}

DEFAULT_DESKRIPSI = {
    "deskripsi": "Profil kompetensi menunjukkan fleksibilitas tinggi dan kecocokan campuran antar industri.",
    "steps": [
        "Konsultasikan hasil ini dengan Pusat Karir kampus.",
        "Perkuat portofolio soft-skills Anda.",
    ],
}

ICON_MAP = {
    "Bidang Tech dan Digital":           "",
    "Industri Kreatif dan Proyek":       "",
    "Industri Konvensional Terstruktur": "",
}


# ==========================================
# 6. HEADER
# ==========================================
if page == "🏠  Beranda & Analisis":

 st.markdown("""
<h1>Sistem Rekomendasi Karir Industri</h1>
<p class='ai-badge'> Vinix 7</p>
<p class='subtitle'>Uji Kompetensi dan Pemetaan Karir Masa Depan Mahasiswa</p>
""", unsafe_allow_html=True)


 # ==========================================
 # 7. FORM INPUT
 # ==========================================
 with st.form("career_form"):

    # ── Bagian 1: Profil Akademik ──────────────────────────────────────
    st.markdown("### Profil Akademik")
    col1, col2 = st.columns(2)
    with col1:
        raw_jurusan = st.text_input(
            "Program Studi Anda",
            placeholder="Contoh: Teknik Informatika, Manajemen...",
            help="Ketikkan nama program studi lengkap Anda.",
        )
        val_magang_input = st.text_input(
            "Tempat Magang Sebelumnya",
            placeholder="Ketik '-' jika belum pernah magang",
            help="Isi nama perusahaan magang. Gunakan '-' jika belum pernah.",
        )
        # IPK terakhir dapat diubah manual melalui number input
        val_ipk = st.number_input(
            "IPK Terakhir",
            min_value=0.00,
            max_value=4.00,
            value=0.00,
            step=0.01,
            format="%.2f",
            help="Klik untuk mengubah angka IPK secara manual.",
        )
    with col2:
        raw_dream_job = st.text_input(
            "Pekerjaan Impian (Dream Job)",
            placeholder="Contoh: Data Scientist, HR Manager...",
            help="Isi pekerjaan spesifik yang Anda incar.",
        )
        raw_semester = st.selectbox(
            "Semester Saat Ini",
            options=[f"Semester {i}" for i in range(0, 9)] + ["Lulus (Alumni)"],
            index=1,
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── Bagian 2: Nilai Kerja (Work Values) ───────────────────────────
    st.markdown("### Nilai Kerja (Work Values)")
    st.markdown("""
    <div class="compact-info">
        <strong>Panduan Skala Nilai Kerja (1–100):</strong>
        &nbsp;&nbsp;
        <span><strong>1–33</strong> Kapasitas rendah</span> &nbsp;·&nbsp;
        <span><strong>34–66</strong> Kapasitas standar</span> &nbsp;·&nbsp;
        <span><strong>67–100</strong> Sangat menguasai</span>
        &nbsp;·&nbsp; <em>Minat Wirausaha menggunakan skala 1–5</em>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        skor_m1 = st.slider("Background",    1, 100, 50, help="Kesesuaian latar belakang pendidikan & pengalaman dengan karir impian.")
        skor_m4 = st.slider("Interest",      1, 100, 50, help="Seberapa besar passion Anda pada bidang pekerjaan yang diincar.")
        skor_m3 = st.slider("Industry Fit",  1, 100, 50, help="Kecocokan gaya kerja Anda dengan budaya industri / korporat.")
    with c2:
        skor_m5 = st.slider("Moral Compass", 1, 100, 50, help="Kekuatan etika kerja, integritas, dan komitmen penyelesaian tugas.")
        skor_wirausaha = st.slider("Minat Wirausaha", 1, 5, 2, help="1 = Karyawan profesional. 5 = Berminat startup/bisnis sendiri.")

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── Bagian 3: Gaya Kerja (Work Styles) ────────────────────────────
    st.markdown("### Gaya Kerja (Work Styles)")
    st.markdown("""
    <div class="compact-info">
        <strong>Panduan Skala Gaya Kerja (1–100):</strong>
        &nbsp;&nbsp;
        <span><strong>1–33</strong> Kapasitas rendah</span> &nbsp;·&nbsp;
        <span><strong>34–66</strong> Kapasitas standar</span> &nbsp;·&nbsp;
        <span><strong>67–100</strong> Sangat menguasai</span>
        &nbsp;·&nbsp; <em>Kesiapan Wawancara menggunakan skala 1–5</em>
    </div>
    """, unsafe_allow_html=True)

    c2a, c2b, c2c = st.columns(3)
    with c2a:
        skor_m2 = st.slider("Hard Skills",   1, 100, 50, help="Tingkat penguasaan teknis / hard-skill spesifik untuk bidang pekerjaan.")
        skor_m7 = st.slider("Branding",      1, 100, 50, help="Kemampuan memasarkan diri (CV, Portofolio, LinkedIn, Komunikasi profesional).")
    with c2b:
        skor_m8 = st.slider("Ambisi Karir",  1, 100, 50, help="Dorongan internal untuk mencapai target posisi/gaji dan kepemimpinan.")
        skor_m9 = st.slider("Resiliensi",    1, 100, 50, help="Daya tahan mental dalam menghadapi tekanan tinggi dan revisi pekerjaan.")
    with c2c:
        skor_m6 = st.slider("Adaptability",  1, 100, 50, help="Kemampuan beradaptasi terhadap perubahan lingkungan dan teknologi baru.")
        skor_interview = st.slider("Kesiapan Wawancara", 1, 5, 3, help="1 = Gugup dan belum siap. 5 = Sangat siap, percaya diri.")

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── Bagian 4: Preferensi Karir ─────────────────────────────────────
    st.markdown("### Preferensi Karir")
    st.markdown("""
    <div class="compact-info">
        Pilih kondisi dan preferensi lingkungan kerja yang paling sesuai dengan diri Anda saat ini.
    </div>
    """, unsafe_allow_html=True)

    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        jalur_karir = st.selectbox(
            "Jalur Karir yang Dipilih",
            options=["expand", "stay", "switch", "unsure"],
            format_func=lambda x: {
                "expand": "🚀 Expand – Kembangkan karir di bidang saat ini",
                "stay":   "🏠 Stay – Tetap di jalur dan jurusan yang sama",
                "switch": "🔀 Switch – Pindah jalur karir baru",
                "unsure": "❓ Unsure – Belum yakin arahnya",
            }[x],
            help="Pilih jalur karir yang paling menggambarkan rencana Anda ke depan.",
        )
        ukuran_perusahaan = st.selectbox(
            "Ukuran Perusahaan Ideal",
            options=["big", "mid", "startup", "flex"],
            format_func=lambda x: {
                "big":     "🏢 Korporat Besar (>500 karyawan)",
                "mid":     "🏬 Perusahaan Menengah (50–500)",
                "startup": "🚀 Startup / Scale-up (<50)",
                "flex":    "🔄 Fleksibel (tidak ada preferensi)",
            }[x],
            help="Ukuran perusahaan yang paling ideal untuk Anda.",
        )
    with cp2:
        work_style = st.selectbox(
            "Gaya Kerja (Work Style)",
            options=["flex", "big", "small", "solo"],
            format_func=lambda x: {
                "flex":  "🔄 Fleksibel – Adaptif di semua kondisi",
                "big":   "👥 Tim Besar – Senang kolaborasi lintas divisi",
                "small": "🤝 Tim Kecil – Dekat dan intim",
                "solo":  "🧘 Solo – Mandiri dan independen",
            }[x],
            help="Pilih gaya kerja yang paling nyaman untuk Anda.",
        )
        kultur_kerja = st.selectbox(
            "Kultur Kerja yang Disukai",
            options=["collab", "agile", "formal", "result"],
            format_func=lambda x: {
                "collab": "🤝 Collaborative – Kerja tim, saling support",
                "agile":  "⚡ Agile – Cepat, iteratif, dinamis",
                "formal": "👔 Formal – Terstruktur dan prosedural",
                "result": "🎯 Result-Oriented – Fokus output dan target",
            }[x],
            help="Pilih kultur kerja yang paling sesuai.",
        )
    with cp3:
        cognitive_style = st.selectbox(
            "Gaya Berpikir (Cognitive Style)",
            options=["analytical", "creative", "social", "strategic"],
            format_func=lambda x: {
                "analytical": "🔬 Analytical – Logis, berbasis data",
                "creative":   "🎨 Creative – Inovatif, out-of-the-box",
                "social":     "💬 Social – Empatik, people-oriented",
                "strategic":  "♟️ Strategic – Visioner, big picture",
            }[x],
            help="Pilih gaya berpikir yang paling dominan dalam diri Anda.",
        )
        preferensi_lokasi = st.selectbox(
            "Preferensi Lokasi Kerja",
            options=["hybrid", "onsite", "remote", "any"],
            format_func=lambda x: {
                "hybrid":  "🏡🏢 Hybrid – Kombinasi WFH & kantor",
                "onsite":  "🏢 Onsite – Full di kantor",
                "remote":  "🌐 Remote – Full kerja dari rumah",
                "any":     "🔄 Terserah – Tidak ada preferensi",
            }[x],
            help="Pilih preferensi lokasi kerja Anda.",
        )

    cp4, cp5 = st.columns(2)
    with cp4:
        motivasi = st.selectbox(
            "Motivasi Utama Bekerja",
            options=["growth", "money", "impact", "prestige", "freedom"],
            format_func=lambda x: {
                "growth":   "📈 Growth – Ingin terus berkembang & belajar",
                "money":    "💰 Money – Gaji dan finansial adalah prioritas",
                "impact":   "🌱 Impact – Ingin memberi dampak nyata",
                "prestige": "🏆 Prestige – Reputasi dan pengakuan penting",
                "freedom":  "🕊️ Freedom – Fleksibilitas dan otonomi kerja",
            }[x],
            help="Apa motivasi terbesar Anda dalam berkarir?",
        )

    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # ── Bagian 5: Pengembangan Diri ────────────────────────────────────
    st.markdown("### Pengembangan Diri")
    st.markdown("""
    <div class="compact-info">
        <strong>Panduan Skala (1–5):</strong>
        &nbsp;&nbsp;
        <span><strong>1</strong> Sangat rendah / Tidak sama sekali</span> &nbsp;·&nbsp;
        <span><strong>3</strong> Cukup / Standar</span> &nbsp;·&nbsp;
        <span><strong>5</strong> Sangat tinggi / Sangat aktif</span>
    </div>
    """, unsafe_allow_html=True)

    cd1, cd2, cd3, cd4 = st.columns(4)
    with cd1:
        ekspektasi_gaji = st.slider(
            "Ekspektasi Gaji",
            1, 5, 3,
            help="1 = Di bawah UMR. 3 = Standar industri. 5 = Sangat tinggi / kompetitif.",
        )
    with cd2:
        rencana_s2 = st.slider(
            "Rencana S2 / Sertifikasi",
            1, 5, 3,
            help="1 = Tidak ada rencana. 5 = Sudah ada rencana konkret dan segera.",
        )
    with cd3:
        frekuensi_belajar = st.slider(
            "Frekuensi Belajar Mandiri",
            1, 5, 3,
            help="1 = Jarang sekali belajar di luar kuliah. 5 = Belajar setiap hari secara aktif.",
        )
    with cd4:
        level_bahasa = st.slider(
            "Level Bahasa Inggris",
            1, 5, 3,
            help="1 = Pasif / sangat terbatas. 3 = Bisa berkomunikasi. 5 = Profesional / fasih.",
        )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Mulai Analisis Karir Saya", use_container_width=True)


 # ==========================================
 # 8. VALIDASI INPUT
 # ==========================================
 if submitted:
    errors = []
    if not raw_jurusan.strip():
        errors.append("Program Studi tidak boleh kosong.")
    if not raw_dream_job.strip():
        errors.append("Pekerjaan Impian tidak boleh kosong.")
    if not val_magang_input.strip():
        errors.append("Kolom Tempat Magang tidak boleh kosong (isi '-' jika belum pernah).")

    if errors:
        for err in errors:
            st.markdown(f"<div class='validation-error'>{err}</div>", unsafe_allow_html=True)
        st.stop()

    # ── Loading Overlay ─────────────────────────────────────────────────
    loading_slot = st.empty()
    loading_slot.markdown("""
        <div style="position:fixed;top:0;left:0;width:100vw;height:100vh;
                    background:rgba(0,0,0,0.85);backdrop-filter:blur(25px);
                    -webkit-backdrop-filter:blur(25px);z-index:999999;
                    display:flex;flex-direction:column;
                    justify-content:center;align-items:center;">
            <div style="width:60px;height:60px;border:4px solid rgba(10,132,255,0.2);
                        border-top:4px solid #0a84ff;border-radius:50%;
                        animation:spin 1s cubic-bezier(0.4,0,0.2,1) infinite;"></div>
            <h3 style="margin-top:24px;font-family:-apple-system,sans-serif;
                       color:#ffffff;font-weight:600;letter-spacing:-0.5px;">
                Menganalisis Profil...
            </h3>
            <p style="color:#8e8e93;font-size:14px;text-align:center;max-width:320px;">
                AI sedang melakukan kalkulasi normalisasi dan pencocokan model statistik Vinix 7
            </p>
        </div>
        <style>
            @keyframes spin {
                0%   { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)

    time.sleep(2.5)
    loading_slot.empty()

    # ── Preprocessing ────────────────────────────────────────────────────
    user_data = {
        # ── Profil Akademik ──────────────────────────
        "Program Studi":           map_jurusan(raw_jurusan),
        "Dream Job":               map_dream_job(raw_dream_job),
        "Semester":                parse_semester(raw_semester),
        "Tempat Magang":           parse_magang(val_magang_input),
        "IPK":                     val_ipk,
        # ── Nilai Kerja (Work Values) ────────────────
        "Skor M1 (Background)":    scale_to_15(skor_m1),
        "Skor M4 (Interest)":      scale_to_15(skor_m4),
        "Skor M3 (Industry)":      scale_to_15(skor_m3),
        "Skor M5 (Compass)":       scale_to_15(skor_m5),
        "Minat Wirausaha":         skor_wirausaha,
        # ── Gaya Kerja (Work Styles) ─────────────────
        "Skor M2 (Skills)":        scale_to_15(skor_m2),
        "Skor M7 (Branding)":      scale_to_15(skor_m7),
        "Skor M8 (Ambisi)":        scale_to_15(skor_m8),
        "Skor M9 (Resiliensi)":    scale_to_15(skor_m9),
        "Skor M6 (Adaptability)":  scale_to_15(skor_m6),
        "Kesiapan Interview":      skor_interview,
        # ── Preferensi Karir (FITUR BARU) ────────────
        "Jalur Karir":             jalur_karir,
        "Work Style":              work_style,
        "Cognitive Style":         cognitive_style,
        "Motivasi":                motivasi,
        "Ukuran Perusahaan":       ukuran_perusahaan,
        "Kultur Kerja":            kultur_kerja,
        "Preferensi Lokasi":       preferensi_lokasi,
        # ── Pengembangan Diri (FITUR BARU) ───────────
        "Ekspektasi Gaji":         ekspektasi_gaji,
        "Rencana S2/Sertifikasi":  rencana_s2,
        "Frekuensi Belajar":       frekuensi_belajar,
        "Level Bahasa Inggris":    level_bahasa,
    }

    df_input   = pd.DataFrame([user_data])
    df_encoded = pd.get_dummies(df_input)
    df_final   = df_encoded.reindex(columns=fitur_blueprint, fill_value=0)

    # ── Prediksi ─────────────────────────────────────────────────────────
    try:
        prediksi_proba = model.predict_proba(df_final)[0]
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses prediksi: {e}")
        st.stop()

    kelas_industri = label_encoder.classes_
    hasil_df = (
        pd.DataFrame({"Industri": kelas_industri, "Kecocokan": prediksi_proba * 100})
        .sort_values("Kecocokan", ascending=False)
        .reset_index(drop=True)
    )

    # ── Render Kartu Hasil ───────────────────────────────────────────────
    st.markdown(
        "<h2 id='hasil-prediksi' style='text-align:center;margin-bottom:2rem;margin-top:1rem;'>"
        "Analisis Kecocokan Industri Anda</h2>",
        unsafe_allow_html=True,
    )

    # Konfigurasi tiap kartu: label, warna skor, judul langkah
    CARD_CONFIG = [
        ("Rekomendasi Utama",  "#0a84ff", "2.0rem", "Langkah Kritis"),
        ("Alternatif Utama",   "#30d158", "2.0rem", "Langkah Jajakan"),
        ("Alternatif Kedua",   "#ff9f0a", "2.0rem", "Langkah Eksplorasi"),
    ]

    cols = st.columns([1, 1, 1])

    for i, col in enumerate(cols):
        if i >= len(hasil_df):
            break

        row        = hasil_df.iloc[i]
        industri   = row["Industri"]
        skor       = row["Kecocokan"]
        ikon       = ICON_MAP.get(industri, "💼")
        info       = DESKRIPSI_MAP.get(industri, DEFAULT_DESKRIPSI)
        label, warna, font_size, step_title = CARD_CONFIG[i]
        steps_html = "".join(f"<li>{s}</li>" for s in info["steps"])

        # PERBAIKAN: Kartu menggunakan var(--text-color) bukan #ffffff
        with col:
            st.markdown(f"""
            <div class="glass-card js-podium-card">
                <div class="card-body">
                    <p class="proper-title">{label}</p>
                    <h3>{industri}</h3>
                    <div style="font-size:{font_size};font-weight:800;color:{warna};white-space:nowrap;">
                        {skor:.1f}% Kesesuaian
                    </div>
                    <p class="proper-description">{info['deskripsi']}</p>
                </div>
                <div class="next-steps">
                    <h5>{step_title}:</h5>
                    <ul>{steps_html}</ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── JavaScript: Equalizer tinggi kartu & auto-scroll ─────────────────
    components.html("""
    <script>
    (function() {
        const parentDoc = window.parent.document;
        function equalizeHeights() {
            const cards = parentDoc.querySelectorAll('.js-podium-card');
            if (cards.length === 0) return;
            cards.forEach(c => c.style.height = 'auto');
            const maxH = Math.max(...[...cards].map(c => c.offsetHeight));
            cards.forEach(c => c.style.height = maxH + 'px');
        }
        function scrollToResults() {
            const target = parentDoc.getElementById('hasil-prediksi');
            if (target) { target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
        }
        setTimeout(() => { equalizeHeights(); scrollToResults(); }, 400);
        setTimeout(() => { equalizeHeights(); }, 900);
        const observer = new MutationObserver(equalizeHeights);
        observer.observe(parentDoc.body, { childList: true, subtree: true });
        window.parent.addEventListener('resize', equalizeHeights);
    })();
    </script>
    """, height=0)

    # ── Simpan ke session state & hitung metrik tambahan ──────────────
    raw_scores_100 = {
        "M1 Background":   skor_m1,  "M2 Hard Skills":  skor_m2,
        "M3 Industry Fit": skor_m3,  "M4 Interest":     skor_m4,
        "M5 Moral Compass":skor_m5,  "M6 Adaptability": skor_m6,
        "M7 Branding":     skor_m7,  "M8 Ambisi":       skor_m8,
        "M9 Resiliensi":   skor_m9,
    }
    archetype_label, archetype_color, archetype_desc = detect_archetype(raw_scores_100)
    kesiapan_skor, kesiapan_label, kesiapan_color = hitung_kesiapan(
        raw_scores_100, val_ipk, parse_magang(val_magang_input), skor_interview, level_bahasa
    )

    result_entry = {
        "waktu":           datetime.now().strftime("%H:%M:%S"),
        "jurusan":         raw_jurusan,
        "dream_job":       raw_dream_job,
        "hasil_df":        hasil_df.copy(),
        "scores":          raw_scores_100,
        "archetype":       archetype_label,
        "archetype_color": archetype_color,
        "archetype_desc":  archetype_desc,
        "kesiapan_skor":   kesiapan_skor,
        "kesiapan_label":  kesiapan_label,
        "kesiapan_color":  kesiapan_color,
        "ipk":             val_ipk,
        "semester":        raw_semester,
        "minat_wirausaha": skor_wirausaha,
        "interview":       skor_interview,
        "bahasa":          level_bahasa,
    }
    st.session_state["last_result"] = result_entry
    st.session_state["riwayat"].append(result_entry)

    # ── Tab Visualisasi Dashboard (inline) ─────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        "<h2 style='text-align:center;margin-bottom:1.5rem;'>📊 Dashboard Analitik</h2>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["🕸️ Radar Kompetensi", "📈 Skor Industri", "🧬 Profil Archetype"])

    with tab1:
        categories = list(raw_scores_100.keys())
        values     = list(raw_scores_100.values())
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(10,132,255,0.15)",
            line=dict(color="#0a84ff", width=2.5),
            name="Kompetensi Anda",
            hovertemplate="%{theta}: %{r:.0f}/100<extra></extra>",
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10),
                                gridcolor="rgba(128,128,128,0.2)", linecolor="rgba(128,128,128,0.2)"),
                angularaxis=dict(gridcolor="rgba(128,128,128,0.15)", linecolor="rgba(128,128,128,0.2)"),
                bgcolor="rgba(0,0,0,0)",
            ),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=60, r=60, t=40, b=40),
            height=420,
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Skor kesiapan kerja
        st.markdown(f"""
        <div style="background:rgba(128,128,128,0.07);border-radius:18px;padding:20px 28px;
                    border:1px solid rgba(128,128,128,0.15);margin-top:0.5rem;">
            <div style="opacity:0.55;font-size:0.8rem;font-weight:600;text-transform:uppercase;
                        letter-spacing:0.5px;margin-bottom:6px;">Skor Kesiapan Kerja Keseluruhan</div>
            <div style="font-size:2.4rem;font-weight:900;color:{kesiapan_color};">
                {kesiapan_skor}<span style="font-size:1rem;font-weight:600;opacity:0.6;">/100</span>
                &nbsp; <span style="font-size:1.1rem;">{kesiapan_label}</span>
            </div>
            <div style="background:rgba(128,128,128,0.15);border-radius:99px;height:6px;margin-top:10px;">
                <div style="background:{kesiapan_color};width:{kesiapan_skor}%;height:100%;
                            border-radius:99px;transition:width 1s ease;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        fig_bar = go.Figure()
        colors_bar = ["#0a84ff", "#30d158", "#ff9f0a"]
        for idx, (_, row_b) in enumerate(hasil_df.iterrows()):
            fig_bar.add_trace(go.Bar(
                x=[row_b["Kecocokan"]],
                y=[row_b["Industri"]],
                orientation="h",
                marker_color=colors_bar[idx % len(colors_bar)],
                text=[f"{row_b['Kecocokan']:.1f}%"],
                textposition="outside",
                hovertemplate=f"{row_b['Industri']}: %{{x:.1f}}%<extra></extra>",
                name=row_b["Industri"],
            ))
        fig_bar.update_layout(
            barmode="overlay",
            xaxis=dict(range=[0, 105], title="Tingkat Kecocokan (%)",
                       gridcolor="rgba(128,128,128,0.15)", showgrid=True),
            yaxis=dict(title="", tickfont=dict(size=13)),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=60, t=20, b=40),
            height=280,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Tabel detail skor
        st.markdown("**Rincian Skor per Kompetensi**")
        score_rows = []
        for label_s, val_s in raw_scores_100.items():
            if val_s >= 70:   status = "🟢 Unggulan"
            elif val_s >= 45: status = "🟡 Standar"
            else:             status = "🔴 Perlu Ditingkatkan"
            score_rows.append({"Kompetensi": label_s, "Skor": f"{val_s}/100", "Status": status})
        st.dataframe(pd.DataFrame(score_rows), use_container_width=True, hide_index=True)

    with tab3:
        arc_col1, arc_col2 = st.columns([1, 2])
        with arc_col1:
            st.markdown(f"""
            <div style="background:rgba(128,128,128,0.07);border-radius:20px;padding:28px 20px;
                        border:1px solid rgba(128,128,128,0.15);text-align:center;height:100%;">
                <div style="font-size:3rem;margin-bottom:12px;">
                    {archetype_label.split()[0]}
                </div>
                <div style="font-size:1rem;font-weight:800;color:{archetype_color};
                            margin-bottom:6px;line-height:1.3;">
                    {" ".join(archetype_label.split()[1:])}
                </div>
                <div style="opacity:0.55;font-size:0.78rem;text-transform:uppercase;
                            letter-spacing:0.5px;">Archetype Karir</div>
            </div>
            """, unsafe_allow_html=True)
        with arc_col2:
            st.markdown(f"""
            <div style="background:rgba(128,128,128,0.07);border-radius:20px;padding:24px 28px;
                        border:1px solid rgba(128,128,128,0.15);">
                <div style="opacity:0.55;font-size:0.78rem;font-weight:600;text-transform:uppercase;
                            letter-spacing:0.5px;margin-bottom:10px;">Deskripsi Archetype</div>
                <p style="font-size:0.95rem;line-height:1.65;margin:0;">{archetype_desc}</p>
                <hr style="border:none;border-top:1px solid rgba(128,128,128,0.15);margin:16px 0;">
                <div style="display:flex;gap:20px;flex-wrap:wrap;">
                    <div><div style="opacity:0.5;font-size:0.75rem;">IPK</div>
                         <div style="font-weight:700;">{val_ipk:.2f}</div></div>
                    <div><div style="opacity:0.5;font-size:0.75rem;">Semester</div>
                         <div style="font-weight:700;">{raw_semester}</div></div>
                    <div><div style="opacity:0.5;font-size:0.75rem;">Minat Wirausaha</div>
                         <div style="font-weight:700;">{skor_wirausaha}/5</div></div>
                    <div><div style="opacity:0.5;font-size:0.75rem;">Bahasa Inggris</div>
                         <div style="font-weight:700;">{level_bahasa}/5</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Tips berdasarkan skor terendah
        st.markdown("<br>", unsafe_allow_html=True)
        skor_sorted = sorted(raw_scores_100.items(), key=lambda x: x[1])
        weak_areas  = skor_sorted[:3]
        tips_map = {
            "M1 Background":    "Perkuat relevansi latar belakang dengan riset posisi yang Anda incar.",
            "M2 Hard Skills":   "Ikuti kursus online (Coursera, Udemy) untuk meningkatkan skill teknis.",
            "M3 Industry Fit":  "Pelajari lebih dalam budaya dan tren industri target Anda.",
            "M4 Interest":      "Eksplorasi lebih banyak sub-bidang untuk menemukan passion yang tepat.",
            "M5 Moral Compass": "Bangun kebiasaan kerja yang konsisten dan tingkatkan integritas profesional.",
            "M6 Adaptability":  "Biasakan diri dengan tool baru dan tantang zona nyaman setiap bulan.",
            "M7 Branding":      "Optimalkan LinkedIn, buat CV ATS-friendly, dan bangun portofolio online.",
            "M8 Ambisi":        "Tetapkan target karir jangka pendek (3 bln) dan jangka panjang (1 thn).",
            "M9 Resiliensi":    "Latih mindset growth — setiap penolakan adalah data, bukan kegagalan.",
        }
        st.markdown("**💡 Area yang Perlu Ditingkatkan:**")
        for area, val_a in weak_areas:
            tip = tips_map.get(area, "Terus kembangkan kompetensi ini secara konsisten.")
            st.markdown(f"""
            <div style="background:rgba(255,159,10,0.07);border-left:3px solid #ff9f0a;
                        border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:8px;">
                <span style="font-weight:700;">{area}</span>
                <span style="opacity:0.5;font-size:0.85rem;"> ({val_a}/100)</span><br>
                <span style="font-size:0.88rem;opacity:0.8;">{tip}</span>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# HALAMAN: DASHBOARD HASIL
# ==========================================
elif page == "📊  Dashboard Hasil":
    st.markdown("""
    <h1 style='text-align:center;'>📊 Dashboard Hasil</h1>
    <p class='subtitle'>Visualisasi lengkap hasil analisis terakhir Anda</p>
    """, unsafe_allow_html=True)

    lr = st.session_state.get("last_result")
    if lr is None:
        st.info("Belum ada analisis. Silakan jalankan analisis di halaman **Beranda & Analisis** terlebih dahulu.")
    else:
        # ── Ringkasan profil ──────────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div style="background:rgba(10,132,255,0.08);border:1px solid rgba(10,132,255,0.2);
                        border-radius:16px;padding:18px 20px;text-align:center;">
                <div style="opacity:0.55;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">
                    Rekomendasi Utama</div>
                <div style="font-weight:800;font-size:1.15rem;margin-top:6px;">
                    {lr['hasil_df'].iloc[0]['Industri']}</div>
                <div style="color:#0a84ff;font-weight:700;">
                    {lr['hasil_df'].iloc[0]['Kecocokan']:.1f}%</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div style="background:rgba(48,209,88,0.08);border:1px solid rgba(48,209,88,0.2);
                        border-radius:16px;padding:18px 20px;text-align:center;">
                <div style="opacity:0.55;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">
                    Skor Kesiapan</div>
                <div style="font-weight:800;font-size:1.5rem;margin-top:6px;color:{lr['kesiapan_color']};">
                    {lr['kesiapan_skor']}/100</div>
                <div style="font-size:0.85rem;opacity:0.7;">{lr['kesiapan_label']}</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
            <div style="background:rgba(191,90,242,0.08);border:1px solid rgba(191,90,242,0.2);
                        border-radius:16px;padding:18px 20px;text-align:center;">
                <div style="opacity:0.55;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;">
                    Archetype</div>
                <div style="font-weight:800;font-size:1rem;margin-top:6px;color:{lr['archetype_color']};">
                    {lr['archetype']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Radar chart ───────────────────────────────────────────────
        dc1, dc2 = st.columns(2)
        with dc1:
            st.markdown("#### 🕸️ Radar Kompetensi")
            cats   = list(lr["scores"].keys())
            vals   = list(lr["scores"].values())
            fig_r2 = go.Figure()
            fig_r2.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=cats + [cats[0]], fill="toself",
                fillcolor="rgba(10,132,255,0.15)",
                line=dict(color="#0a84ff", width=2.5),
                hovertemplate="%{theta}: %{r:.0f}/100<extra></extra>",
            ))
            fig_r2.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100],
                                    gridcolor="rgba(128,128,128,0.2)"),
                    angularaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=50, r=50, t=30, b=30),
                height=360,
            )
            st.plotly_chart(fig_r2, use_container_width=True)

        with dc2:
            st.markdown("#### 📈 Kecocokan Industri")
            fig_b2 = px.bar(
                lr["hasil_df"],
                x="Kecocokan", y="Industri",
                orientation="h",
                color="Kecocokan",
                color_continuous_scale=["#ff9f0a", "#0a84ff", "#30d158"],
                text=lr["hasil_df"]["Kecocokan"].apply(lambda v: f"{v:.1f}%"),
            )
            fig_b2.update_traces(textposition="outside")
            fig_b2.update_layout(
                xaxis=dict(range=[0, 110], title="Kecocokan (%)",
                           gridcolor="rgba(128,128,128,0.15)"),
                yaxis_title="",
                coloraxis_showscale=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=60, t=10, b=40),
                height=360,
            )
            st.plotly_chart(fig_b2, use_container_width=True)

        # ── Gauge kesiapan ────────────────────────────────────────────
        st.markdown("#### 🎯 Gauge Kesiapan Kerja")
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=lr["kesiapan_skor"],
            delta={"reference": 55, "valueformat": ".0f"},
            title={"text": lr["kesiapan_label"], "font": {"size": 16}},
            gauge={
                "axis":  {"range": [0, 100], "tickwidth": 1},
                "bar":   {"color": lr["kesiapan_color"]},
                "steps": [
                    {"range": [0, 40],  "color": "rgba(255,59,48,0.15)"},
                    {"range": [40, 55], "color": "rgba(255,159,10,0.15)"},
                    {"range": [55, 75], "color": "rgba(10,132,255,0.15)"},
                    {"range": [75, 100],"color": "rgba(48,209,88,0.15)"},
                ],
                "threshold": {"line": {"color": lr["kesiapan_color"], "width": 3}, "value": lr["kesiapan_skor"]},
            },
            number={"suffix": "/100"},
        ))
        fig_g.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=280,
            margin=dict(l=40, r=40, t=40, b=20),
        )
        st.plotly_chart(fig_g, use_container_width=True)


# ==========================================
# HALAMAN: RIWAYAT SESI
# ==========================================
elif page == "📋  Riwayat Sesi":
    st.markdown("""
    <h1 style='text-align:center;'>📋 Riwayat Analisis</h1>
    <p class='subtitle'>Semua analisis yang dilakukan selama sesi ini</p>
    """, unsafe_allow_html=True)

    riwayat = st.session_state.get("riwayat", [])
    if not riwayat:
        st.info("Belum ada riwayat analisis. Jalankan analisis di halaman **Beranda & Analisis**.")
    else:
        # Tabel ringkasan
        st.markdown("<br>### 🎯 Daftar Analisis Anda", unsafe_allow_html=True)
        
        # Callback: Mengubah state sebelum UI dirender dari atas
        def lompat_ke_dashboard(data_riwayat):
            st.session_state["last_result"] = data_riwayat
            st.session_state["nav_page"] = "📊  Dashboard Hasil"

        # Looping riwayat secara terbalik agar yang paling baru muncul di atas
        for i, r in enumerate(reversed(riwayat)):
            idx_asli = len(riwayat) - 1 - i  # Melacak index asli di memori
            
            # Membuat kartu yang bisa dibuka-tutup
            with st.expander(f"Analisis #{idx_asli + 1} | 🕒 {r['waktu']} | 🏆 {r['hasil_df'].iloc[0]['Industri']}", expanded=(i==0)):
                col_r1, col_r2, col_r3 = st.columns([2, 2, 1.5])
                
                with col_r1:
                    st.markdown(f"**🎓 Program Studi:**<br>{r['jurusan']}", unsafe_allow_html=True)
                    st.markdown(f"**💼 Dream Job:**<br>{r['dream_job']}", unsafe_allow_html=True)
                
                with col_r2:
                    st.markdown(f"**🧬 Archetype:**<br><span style='color:{r['archetype_color']};font-weight:700;'>{r['archetype']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**⚡ Kesiapan Kerja:**<br>{r['kesiapan_skor']}/100 ({r['kesiapan_label']})", unsafe_allow_html=True)
                
                with col_r3:
                    st.markdown("<br>", unsafe_allow_html=True) # Spacing
                    
                    # TOMBOL NAVIGASI TERPROGRAM (Menggunakan Callback)
                    st.button(
                        "📊 Lihat Full Dashboard", 
                        key=f"btn_dash_{idx_asli}", 
                        use_container_width=True,
                        on_click=lompat_ke_dashboard,
                        args=(riwayat[idx_asli],)
                    )

        # Detail tiap entri
        if len(riwayat) > 1:
            st.markdown("<br>**Perbandingan Radar Kompetensi (Semua Sesi)**", unsafe_allow_html=True)
            fig_cmp = go.Figure()
            cmp_colors = ["#0a84ff", "#30d158", "#ff9f0a", "#bf5af2", "#ff3b30"]
            for i, r in enumerate(riwayat):
                cats = list(r["scores"].keys())
                vals = list(r["scores"].values())
                fig_cmp.add_trace(go.Scatterpolar(
                    r=vals + [vals[0]], theta=cats + [cats[0]],
                    fill="toself",
                    fillcolor=f"rgba{tuple(int(cmp_colors[i%5].lstrip('#')[j:j+2],16) for j in (0,2,4)) + (0.1,)}",
                    line=dict(color=cmp_colors[i % 5], width=2),
                    name=f"#{i+1} {r['waktu']}",
                ))
            fig_cmp.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100],
                                    gridcolor="rgba(128,128,128,0.2)"),
                    angularaxis=dict(gridcolor="rgba(128,128,128,0.15)"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=-0.15),
                margin=dict(l=60, r=60, t=40, b=60),
                height=480,
            )
            st.plotly_chart(fig_cmp, use_container_width=True)


# ==========================================
# HALAMAN: TENTANG SISTEM
# ==========================================
elif page == "ℹ️  Tentang Sistem":
    st.markdown("""
    <h1 style='text-align:center;'>ℹ️ Tentang Sistem Vinix 7</h1>
    <p class='subtitle'>Metodologi, Model AI, dan Tim Pengembang</p>
    """, unsafe_allow_html=True)

    t1, t2, t3 = st.tabs(["🧠 Metodologi", "📐 Arsitektur Model", "👥 Tim & Kontak"])

    with t1:
        st.markdown("""
        ### Bagaimana Sistem Ini Bekerja?

        Sistem Rekomendasi Karir Vinix 7 menggunakan **machine learning berbasis LightGBM**
        untuk memetakan profil mahasiswa ke dalam tiga klaster industri utama.

        **Alur Analisis:**

        1. **Input Profil** — Pengguna mengisi 27 variabel mencakup akademik, kompetensi,
           preferensi karir, dan pengembangan diri.
        2. **Preprocessing** — Data distandarisasi, di-mapping, dan di-encoding agar
           kompatibel dengan blueprint fitur model (48 fitur aktif).
        3. **Prediksi LightGBM** — Model menghitung probabilitas kecocokan terhadap
           tiga klaster industri secara bersamaan.
        4. **Interpretasi** — Hasil disajikan dalam bentuk persentase kecocokan,
           radar chart kompetensi, archetype, dan rekomendasi langkah konkret.

        **Tiga Klaster Industri:**

        | Klaster | Karakteristik |
        |---|---|
        | 💻 Bidang Tech dan Digital | Lingkungan agile, cepat, dan berbasis inovasi |
        | 🎨 Industri Kreatif dan Proyek | Fleksibel, kolaboratif, berbasis proyek |
        | 🏛️ Industri Konvensional Terstruktur | Stabil, formal, jenjang karir jelas |
        """)

    with t2:
        st.markdown("""
        ### Spesifikasi Teknis Model

        | Parameter | Nilai |
        |---|---|
        | **Algoritma** | LightGBM (Gradient Boosting Decision Tree) |
        | **Optimasi** | Bayesian Optimization via Optuna (50 trials) |
        | **Seleksi Fitur** | RFECV (Recursive Feature Elimination with CV) |
        | **Jumlah Fitur Aktif** | 49 fitur (dari 60+ fitur asli) |
        | **Strategi Kelas Imbalanced** | `class_weight='balanced'` |
        | **Evaluasi** | 5-Fold Stratified Cross-Validation |
        | **Target** | 3 kelas industri makro |

        **Hyperparameter Optimal (Optuna):**

        | Parameter | Nilai |
        |---|---|
        | learning_rate | 0.0310 |
        | num_leaves | 24 |
        | max_depth | 9 |
        | min_child_samples | 32 |
        | feature_fraction | 0.5184 |
        | subsample | 0.7944 |

        ---
        > Model dilatih menggunakan data hasil survei nyata mahasiswa peserta program Vinix 7.
        """)

    with t3:
        st.markdown("""
        <h3 style='margin-bottom:0.3rem;'>Tim Pengembang</h3>
        <p style='opacity:0.55;font-size:0.9rem;margin-top:0;'>
            Kelompok 02 — Program Internship Berbasis Proyek <strong>Vinix 7</strong>
        </p>
        """, unsafe_allow_html=True)

        TEAM = [
            {
                "nama":   "Muhammad Fikri Prasetyo",
                "inisial":"MFP",
                "warna":  "#0a84ff",
                "peran":  "ML Engineer & Data Scientist",
                "ikon":   "🤖",
                "tugas":  [
                    "Pelatihan & tuning model LightGBM dengan Optuna",
                    "Evaluasi model menggunakan 5-Fold Stratified CV",
                    "Seleksi fitur dengan RFECV",
                    "Ekspor model, label encoder, dan blueprint fitur (.pkl)",
                ],
            },
            {
                "nama":   "Abdul Muin",
                "inisial":"AM",
                "warna":  "#30d158",
                "peran":  "Data Engineer & Analyst",
                "ikon":   "🗄️",
                "tugas":  [
                    "Pengumpulan dan validasi data survei mahasiswa",
                    "Preprocessing, standarisasi, dan mapping fitur",
                    "Encoding kategorikal & penanganan data imbalanced",
                    "Analisis distribusi target dan insight dataset",
                ],
            },
            {
                "nama":   "Achmad Shandy Wijaya",
                "inisial":"ASW",
                "warna":  "#ff9f0a",
                "peran":  "App Developer & UI/UX",
                "ikon":   "🖥️",
                "tugas":  [
                    "Pengembangan aplikasi Streamlit end-to-end",
                    "Desain UI/UX (glassmorphism, dark/light adaptive)",
                    "Integrasi visualisasi Plotly (radar, bar, gauge)",
                    "Splash screen, sidebar navigasi, dan dashboard analitik",
                ],
            },
        ]

        for member in TEAM:
            st.markdown(f"""
            <div style="background:rgba(128,128,128,0.06);border:1px solid rgba(128,128,128,0.15);
                        border-radius:20px;padding:22px 26px;margin-bottom:16px;
                        display:flex;gap:20px;align-items:flex-start;
                        transition:all 0.3s ease;">
                <!-- Avatar -->
                <div style="min-width:54px;height:54px;border-radius:50%;
                            background:linear-gradient(135deg,{member['warna']}33,{member['warna']}99);
                            border:2px solid {member['warna']};
                            display:flex;align-items:center;justify-content:center;
                            font-size:1.15rem;font-weight:900;color:{member['warna']};
                            flex-shrink:0;">
                    {member['inisial']}
                </div>
                <!-- Info -->
                <div style="flex:1;">
                    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px;">
                        <span style="font-size:1.05rem;font-weight:800;">{member['nama']}</span>
                        <span style="background:{member['warna']}22;color:{member['warna']};
                                     border:1px solid {member['warna']}44;border-radius:99px;
                                     font-size:0.72rem;font-weight:700;padding:2px 10px;
                                     text-transform:uppercase;letter-spacing:0.4px;">
                            {member['ikon']} {member['peran']}
                        </span>
                    </div>
                    <ul style="margin:6px 0 0 0;padding-left:1.2rem;opacity:0.75;font-size:0.87rem;line-height:1.7;">
                        {''.join(f"<li>{t}</li>" for t in member['tugas'])}
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        **Stack Teknologi:**
        - 🐍 Python 3.10
        - 🌐 Streamlit (web app framework)
        - 🤖 LightGBM (model ML)
        - 📊 Plotly (visualisasi interaktif)
        - 🔢 Scikit-learn, Optuna (evaluasi & optimasi)
        - 📦 Pandas, NumPy (data processing)

        ---
        > *"AI Career Intelligence — Powered by Data, Driven by Purpose."*
        """)


# ==========================================
# FOOTER (tampil di semua halaman)
# ==========================================
st.markdown(
    "<br><p style='text-align:center;color:#8e8e93;font-size:0.85rem;'>"
    "Designed by KELOMPOK 02 VINIX7. Powered by Streamlit &amp; LightGBM.</p>",
    unsafe_allow_html=True,
)
