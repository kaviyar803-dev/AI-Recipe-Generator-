import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")

# --- SUPER STYLISH CSS DA ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
* {font-family: 'Poppins', sans-serif;}
.stApp {background: linear-gradient(135deg, #FFF5E5 0%, #FFE0B2 100%);}
.main-title {
    text-align:center; font-size: 3rem; font-weight: 800;
    background: linear-gradient(90deg, #FF4B4B, #FF8C00);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sub-title {text-align:center; color:#666; font-size:1.1rem; margin-bottom:25px;}
div[data-testid="stTextInput"] > div > div > input {
    border-radius: 30px; border: 2px solid #FF8C00; padding:15px 20px; font-size:1.1rem;
    background-color: white; color: black!important;
}
div.stButton > button {
    border-radius: 30px; font-weight: 600; padding: 12px; border:none; transition: 0.3s;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #FF4B4B, #FF8C00); color:white;
    box-shadow: 0 4px 15px rgba(255,75,75,0.3);
}
div.stButton > button[kind="primary"]:hover {transform: scale(1.03);}
.recipe-card {
    background: white; border-radius: 20px; padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08); border-left: 6px solid #FF8C00;
    margin-bottom: 15px;
}
.badge {
    display:inline-block; padding: 4px 12px; border-radius: 20px;
    font-size: 0.8rem; font-weight:600; margin-right:6px;
}
.badge-cal {background:#FFEBEE; color:#FF4B4B;}
.badge-pro {background:#E8F5E9; color:#2E7D32;}
.badge-time {background:#FFF3E0; color:#EF6C00;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍛 AI RECIPE GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Got ingredients? We got the perfect recipe magic for you ✨</div>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    try: return pd.read_excel("recipes.csv", engine="openpyxl")
    except: return pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')

df = load_data()

def find_col(kws, idx):
    for kw in kws:
        for c in df.columns:
            if kw.lower() in str(c).lower(): return c
    return df.columns[idx]

name_col = find_col(['recipe name','recipe','dish'], 1)
ing_col = find_col(['ingredient'], 2)
ins_col = find_col(['instruction','method','steps'], 5)

# Search box stylish ah
st.markdown("### 👨‍🍳 <span style='color:#FF4B4B'>What do you have in your kitchen?</span>", unsafe_allow_html=True)
user_input = st.text_input("", placeholder="🍅 Ex: tomato, egg, onion, chicken, rice... type & press Enter", label_visibility="collapsed")

col1, col2 = st.columns([3,1])
with col1:
    btn = st.button("🔍 Find My Recipe", type="primary", use_container_width=True)
with col2:
    random_btn = st.button("🎲 Surprise Me!", use_container_width=True)

if random_btn:
    s = df.sample(1).iloc[0]
    st.balloons()
    st.markdown(f"""
    <div class="recipe-card">
        <h3>🎲 Chef's Surprise: {s[name_col]}</h3>
        <p><b>🧾 Ingredients:</b> {s[ing_col]}</p>
        <p>{str(s.get(ins_col,''))[:500]}...</p>
    </div>
    """, unsafe_allow_html=True)

if btn and user_input:
    ings = [x.strip().lower() for x in user_input.split(",") if x.strip()!=""]
    df['score'] = df[ing_col].apply(lambda v: sum(1 for i in ings if i in str(v).lower()))
    result = df[df['score']>0].sort_values('score', ascending=False).head(6)

    if len(result)>0:
        st.success(f"🔥 Found {len(result)} delicious recipes for you!")
        for _, row in result.iterrows():
            cal = str(row.get('Calories (kcal)', '250')).split('.')[0]
            pro = str(row.get('Protein (g)', '12')).split('.')[0]
            time = str(row.get('Cook Time (min)', '20')).split('.')[0]
            st.markdown(f"""
            <div class="recipe-card">
                <h3>🍲 {row[name_col]}</h3>
                <span class="badge badge-cal">🔥 {cal} kcal</span>
                <span class="badge badge-pro">💪 {pro}g Protein</span>
                <span class="badge badge-time">⏱️ {time} min</span>
                <hr style="margin:12px 0; border:0; border-top:1px solid #eee">
                <p><b>🧾 You Need:</b> {row[ing_col]}</p>
                <p><b>👩‍🍳 How to Cook:</b><br>{str(row.get(ins_col,''))[:700]}...</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="recipe-card" style="border-left-color:#4CAF50">
            <h3>✨ AI Magic Created: {' '.join([i.title() for i in ings[:2]])} Special</h3>
            <p><b>Your Items:</b> {user_input}</p>
            <p><b>Recipe:</b> Heat oil, sauté onion & tomato, add <b>{', '.join(ings)}</b>, add salt, chilli, garam masala. Cook 10 mins, garnish with coriander. Tasty {', '.join(ings)} dish ready!</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()

if not btn and not random_btn:
    st.divider()
    st.markdown(f"### 📚 <span style='color:#333'>Total {len(df)} Recipes Loaded</span>", unsafe_allow_html=True)
    st.dataframe(df[[name_col, ing_col]].head(20), use_container_width=True, hide_index=True)
