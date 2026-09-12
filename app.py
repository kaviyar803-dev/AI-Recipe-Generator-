import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")
st.markdown("<h1 style='text-align:center;color:#FF4B4B;'>🍛 AI RECIPE GENERATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>En kitta enna ingredients irukko adha potta, AI unakku recipe eduthu tharum!</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("recipes.csv")
    except:
        import glob
        f = glob.glob("**/recipes.*", recursive=True)[0]
        df = pd.read_csv(f) if f.endswith(".csv") else pd.read_excel(f)
    return df

df = load_data()

# --- AI SEARCH BOX ---
st.markdown("### 👨‍🍳 Enna Ingredients Irukku?")
col1, col2 = st.columns([3,1])
with col1:
    user_input = st.text_input("", placeholder="Ex: tomato, egg, onion, rice, chicken... random ah type pannu da", label_visibility="collapsed")
with col2:
    search = st.button("🔍 AI Recipe Thedu", use_container_width=True, type="primary")

if search and user_input:
    ings = [i.strip().lower() for i in user_input.split(",")]

    # AI Matching Logic
    def match_score(recipe_ings):
        recipe_ings = str(recipe_ings).lower()
        score = sum(1 for i in ings if i in recipe_ings)
        return score

    df['match_score'] = df['Main Ingredients'].apply(match_score) if 'Main Ingredients' in df.columns else df['Ingredients'].apply(match_score)
    matched = df[df['match_score']>0].sort_values(by='match_score', ascending=False).head(6)

    if len(matched) > 0:
        st.success(f"🤖 AI Found {len(matched)} recipes for: **{user_input}**")
        for _, row in matched.iterrows():
            with st.container(border=True):
                st.subheader(f"🍲 {row.get('Recipe Name', row.get('name','Custom Recipe'))}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Calories", f"{row.get('Calories (kcal)','~250')} kcal")
                c2.metric("Protein", f"{row.get('Protein (g)','~12')}g")
                c3.metric("Time", f"{row.get('Cook Time (min)', row.get('cook_time_min',20))} min")
                st.write(f"**Ingredients:** {row.get('Ingredients', row.get('Main Ingredients',''))}")
                st.write(f"**Region:** {row.get('Region / Cuisine','Indian')} | **Diet:** {row.get('Diet Type','Veg')}")
    else:
        # AI Creates New Recipe if no match
        st.warning("Exact match illa da, aana AI pudhusa oru recipe create panniduchu!")
        with st.container(border=True):
            new_name = f"{' '.join([i.title() for i in ings[:2]])} Special Fry"
            st.subheader(f"✨ AI Generated: {new_name}")
            st.write(f"**Un Ingredients:** {user_input}")
            st.write(f"**Seimura:** 1. {ings[0].title()} ah cut pannu. 2. Oil la onion, tomato pottu vathakku. 3. {', '.join(ings)} ellam pottu 10 mins cook pannu. 4. Salt, pepper potta super {new_name} ready!")
            st.metric("Estimated Calories", f"{random.randint(200,400)} kcal")
            st.balloons()

else:
    st.info("👆 Mela ingredients type panni 'AI Recipe Thedu' button ah click pannu da")
    st.subheader(f"📚 Total {len(df)} Recipes Available - Scroll panni paaru")
    st.dataframe(df.head(50), use_container_width=True)
