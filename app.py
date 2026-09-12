import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")
st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🍛 AI RECIPE GENERATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Enter your ingredients, AI will find the perfect recipe for you!</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        # CSV try pannum, thappu lines ah skip pannidum
        return pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')
    except:
        try:
            # CSV illa na Excel ah try pannum (nee rename panna file)
            return pd.read_excel("recipes.csv")
        except:
            # Rendume illa na vera file thedum
            import glob
            f = glob.glob("**/*.xlsx", recursive=True)[0]
            return pd.read_excel(f)

df = load_data()
name_col = [c for c in df.columns if 'Recipe' in c][0] if any('Recipe' in c for c in df.columns) else df.columns[1]
ing_col = [c for c in df.columns if 'Ingredient' in c][0] if any('Ingredient' in c for c in df.columns) else df.columns[4]

st.markdown("### 👨‍🍳 What Ingredients Do You Have?")
user_input = st.text_input("Ingredients", placeholder="Ex: tomato, egg, onion, chicken, rice...", label_visibility="collapsed")

c1, c2 = st.columns(2)
with c1:
    btn = st.button("🔍 Find AI Recipe", type="primary", use_container_width=True)
with c2:
    random_btn = st.button("🎲 Random Recipe", use_container_width=True)

if random_btn:
    sample = df.sample(1).iloc[0]
    with st.container(border=True):
        st.subheader(f"🎲 Random Pick: {sample[name_col]}")
        st.write(f"**Ingredients:** {sample[ing_col]}")

if btn and user_input:
    ings = [x.strip().lower() for x in user_input.split(",")]
    df['score'] = df[ing_col].apply(lambda v: sum(1 for i in ings if i in str(v).lower()))
    result = df[df['score']>0].sort_values('score', ascending=False).head(5)

    if len(result)>0:
        st.success(f"Found {len(result)} recipes for '{user_input}'")
        for _, row in result.iterrows():
            with st.container(border=True):
                st.subheader(f"🍲 {row[name_col]}")
                st.write(f"**Ingredients:** {row[ing_col]}")
                if 'Instructions' in df.columns:
                    st.write(f"**Method:** {str(row['Instructions'])[:500]}...")
    else:
        with st.container(border=True):
            dish = f"{' '.join([i.title() for i in ings[:2]])} Masala Special"
            st.subheader(f"✨ AI Generated: {dish}")
            st.write(f"**Your Ingredients:** {user_input}")
            st.write(f"**Recipe:** Saute onion & tomato, add {', '.join(ings)}, add spices, cook for 10 mins. Your {dish} is ready!")
            st.balloons()
elif btn:
    st.warning("Please enter at least one ingredient!")

if not btn and not random_btn:
    st.divider()
    st.write(f"📚 Total {len(df)} Recipes Available")
    st.dataframe(df.head(50), use_container_width=True)
