import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
* {font-family:'Poppins', sans-serif;}
.stApp {background: linear-gradient(135deg, #FFF8E1 0%, #FFE0B2 100%);}
.main-title {
    text-align:center; font-size:2.8rem; font-weight:800;
    background: linear-gradient(90deg, #FF4B4B, #FF8C00);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.metric-card {
    background:white; border-radius:16px; padding:18px; text-align:center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07); border-top:4px solid #FF8C00;
}
.recipe-card {
    background:white; border-radius:18px; padding:18px; margin-bottom:12px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06); border-left:5px solid #FF8C00;
}
.badge {display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; margin-right:5px;}
.badge-veg {background:#E8F5E9; color:#2E7D32;}.badge-cal {background:#E3F2FD; color:#1565C0;}
.badge-time {background:#FFF3E0; color:#EF6C00;}.badge-pro {background:#F3E5F5; color:#7B1FA2;}
div[data-testid="stTextInput"] input {border-radius:30px; border:2px solid #FF8C00; padding:14px 20px;}
div.stButton > button {border-radius:30px; font-weight:600;}
div.stButton > button[kind="primary"]{background:linear-gradient(90deg,#FF4B4B,#FF8C00); color:white; border:none;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍛 AI RECIPE GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666">Random Ingredients Search + Smart Dashboard - All in One ✨</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    try: df = pd.read_excel("recipes.csv", engine="openpyxl")
    except: df = pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')
    for c in df.columns:
        if 'calori' in c.lower() or 'protein' in c.lower() or 'time' in c.lower():
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

df = load_data()
def fcol(kws, idx):
    for kw in kws:
        for c in df.columns:
            if kw.lower() in str(c).lower(): return c
    return df.columns[idx]
name_col = fcol(['recipe name','recipe'], 1)
ing_col = fcol(['ingredient'], 3)
ins_col = fcol(['instruction','method'], 5)
cal_col = fcol(['calori'], 7)
diet_col = fcol(['diet type','diet'], 4)
cat_col = fcol(['category'], 2)
time_col = fcol(['cook time','time'], 6)
prot_col = fcol(['protein'], 8)

# DASHBOARD
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><h2>📚 {len(df)}</h2><p>Total Recipes</p></div>', unsafe_allow_html=True)
with c2:
    veg = len(df[df[diet_col].astype(str).str.contains('Veg', case=False, na=False)]) if diet_col else 180
    st.markdown(f'<div class="metric-card"><h2>🥬 {veg}</h2><p>Veg Recipes</p></div>', unsafe_allow_html=True)
with c3:
    avg = int(df[cal_col].mean()) if cal_col in df.columns and df[cal_col].notna().any() else 285
    st.markdown(f'<div class="metric-card"><h2>🔥 {avg}</h2><p>Avg Calories</p></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><h2>🤖 AI</h2><p>Smart Search</p></div>', unsafe_allow_html=True)

st.divider()

# TABS - OLD + NEW COMBINED
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Random AI Search", "🥗 Diet Food", "👶 Kids Food", "⚡ Low Calorie & Protein", "⏱️ Quick & Dashboard"])

with tab1:
    st.markdown("#### 👨‍🍳 Enter Random Ingredients (Old Feature)")
    st.caption("Ex: tomato, egg, onion, rice, chicken - comma potu type pannu da, AI kandupidikkum!")
    user_input = st.text_input("", placeholder="🍅 Ex: tomato, egg, onion, chicken...", key="ai", label_visibility="collapsed")

    colA, colB, colC = st.columns([2,2,1])
    with colA: btn = st.button("🔍 Find My Recipe", type="primary", use_container_width=True)
    with colB: rand_btn = st.button("🎲 Surprise Me! Random Recipe", use_container_width=True)
    with colC:
        if st.button("🎯 Random Ingredients", use_container_width=True):
            samples = ["tomato, onion, egg", "rice, chicken, curd", "potato, cheese, bread", "oats, milk, banana"]
            st.session_state['rand_ing'] = random.choice(samples)
            st.info(f"Try this: {st.session_state['rand_ing']}")

    if 'rand_ing' in st.session_state and not user_input:
        user_input = st.session_state['rand_ing']

    if rand_btn:
        s=df.sample(1).iloc[0]
        st.balloons()
        st.markdown(f'<div class="recipe-card"><h3>🎲 Chef Surprise: {s[name_col]}</h3><p><b>Ingredients:</b> {s[ing_col]}</p><p>{str(s.get(ins_col,""))[:600]}...</p></div>', unsafe_allow_html=True)

    if btn and user_input:
        ings=[x.lower().strip() for x in user_input.split(",") if x.strip()!=""]
        df['score']=df[ing_col].apply(lambda v: sum(1 for i in ings if i in str(v).lower()))
        res=df[df['score']>0].sort_values('score', ascending=False).head(6)
        if len(res)>0:
            st.success(f"🤖 AI Found {len(res)} recipes matching {', '.join(ings)}")
            for _,r in res.iterrows():
                cal = str(r.get(cal_col, '250')).split('.')[0] if cal_col in df.columns else '250'
                tim = str(r.get(time_col, '20')).split('.')[0] if time_col in df.columns else '20'
                pro = str(r.get(prot_col, '10')).split('.')[0] if prot_col in df.columns else '10'
                st.markdown(f'''
                <div class="recipe-card">
                    <h4>🍲 {r[name_col]} <span style="color:#FF8C00">({int(r['score'])}/{len(ings)} matched)</span></h4>
                    <span class="badge badge-cal">🔥 {cal} kcal</span>
                    <span class="badge badge-pro">💪 {pro}g Protein</span>
                    <span class="badge badge-time">⏱️ {tim} min</span>
                    <p style="margin-top:10px"><b>🧾 Ingredients:</b> {r[ing_col]}</p>
                    <p><b>👩‍🍳 Method:</b> {str(r.get(ins_col,""))[:650]}...</p>
                </div>''', unsafe_allow_html=True)
        else:
            st.warning("Exact match illa da, but AI generated one!")
            st.markdown(f'''
            <div class="recipe-card" style="border-left-color:#4CAF50">
                <h3>✨ AI Generated: {" ".join([i.title() for i in ings[:2]])} Masala Magic</h3>
                <p><b>Your Random Ingredients:</b> {user_input}</p>
                <p><b>Recipe:</b> 1. Kadai la oil vittu onion vathakku. 2. {", ".join(ings)} add pannu. 3. Salt, chilli, garam masala potu 10 min cook pannu. 4. Coriander thooti serve pannu. Ready da!</p>
            </div>''', unsafe_allow_html=True)
            st.balloons()

with tab2:
    st.markdown("### 🥗 Diet Food Dashboard")
    diet_df = df[df[diet_col].astype(str).str.contains('Vegan|Vegetarian|High Protein|Low Fat|Healthy', case=False, na=False)] if diet_col in df.columns else df.head(10)
    for _,r in diet_df.head(8).iterrows():
        st.markdown(f'<div class="recipe-card"><h4>🥗 {r[name_col]}</h4><span class="badge badge-veg">{r.get(diet_col,"Diet")}</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 👶 Kids Food - Yummy Zone")
    kids_df = df[df[cat_col].astype(str).str.contains('Snack|Kids|Sweet|Dessert|Breakfast', case=False, na=False)] if cat_col in df.columns else df.sample(8)
    if len(kids_df)<3: kids_df = df.sample(8)
    for _,r in kids_df.head(8).iterrows():
        st.markdown(f'<div class="recipe-card" style="border-left-color:#FF4081"><h4>🍭 {r[name_col]}</h4><span class="badge" style="background:#FCE4EC;color:#AD1457">👶 Kids Special</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### ⚡ Low Calorie (<250 kcal) & High Protein")
    cL,cR = st.columns(2)
    with cL:
        st.markdown("**🔥 Low Calorie**")
        low = df[df[cal_col] < 250] if cal_col in df.columns and df[cal_col].notna().any() else df.head(5)
        for _,r in low.head(5).iterrows():
            st.markdown(f'<div class="recipe-card"><h5>⚡ {r[name_col]}</h5><span class="badge badge-cal">{r.get(cal_col,180)} kcal</span><p style="font-size:0.9rem">{str(r[ing_col])[:100]}...</p></div>', unsafe_allow_html=True)
    with cR:
        st.markdown("**💪 High Protein**")
        if prot_col in df.columns:
            high = df[pd.to_numeric(df[prot_col], errors='coerce')>12].sort_values(prot_col, ascending=False).head(5)
        else: high = df.sample(5)
        for _,r in high.iterrows():
            st.markdown(f'<div class="recipe-card" style="border-left-color:#4CAF50"><h5>💪 {r[name_col]}</h5><span class="badge badge-pro">High Protein</span><p style="font-size:0.9rem">{str(r[ing_col])[:100]}...</p></div>', unsafe_allow_html=True)

with tab5:
    st.markdown("### ⏱️ Quick Recipes & Full List")
    st.dataframe(df[[name_col, ing_col, cal_col if cal_col in df.columns else name_col]].head(50), use_container_width=True, hide_index=True)
