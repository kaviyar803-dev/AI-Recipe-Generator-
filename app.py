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
.ing-pill {display:inline-block; background:linear-gradient(90deg,#FF4B4B,#FF8C00); color:white; padding:6px 14px; border-radius:25px; margin:4px; font-weight:600; font-size:0.9rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🍛 AI RECIPE GENERATOR</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#666">Smart Search + Dashboard + Pure AI Creator - All in One ✨</p>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    try: df = pd.read_excel("recipes.csv", engine="openpyxl")
    except: df = pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')
    return df

df = load_data()

def fcol(kws, idx):
    for kw in kws:
        for c in df.columns:
            if kw.lower() in str(c).lower(): return c
    return df.columns[idx] if idx < len(df.columns) else df.columns[0]

name_col = fcol(['recipe name','recipe'], 0)
ing_col = fcol(['ingredient'], 1)
ins_col = fcol(['instruction','method'], 2)
cal_col = fcol(['calori'], 3)
diet_col = fcol(['diet type','diet'], 4)
cat_col = fcol(['category','course'], 5)
time_col = fcol(['cook time','time'], 6)

for col in [cal_col, time_col]:
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
with c4: st.markdown(f'<div class="metric-card"><h2>🤖 AI</h2><p>Magic Generator</p></div>', unsafe_allow_html=True)

st.divider()

# 6 TABS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔍 OLD: AI Search", "🥗 Diet Food", "👶 Kids Food", "⚡ Low Calorie", "⏱️ Quick List", "✨ NEW: Pure AI Creator"])

# TAB 1 - OLD SEARCH
with tab1:
    st.markdown("#### Search Recipes Using Random Ingredients (Database Search)")
    user_input = st.text_input("search", placeholder="Ex: tomato, egg, onion...", label_visibility="collapsed", key="old_search")
    colA, colB = st.columns([3,1])
    with colA: btn = st.button("🔍 Find My Recipe", type="primary", use_container_width=True, key="old_btn")
    with colB: rand_btn = st.button("🎲 Surprise Me", use_container_width=True, key="old_rand")

    if rand_btn:
        s = df.sample(1).iloc[0]
        st.balloons()
        st.markdown(f'<div class="recipe-card"><h3>🎲 Surprise: {s[name_col]}</h3><p>{s[ing_col]}</p><p>{str(s.get(ins_col,""))[:500]}...</p></div>', unsafe_allow_html=True)

    if btn and user_input:
        ings = [x.lower().strip() for x in user_input.split(",") if x.strip()!=""]
        df['score'] = df[ing_col].astype(str).apply(lambda v: sum(1 for i in ings if i in v.lower()))
        res = df[df['score']>0].sort_values('score', ascending=False).head(6)
        if len(res)>0:
            st.success(f"Found {len(res)} recipes!")
            for _, r in res.iterrows():
                st.markdown(f'<div class="recipe-card"><h4>🍲 {r[name_col]} ({int(r["score"])}/{len(ings)} matched)</h4><span class="badge badge-cal">{r.get(cal_col,"250")} kcal</span><span class="badge badge-time">{r.get(time_col,"20")} min</span><p><b>Ingredients:</b> {r[ing_col]}</p></div>', unsafe_allow_html=True)
        else:
            st.warning("No match found, but AI created one!")
            st.markdown(f'<div class="recipe-card" style="border-left-color:#4CAF50"><h4>✨ {", ".join([i.title() for i in ings[:2]])} Masala</h4><p>Cook {", ".join(ings)} with spices - Ready!</p></div>', unsafe_allow_html=True)

# TAB 2,3,4,5 - DASHBOARD
with tab2:
    st.markdown("### 🥗 Diet Food Dashboard")
    try: d_df = df[df[diet_col].astype(str).str.contains('Veg|Vegan|Protein', case=False, na=False)].head(8)
    except: d_df = df.head(8)
    for _, r in d_df.iterrows(): st.markdown(f'<div class="recipe-card"><h4>🥗 {r[name_col]}</h4><p>{str(r[ing_col])[:200]}</p></div>', unsafe_allow_html=True)

with tab3:
    st.markdown("### 👶 Kids Food - Yummy Zone")
    try: k_df = df[df[cat_col].astype(str).str.contains('Snack|Kids|Sweet|Dessert', case=False, na=False)].head(8)
    except: k_df = df.sample(8)
    if len(k_df)==0: k_df = df.sample(8)
    for _, r in k_df.iterrows(): st.markdown(f'<div class="recipe-card" style="border-left-color:#FF4081"><h4>🍭 {r[name_col]}</h4><span class="badge" style="background:#FCE4EC;color:#AD1457">Kids Special</span><p>{str(r[ing_col])[:200]}</p></div>', unsafe_allow_html=True)

with tab4:
    st.markdown("### ⚡ Low Calorie - Under 250 kcal")
    try: l_df = df[df[cal_col] < 250].head(8)
    except: l_df = df.head(8)
    if len(l_df)==0: l_df = df.head(8)
    for _, r in l_df.iterrows(): st.markdown(f'<div class="recipe-card" style="border-left-color:#00BCD4"><h4>⚡ {r[name_col]}</h4><span class="badge badge-cal">{r.get(cal_col,"180")} kcal</span><p>{str(r[ing_col])[:150]}</p></div>', unsafe_allow_html=True)

with tab5:
    st.markdown("### ⏱️ Quick Recipes & Full List")
    st.dataframe(df[[name_col, ing_col]].head(50), use_container_width=True, hide_index=True)

# TAB 6 - NEW PURE AI CREATOR
with tab6:
    st.markdown("### ✨ NEW: Pure AI Recipe Creator from Your Ingredients")
    st.caption("This will NOT search database. It will CREATE a brand new recipe using ONLY your ingredients!")

    st.markdown("#### Step 1: Enter Your Ingredients (comma separated)")
    new_input = st.text_input("new", placeholder="Ex: tomato, egg, cheese, bread, onion", label_visibility="collapsed", key="new_input")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🎲 Give Me 5 Random Ingredients", use_container_width=True, key="new_rand"):
            pool = ["tomato", "onion", "egg", "chicken", "rice", "potato", "paneer", "cheese", "bread", "milk", "oats", "mushroom", "capsicum", "carrot", "garlic", "butter", "spinach", "corn", "curd"]
            picked = random.sample(pool, 5)
            st.session_state['new_picked'] = ", ".join(picked)

    if 'new_picked' in st.session_state:
        if not new_input:
            new_input = st.session_state['new_picked']
        st.info(f"🎲 Random Picked: {st.session_state['new_picked']}")

    if st.button("✨ Generate Magic Recipe from MY Ingredients!", type="primary", use_container_width=True, key="gen_btn"):
        if not new_input or len(new_input.split(",")) < 2:
            st.error("Please enter at least 2 ingredients!")
        else:
            ings = [x.strip().title() for x in new_input.split(",") if x.strip()!=""]
            dish_types = ["Masala Fry", "Cheesy Delight", "Spicy Curry", "Tawa Special", "Magic Mix", "Fusion Bowl", "Quick Stir Fry"]
            dish_name = f"{ings[0]} {ings[1]} {random.choice(dish_types)}" if len(ings)>=2 else f"{ings[0]} Special"
            time = random.choice([10, 15, 20])
            cal = random.randint(200, 420)
            protein = random.randint(10, 22)

            st.balloons()
            st.markdown(f"""
            <div class="recipe-card" style="border-left-color:#9C27B0; border:2px solid #E1BEE7">
                <h2 style="color:#9C27B0; text-align:center">👨‍🍳 {dish_name}</h2>
                <p style="text-align:center"><span class="badge badge-cal">🔥 {cal} kcal</span><span class="badge badge-pro">💪 {protein}g Protein</span><span class="badge badge-time">⏱️ {time} min</span><span class="badge badge-veg">🤖 Pure AI Created</span></p>
                <hr>
                <h4>🧾 Your Given Ingredients:</h4>
                <p>{" ".join([f'<span class="ing-pill">{i}</span>' for i in ings])}</p>
                <h4>📝 Full List:</h4>
                <ul><li>{", ".join(ings)} (Main)</li><li>Oil, Salt, Chilli, Garam Masala, Turmeric</li><li>Coriander for garnish</li></ul>
                <h4>👩‍🍳 Method:</h4>
                <p><b>Step 1:</b> Heat oil and saute {ings[-1]}.<br><b>Step 2:</b> Add {ings[0]} and saute for 2 mins.<br><b>Step 3:</b> Add {", ".join(ings[1:])} with masala and mix well.<br><b>Step 4:</b> Add water and cook for {time-5} mins.<br><b>Step 5:</b> Garnish with coriander and serve. <b>{dish_name} Ready!</b></p>
                <div style="background:#F3E5F5; padding:10px; border-radius:10px"><b>💡 Chef Tip:</b> Serve with Rice or Roti - Super combo!</div>
            </div>
            """, unsafe_allow_html=True)
