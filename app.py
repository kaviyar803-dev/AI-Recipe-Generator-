import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")
st.markdown("<h1 style='text-align:center; color:#FF4B4B;'>🍛 AI RECIPE GENERATOR</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Enter your ingredients, AI will find the perfect recipe for you!</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        return pd.read_csv("recipes.csv", encoding='latin1', on_bad_lines='skip', engine='python')
    except:
        try:
            return pd.read_excel("recipes.csv")
        except:
            return pd.read_csv("recipes.csv", encoding='utf-8', on_bad_lines='skip', engine='python')

df = load_data()

def find_col(keywords, default_idx):
    for kw in keywords:
        for col in df.columns:
            if kw.lower() in str(col).lower():
                return col
    return df.columns[default_idx] if len(df.columns) > default_idx else df.columns[0]

name_col = find_col(['recipe name', 'recipe', 'dish', 'name'], 1)
ing_col = find_col(['ingredient', 'main', 'items', 'material'], 3)

st.markdown("### 👨‍🍳 What Ingredients Do You Have?")
user_input = st.text_input("", placeholder="Ex: tomato, egg, onion...", label_visibility="collapsed")

c1, c2 = st.columns(2)
with c1:
    btn = st.button("🔍 Find AI Recipe", type="primary", use_container_width=True)
with c2:
    random_btn = st.button("🎲 Random Recipe", use_container_width=True)

if random_btn:
    sample = df.sample(1).iloc[0]
    with st.container(border=True):
        st.subheader(f"🎲 {sample[name_col]}")
        st.write(f"**Ingredients:** {sample[ing_col]}")
        st.balloons()

if btn and user_input:
    ings = [x.strip().lower() for x in user_input.split(",") if x.strip()!=""]
    df['score'] = df[ing_col].apply(lambda v: sum(1 for i in ings if i in str(v).lower()))
    result = df[df['score']>0].sort_values('score', ascending=False).head(5)
    if len(result)>0:
        st.success(f"Found {len(result)} recipes for '{user_input}'")
        for _, row in result.iterrows():
            with st.container(border=True):
                st.subheader(f"🍲 {row[name_col]}")
                st.write(f"**Ingredients:** {row[ing_col]}")
    else:
        with st.container(border=True):
            dish = f"{' '.join([i.title() for i in ings[:2]])} Special"
            st.subheader(f"✨ AI Generated: {dish}")
            st.write(f"Your ingredients: {user_input}")
            st.write(f"Method: Saute onion, add {', '.join(ings)}, add spices, cook 10 mins. Ready!")
            st.balloons()

if not btn and not random_btn:
    st.write(f"📚 Total {len(df)} recipes loaded")
    st.dataframe(df.head(30), use_container_width=True)
