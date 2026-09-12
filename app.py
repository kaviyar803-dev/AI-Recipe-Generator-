import streamlit as st
import pandas as pd
import random
import glob

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")
st.markdown("<h1 style='text-align:center;color:#FF4B4B;'>🍛 AI RECIPE GENERATOR</h1>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # File-a auto kandupidikkum
    try:
        files = glob.glob("**/*.csv", recursive=True)
        for f in files:
            try:
                df = pd.read_csv(f)
                if len(df) > 10: # Correct file
                    return df
            except:
                continue
        # xlsx try pannum
        files = glob.glob("**/*.xlsx", recursive=True)
        for f in files:
            try:
                df = pd.read_excel(f)
                if len(df) > 10:
                    return df
            except:
                continue
    except:
        pass
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("recipes.csv file kedaikala da! Check pannu")
    st.stop()

# --- AUTO FIND COLUMNS - ithan trick da! ---
cols = [c.lower() for c in df.columns]
# Name column kandupidikkum
name_col = next((c for c in df.columns if 'recipe' in c.lower() or c.lower()=='name'), df.columns[1])
# Ingredients column kandupidikkum
ing_col = next((c for c in df.columns if 'ingred' in c.lower()), None)
if not ing_col:
    ing_col = next((c for c in df.columns if 'main' in c.lower()), df.columns[2])

st.write(f"DEBUG: Using columns -> Name: `{name_col}`, Ingredients: `{ing_col}`") # Ithu work aana aprom delete pannidalam

# --- MAIN AI BOX ---
st.markdown("### 👨‍🍳 Un kitta enna irukku? Type pannu da")
user_input = st.text_input("", placeholder="Ex: tomato, egg, onion, rice...")

if st.button("🔍 AI Recipe Thedu", type="primary"):
    if not user_input:
        st.warning("Edhavathu type pannu da!")
    else:
        ings = [i.strip().lower() for i in user_input.split(",") if i.strip()!=""]

        # Matching
        def get_score(val):
            val = str(val).lower()
            return sum(1 for i in ings if i in val)

        df['score'] = df[ing_col].apply(get_score)
        matched = df[df['score']>0].sort_values('score', ascending=False).head(6)

        if len(matched) > 0:
            st.success(f"AI Found {len(matched)} recipes for {user_input}")
            for _, r in matched.iterrows():
                with st.container(border=True):
                    st.subheader(f"🍲 {r[name_col]}")
                    st.write(f"**Ingredients:** {r[ing_col]}")
                    # vera info iruntha kaamikkum
                    if 'Region / Cuisine' in df.columns:
                        st.caption(f"Region: {r['Region / Cuisine']} | Diet: {r.get('Diet Type','')}")
        else:
            st.warning("Exact match illa da, AI pudhusa create pannuthu!")
            with st.container(border=True):
                new_name = f"{' '.join([x.title() for x in ings[:2]])} Masala Special"
                st.subheader(f"✨ AI Generated: {new_name}")
                st.write(f"**Un ingredients:** {user_input}")
                steps = f"1. Kadai la oil vittu onion ah vathakku.\n2. {', '.join(ings)} add pannu.\n3. Salt, chilli, garam masala pottu 10 min cook pannu.\n4. Kothamalli thooti serve pannu - {new_name} ready da!"
                st.write(steps)
                st.balloons()
else:
    st.info("Mela ingredients potu button click pannu da")
    st.dataframe(df.head(30), use_container_width=True)
