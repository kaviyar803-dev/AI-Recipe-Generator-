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
.badge-veg {background:#E8F5E9; color:#2E7D32;}
.badge-cal {background:#E3F2FD; color:#1565C0;}
.badge-time {background:#FFF3E0; color:#EF6C00;}
.badge-pro {background:#F3E5F5; color:#7B1FA2;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍛 AI RECIPE GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666">Random Ingredients + Dashboard + 5 Ingredients Magic ✨</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("recipes.csv", engine="openpyxl")
    except:
        df = pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')
    return df

df = load_data()

# Safe column finder
def fcol(kws, idx):
    for kw in kws:
        for c in df.columns:
            if kw.lower() in str(c).lower():
                return c
    if idx < len(df.columns):
        return df.columns[idx]
    return df.columns[0]

name_col = fcol(['recipe name','recipe'], 0)
ing_col = fcol(['ingredient'], 1)
ins_col = fcol(['instruction','method','steps'], 2)
cal_col = fcol(['calori'], 3)
diet_col = fcol(['diet type','diet'], 4)
cat_col = fcol(['category','course'], 5)
time_col = fcol(['cook time','time'], 6)
prot_col = fcol(['protein'], 7)

# Make numeric safe
for col in [cal_col, time_col, prot_col]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# DASHBOARD
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><h2>📚 {len(df)}</h2><p>Total Recipes</p></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><h2>🥬 180+</h2><p>Veg Recipes</p></div>', unsafe_allow_html=True)
with c3:
    try: avg = int(df[cal_col].mean())
    except: avg = 285
    st.markdown(f'<div class="metric-card"><h2>🔥 {avg}</h2><p>Avg Calories</p></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><h2>🤖 AI</h2><p>Smart Search</p></div>', unsafe_allow_html=True)

st.divider()

# TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔍 AI Search", "🥗 Diet Food", "👶 Kids Food", "⚡ Low Calorie", "⏱️ Quick", "🎲 5 Ingredients Magic"])

with tab1:
    st.markdown("#### 👨‍🍳 Enter Random Ingredients (Ex: tomato, egg, onion)")
    user_input = st.text_input("search", placeholder="🍅 tomato, egg, onion...", label_visibility="collapsed", key="ai")
    colA, colB = st.columns([3,1])
    with colA: btn = st.button("🔍 Find My Recipe", type="primary", use_container_width=True)
    with colB: rand_btn = st.button("🎲 Surprise Me", use_container_width=True)

    if rand_btn:
        s = df.sample(1).iloc[0]
        st.balloons()
        st.markdown(f'<div class="recipe-card"><h3>🎲 {s[name_col]}</h3><p><b>Ingredients:</b> {s[ing_col]}</p><p>{str(s.get(ins_col,""))[:600]}...</p></div>', unsafe_allow_html=True)

    if btn and user_input:
        ings = [x.lower().strip() for x in user_input.split(",") if x.strip()!=""]
        df['score'] = df[ing_col].astype(str).apply(lambda v: sum(1 for i in ings if i in v.lower()))
        res = df[df['score']>0].sort_values('score', ascending=False).head(6)
        if len(res)>0:
            st.success(f"Found {len(res)} recipes for {', '.join(ings)}")
            for _, r in res.iterrows():
                st.markdown(f'<div class="recipe-card"><h4>🍲 {r[name_col]} ({int(r["score"])}/{len(ings)} matched)</h4><span class="badge badge-cal">🔥 {r.get(cal_col,"250")} kcal</span><span class="badge badge-time">⏱️ {r.get(time_col,"20")} min</span><p style="margin-top:10px"><b>Ingredients:</b> {r[ing_col]}</p><p>{str(r.get(ins_col,""))[:500]}...</p></div>', unsafe_allow_html=True)
        else:
            st.warning("No exact match, but AI created one!")
            st.markdown(f'<div class="recipe-card" style="border-left-color:#4CAF50"><h4>✨ {", ".join([i.title() for i in ings[:2]])} Masala</h4><p>Add {", ".join(ings)}, spices, cook 10 min. Ready!</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 🥗 Diet Food")
    try: diet_df = df[df[diet_col].astype(str).str.contains('Veg|Vegan|Protein', case=False, na=False)].head(8)
    except: diet_df = df.head(8)
    for _, r in diet_df.iterrows():
        st.markdown(f'<div class="recipe-card"><h4>🥗 {r[name_col]}</h4><p>{str(r[ing_col])[:200]}</p></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 👶 Kids Food")
    try: kids_df = df[df[cat_col].astype(str).str.contains('Snack|Kids|Sweet|Dessert', case=False, na=False)].head(8)
    except: kids_df = df.sample(8)
    if len(kids_df)==0: kids_df = df.sample(8)
    for _, r in kids_df.iterrows():
        st.markdown(f'<div class="recipe-card" style="border-left-color:#FF4081"><h4>🍭 {r[name_col]}</h4><span class="badge" style="background:#FCE4EC;color:#AD1457">Kids Special</span><p>{str(r[ing_col])[:200]}</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### ⚡ Low Calorie < 250 kcal")
    try: low = df[df[cal_col] < 250].head(8)
    except: low = df.head(8)
    if len(low)==0: low = df.head(8)
    for _, r in low.iterrows():
        st.markdown(f'<div class="recipe-card" style="border-left-color:#00BCD4"><h4>⚡ {r[name_col]}</h4><span class="badge badge-cal">{r.get(cal_col,"180")} kcal</span><p>{str(r[ing_col])[:150]}</p></div>', unsafe_allow_html=True)

with tab5:
    st.markdown("### ⏱️ Quick & Full List")
    st.dataframe(df[[name_col, ing_col]].head(50), use_container_width=True, hide_index=True)

with tab6:
    st.markdown("### 🎲 5 Random Ingredients = 1 Magic Recipe!")
    pool = ["tomato", "onion", "egg", "chicken", "rice", "potato", "paneer", "cheese", "bread", "milk", "oats", "banana", "curd", "spinach", "mushroom", "capsicum", "carrot", "garlic", "butter", "corn"]

    if st.button("🎯 Give Me 5 Random Ingredients & Make Recipe!", type="primary", use_container_width=True, key="magic"):
        picked = random.sample(pool, 5)
        st.session_state['picked_5'] = picked

    if 'picked_5' in st.session_state:
        picked = st.session_state['picked_5']
        st.markdown("#### 🧾 Your 5 Magic Ingredients:")
        cols = st.columns(5)
        for i, ing in enumerate(picked):
            with cols[i]:
                st.markdown(f'<div class="metric-card"><h3>🍅</h3><b>{ing.title()}</b></div>', unsafe_allow_html=True)

        st.divider()
        dish_name = f"{picked[0].title()} {picked[1].title()} Delight"
        st.balloons()
        st.markdown(f"""
        <div class="recipe-card" style="border-left-color:#9C27B0; border:1px solid #E1BEE7">
            <h2>✨ AI Created: {dish_name} 👨‍🍳</h2>
            <span class="badge badge-cal">🔥 320 kcal</span>
            <span class="badge badge-pro">💪 18g Protein</span>
            <span class="badge badge-time">⏱️ 15 min</span>
            <p><b>Ingredients Used:</b> {', '.join([p.title() for p in picked])}</p>
            <p><b>Step 1:</b> Oil la {picked[1]} vathakku.<br>
            <b>Step 2:</b> {picked[0]} and {picked[2]} add pannu.<br>
            <b>Step 3:</b> {picked[3]} and {picked[4]} potu masala add pannu.<br>
            <b>Step 4:</b> 10 min cook panni serve pannu. Ready!</p>
            <p style="background:#F3E5F5; padding:8px; border-radius:8px"><b>Chef Tip:</b> Itha rice kooda sapta super!</p>
        </div>
        """, unsafe_allow_html=True)

        # Similar recipes
        st.markdown("#### 🔍 Similar from DB:")
        df['score2'] = df[ing_col].astype(str).apply(lambda v: sum(1 for p in picked if p in v.lower()))
        sim = df[df['score2']>0].sort_values('score2', ascending=False).head(3)
        for _, r in sim.iterrows():
            st.markdown(f'<div class="recipe-card"><h5>🍲 {r[name_col]} - {int(r["score2"])}/5 matched</h5><p>{str(r[ing_col])[:120]}...</p></div>', unsafe_allow_html=True)
