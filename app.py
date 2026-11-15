import streamlit as st
import joblib
import re
import random
from pathlib import Path

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="بُحور | اكتشف البحر الشعري",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / "model"
ASSETS_DIR = BASE_DIR / "assets"


# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_models():
    model = joblib.load(MODEL_DIR / "best_svm_model.pkl")
    vectorizer = joblib.load(MODEL_DIR / "tfidf_vectorizer.pkl")
    labels = joblib.load(MODEL_DIR / "meter_labels.pkl")
    return model, vectorizer, labels


model, vectorizer, meter_labels = load_models()


# ==========================================
# ARABIC TEXT CLEANING
# ==========================================

def normalize_arabic(text):
    text = str(text)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    text = text.replace("ـ", "")
    text = re.sub(r'[أإآ]', 'ا', text)
    text = re.sub(r'[^\u0600-\u06FF\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ==========================================
# POETS
# ==========================================

poets = [
    {
        "name": "المتنبي",
        "description": "شاعر العربية وأحد أعظم أعلامها",
        "image": "al_mutanabbi.jpg"
    },
    {
        "name": "أبو العتاهية",
        "description": "شاعر الزهد والحكمة",
        "image": "abu_al_atahiya.jpg"
    },
    {
        "name": "عنترة بن شداد",
        "description": "فارس الشعر العربي",
        "image": "antarah.jpg"
    },
    {
        "name": "امرؤ القيس",
        "description": "من أعلام الشعر الجاهلي",
        "image": "imru_al_qais.jpg"
    },
    {
        "name": "أبو تمام",
        "description": "شاعر المعاني والبديع",
        "image": "abu_tammam.jpg"
    },
    {
        "name": "البحتري",
        "description": "صاحب السينية الشهيرة",
        "image": "al_buhturi.jpg"
    },
    {
        "name": "أبو نواس",
        "description": "أحد أعلام الشعر العباسي",
        "image": "abu_nuwas.jpg"
    },
    {
        "name": "أحمد شوقي",
        "description": "أمير الشعراء",
        "image": "ahmed_shawqi.jpg"
    }
]

# اختيار ثلاثة شعراء عشوائيًا لكل جلسة
if "selected_poets" not in st.session_state:
    st.session_state.selected_poets = random.sample(poets, 3)


# ==========================================
# CSS DESIGN
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@400;500;600;700;800&display=swap');

:root {
    --background: #160904;
    --surface: #24140E;
    --surface-light: #321D14;
    --copper: #A94F32;
    --orange: #D58A35;
    --ivory: #F5EBDD;
    --muted: #BDA58F;
    --border: #503021;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 50% 0%,
            #3A1C10 0%,
            #160904 52%,
            #0D0502 100%
        );
    color: var(--ivory);
    font-family: 'Cairo', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* HERO */

.hero-title {
    text-align: center;
    color: #E4B66D;
    font-family: 'Amiri', serif;
    font-size: 88px;
    font-weight: bold;
    line-height: 1.4;
    text-shadow: 0 5px 35px rgba(213,138,53,0.2);
}

.hero-subtitle {
    text-align: center;
    color: #D0B49A;
    font-family: 'Amiri', serif;
    font-size: 23px;
    margin-top: -10px;
}

.gold-divider {
    width: 110px;
    height: 2px;
    background: linear-gradient(
        90deg,
        transparent,
        #D58A35,
        transparent
    );
    margin: 30px auto;
}

/* TITLES */

.section-title {
    color: #E4B66D;
    font-family: 'Amiri', serif;
    font-size: 32px;
    font-weight: bold;
    text-align: right;
    margin-bottom: 10px;
}

.section-description {
    color: #BDA58F;
    font-size: 15px;
    text-align: right;
    line-height: 2;
}

/* POET CARDS */

.poet-card {
    background: linear-gradient(
        145deg,
        #382116,
        #1D0E08
    );
    border: 1px solid rgba(213,138,53,0.35);
    border-radius: 17px;
    padding: 14px;
    text-align: center;
    height: 100%;
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    transition: 0.3s ease;
}

.poet-card:hover {
    border-color: #D58A35;
    transform: translateY(-5px);
}

.poet-name {
    color: #E4B66D;
    font-family: 'Amiri', serif;
    font-size: 27px;
    font-weight: bold;
    margin-top: 12px;
}

.poet-description {
    color: #BDA58F;
    font-size: 13px;
    padding-bottom: 8px;
}

/* IMAGE */

div[data-testid="stImage"] img {
    border-radius: 11px;
    border: 1px solid rgba(213,138,53,0.3);
    object-fit: cover;
}

/* TEXT AREA */

div[data-testid="stTextArea"] textarea {
    background: #21130D;
    color: #F5EBDD;
    border: 1px solid #70432A;
    border-radius: 14px;
    font-family: 'Amiri', serif;
    font-size: 22px;
    line-height: 2;
    direction: rtl;
    padding: 20px;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #D58A35;
    box-shadow: 0 0 15px rgba(213,138,53,0.12);
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #947B68;
}

/* BUTTON */

.stButton > button {
    background: linear-gradient(
        120deg,
        #A94F32,
        #D58A35
    );
    color: white;
    border: 1px solid #D58A35;
    border-radius: 10px;
    height: 54px;
    font-family: 'Cairo', sans-serif;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    background: linear-gradient(
        120deg,
        #C66A43,
        #E5A64D
    );
    color: white;
    border-color: #F0C77C;
    transform: translateY(-2px);
}

/* RESULT */

.result-card {
    background: linear-gradient(
        145deg,
        #382116,
        #1D0E08
    );
    border: 1px solid #D58A35;
    border-radius: 17px;
    padding: 30px;
    text-align: center;
    margin-top: 25px;
}

.result-label {
    color: #BDA58F;
    font-size: 17px;
}

.result-meter {
    color: #E4B66D;
    font-family: 'Amiri', serif;
    font-size: 48px;
    font-weight: bold;
}

/* METER LIST */

.meter-item {
    background: #29170F;
    border: 1px solid rgba(213,138,53,0.25);
    border-radius: 11px;
    padding: 14px 18px;
    margin: 9px 0;
    display: flex;
    justify-content: space-between;
}

.meter-name {
    color: #F5EBDD;
    font-size: 16px;
    font-weight: bold;
}

.meter-score {
    color: #E4B66D;
    font-size: 13px;
}

/* METERS */

.info-card {
    background: linear-gradient(
        145deg,
        #382116,
        #211109
    );
    border: 1px solid rgba(213,138,53,0.25);
    border-radius: 13px;
    padding: 18px 8px;
    text-align: center;
    margin-bottom: 12px;
}

.info-title {
    color: #E4B66D;
    font-family: 'Amiri', serif;
    font-size: 23px;
}

/* DIWAN */

.diwan-link {
    display: inline-block;
    background: linear-gradient(
        120deg,
        #A94F32,
        #D58A35
    );
    color: white !important;
    padding: 14px 38px;
    border-radius: 10px;
    font-weight: bold;
    font-size: 17px;
    transition: 0.3s;
}

.diwan-link:hover {
    background: #E5A64D;
    transform: translateY(-3px);
}

/* FOOTER */

.footer {
    text-align: center;
    color: #947B68;
    font-size: 13px;
    margin-top: 65px;
    border-top: 1px solid #503021;
    padding-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HERO SECTION - BUHOOR BRAND
# ==========================================

logo_path = ASSETS_DIR / "buhoor_logo.png"

if logo_path.exists():
    _, logo_col, _ = st.columns([1, 1.5, 1])

    with logo_col:
        st.image(str(logo_path), use_container_width=True)

else:
    st.markdown(
        """
        <div class="hero-title">بُحور</div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero-subtitle">
        كل قصيدةٍ بحر، ولكل بحرٍ حكاية
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gold-divider"></div>',
    unsafe_allow_html=True
)

# ==========================================
# THREE POET PORTRAITS
# ==========================================

st.markdown(
    '<div class="section-title" style="text-align:center;">'
    'من ذاكرة الشعر العربي</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#BDA58F;
        margin-bottom:25px;
    ">
    وجوه صنعت تاريخ القصيدة العربية.
    </p>
    """,
    unsafe_allow_html=True
)

poet_columns = st.columns(3)

for column, poet in zip(
    poet_columns,
    st.session_state.selected_poets
):

    with column:

        image_path = ASSETS_DIR / poet["image"]

        st.markdown(
            '<div class="poet-card">',
            unsafe_allow_html=True
        )

        if image_path.exists():
            st.image(
                str(image_path),
                use_container_width=True
            )
        else:
            st.markdown(
                """
                <div style="
                    height:230px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:75px;
                    background:#211109;
                    border-radius:10px;
                ">
                📜
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div class="poet-name">{poet["name"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="poet-description">'
            f'{poet["description"]}</div>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# POEM ANALYSIS
# ==========================================

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title">'
    'اكتشف البحر الشعري لقصيدتك'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'أدخل القصيدة كاملة للحصول على نتيجة أكثر دقة.'
    '</div>',
    unsafe_allow_html=True
)

poem = st.text_area(
    "القصيدة",
    height=280,
    placeholder="اكتب أبيات قصيدتك العربية هنا...",
    label_visibility="collapsed"
)

analyze = st.button(
    "✦ اكتشف البحر الشعري",
    use_container_width=True
)


# ==========================================
# CLASSIFICATION
# ==========================================

if analyze:

    if not poem.strip():

        st.warning("يرجى إدخال قصيدة أولاً.")

    else:

        cleaned = normalize_arabic(poem)

        if not cleaned:

            st.warning("لم يتم العثور على نص عربي صالح للتحليل.")

        else:

            vector = vectorizer.transform([cleaned])

            prediction = model.predict(vector)[0]

            scores = model.decision_function(vector)[0]

            classes = model.classes_

            top_indices = scores.argsort()[::-1][:5]

            st.markdown(
                f"""
                <div class="result-card">
                    <div class="result-label">
                        البحر الشعري المتوقع
                    </div>
                    <div class="result-meter">
                        {prediction}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="section-title" style="margin-top:30px;">'
                'أقرب خمسة بحور'
                '</div>',
                unsafe_allow_html=True
            )

            for rank, index in enumerate(top_indices, start=1):

                meter = classes[index]
                score = scores[index]

                st.markdown(
                    f"""
                    <div class="meter-item">
                        <span class="meter-name">
                            {rank}. {meter}
                        </span>
                        <span class="meter-score">
                            درجة القرار: {score:.4f}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ==========================================
# TEN ARABIC METERS
# ==========================================

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title" style="text-align:center;">'
    'البحور الشعرية العشرة'
    '</div>',
    unsafe_allow_html=True
)

meters = [
    "الطويل",
    "الكامل",
    "البسيط",
    "الوافر",
    "الخفيف",
    "السريع",
    "المتقارب",
    "الرجز",
    "الرمل",
    "المنسرح"
]

columns = st.columns(5)

for i, meter in enumerate(meters):

    with columns[i % 5]:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">{meter}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# DIWAN
# ==========================================

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title" style="text-align:center;">'
    'رحلة في دواوين العرب'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#BDA58F;
        line-height:2;
    ">
    تصفح دواوين الشعراء واكتشف روائع الأدب العربي.
    </p>

    <div style="text-align:center; margin:25px;">
        <a class="diwan-link"
        href="https://www.aldiwan.net/"
        target="_blank">
        تصفح موقع الديوان ✦
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# ABOUT
# ==========================================

st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

st.markdown(
    '<div class="section-title" style="text-align:center;">'
    'عن بُحور'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#BDA58F;
        line-height:2.2;
        max-width:750px;
        margin:auto;
    ">
    بُحور مشروع يوظف تعلم الآلة في تصنيف الشعر العربي
    ضمن عشرة بحور شعرية، باستخدام تقنيات معالجة النصوص
    واستخراج الخصائص النصية وخوارزميات التصنيف.
    </p>

    <p style="
        text-align:center;
        color:#D58A35;
        margin-top:20px;
    ">
    Python · TF-IDF · Linear SVM · Scikit-learn
    </p>
    """,
    unsafe_allow_html=True
)


# ==========================================
# FOOTER
# ==========================================

st.markdown(
    """
    <div class="footer">
        بُحور | مشروع في تعلم الآلة واللغة العربية
        <br><br>
        حيث تسكن القصيدة في وزنها
    </div>
    """,
    unsafe_allow_html=True
)