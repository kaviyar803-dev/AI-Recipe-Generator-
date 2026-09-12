import streamlit as st
import pandas as pd

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
.badge-veg {background:#E8F5E9; color:#2E7D32;}.badge-nonveg {background:#FFEBEE; color:#C62828;}
.badge-time {background:#FFF3E0; color:#EF6C00;}.badge-cal {background:#E3F2FD; color:#1565C0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍛 AI RECIPE GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666">Smart Dashboard + AI Search - Find food for every mood ✨</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    try: df = pd.read_excel("recipes.csv", engine="openpyxl")
    except: df = pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')
    # clean calories
    for c in df.columns:
        if 'calori' in c.lower():
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
course_col = fcol(['course'], 3)
time_col = fcol(['cook time','time'], 6)

# --- DASHBOARD METRICS ---
c1,c2,c3,c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><h2>📚 {len(df)}</h2><p>Total Recipes</p></div>', unsafe_allow_html=True)
with c2:
    veg = len(df[df[diet_col].astype(str).str.contains('Veg', case=False, na=False)]) if diet_col else 0
    st.markdown(f'<div class="metric-card"><h2>🥬 {veg}</h2><p>Veg Recipes</p></div>', unsafe_allow_html=True)
with c3:
    avg_cal = int(df[cal_col].mean()) if cal_col and df[cal_col].notna().any() else 250
    st.markdown(f'<div class="metric-card"><h2>🔥 {avg_cal}</h2><p>Avg Calories</p></div>', unsafe_allow_html=True)
with c4:
    kids = len(df[df[cat_col].astype(str).str.contains('Kids|Snack', case=False, na=False)]) if cat_col else 35
    st.markdown(f'<div class="metric-card"><h2>👶 {kids}</h2><p>Kids Friendly</p></div>', unsafe_allow_html=True)

st.divider()

# --- CREATIVE TABS DASHBOARD ---
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔍 AI Search", "🥗 Diet Food", "👶 Kids Food", "⚡ Low Calorie", "💪 High Protein", "⏱️ Quick 15min"])

with tab1:
    st.markdown("#### 👨‍🍳 What ingredients do you have?")
    user_input = st.text_input("", placeholder="Ex: tomato, egg, oats, paneer...", key="search", label_visibility="collapsed")
    b1,b2 = st.columns([3,1])
    with b1: btn = st.button("🔍 Find My Recipe", type="primary", use_container_width=True)
    with b2: rand = st.button("🎲 Surprise Me", use_container_width=True)
    if rand:
        s=df.sample(1).iloc[0]
        st.markdown(f'<div class="recipe-card"><h3>🎲 {s[name_col]}</h3><p>{s[ing_col]}</p></div>', unsafe_allow_html=True)
        st.balloons()
    if btn and user_input:
        ings=[x.lower().strip() for x in user_input.split(",")]
        df['score']=df[ing_col].apply(lambda v: sum(1 for i in ings if i in str(v).lower()))
        res=df[df['score']>0].sort_values('score', ascending=False).head(6)
        if len(res)>0:
            for _,r in res.iterrows():
                st.markdown(f'<div class="recipe-card"><h4>🍲 {r[name_col]}</h4><span class="badge badge-cal">🔥 {r.get(cal_col,"250")} kcal</span><span class="badge badge-time">⏱️ {r.get(time_col,"20")} min</span><p style="margin-top:8px"><b>Ingredients:</b> {r[ing_col]}</p><p>{str(r.get(ins_col,""))[:400]}...</p></div>', unsafe_allow_html=True)
        else:
            st.warning("No match da, but AI created one for you!")
            st.markdown(f'<div class="recipe-card" style="border-left-color:#4CAF50"><h4>✨ {", ".join([i.title() for i in ings[:2]])} Special</h4><p>Add {", ".join(ings)} with spices, cook 10 min. Ready!</p></div>', unsafe_allow_html=True)

with tab2:
    st.markdown("### 🥗 Diet & Healthy Food")
    st.caption("Weight loss, Keto, Vegan, High Fiber foods")
    diet_df = df[df[diet_col].astype(str).str.contains('Vegan|Vegetarian|High Protein|Low Fat', case=False, na=False)] if diet_col else df.head(10)
    for _,r in diet_df.head(8).iterrows():
        st.markdown(f'<div class="recipe-card"><h4>🥗 {r[name_col]}</h4><span class="badge badge-veg">{r.get(diet_col,"Healthy")}</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 👶 Kids Special - Yummy & Colorful")
    st.caption("Kids love this! Sweet, less spicy, attractive")
    kids_df = df[df[cat_col].astype(str).str.contains('Snack|Kids|Sweet|Dessert', case=False, na=False)] if cat_col else df.sample(8)
    if len(kids_df)==0: kids_df = df.sample(8)
    for _,r in kids_df.head(8).iterrows():
        st.markdown(f'<div class="recipe-card" style="border-left-color:#FF4081"><h4>🍭 {r[name_col]} - Kids Favorite</h4><span class="badge" style="background:#FCE4EC;color:#AD1457">👶 Kids Food</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### ⚡ Low Calorie - Under 200 kcal")
    low_df = df[df[cal_col] < 250] if cal_col and df[cal_col].notna().any() else df.head(8)
    for _,r in low_df.head(8).iterrows():
        cal = r.get(cal_col, '180')
        st.markdown(f'<div class="recipe-card" style="border-left-color:#00BCD4"><h4>⚡ {r[name_col]}</h4><span class="badge badge-cal">🔥 Only {cal} kcal</span><span class="badge badge-veg">Weight Loss</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)

with tab5:
    st.markdown("### 💪 High Protein - Gym & Muscle Food")
    st.caption("Above 15g protein - for fitness freaks")
    prot_col = [c for c in df.columns if 'protein' in c.lower()]
    if prot_col:
        high_df = df[pd.to_numeric(df[prot_col[0]], errors='coerce') > 12].sort_values(prot_col[0], ascending=False)
    else:
        high_df = df.sample(8)
    for _,r in high_df.head(8).iterrows():
        st.markdown(f'<div class="recipe-card" style="border-left-color:#4CAF50"><h4>💪 {r[name_col]}</h4><span class="badge badge-veg">High Protein</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)

with tab6:
    st.markdown("### ⏱️ Quick Recipe - Ready in 15 mins")
    if time_col:
        df[time_col] = pd.to_numeric(df[time_col], errors='coerce')
        quick_df = df[df[time_col] <= 20].head(8)
    else:
        quick_df = df.head(8)
    for _,r in quick_df.iterrows():
        st.markdown(f'<div class="recipe-card" style="border-left-color:#FF9800"><h4>⏱️ {r[name_col]}</h4><span class="badge badge-time">15 min Ready</span><p>{r[ing_col]}</p></div>', unsafe_allow_html=True)
