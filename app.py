import streamlit as st
import pandas as pd
import plotly.express as px
import os
import glob

st.set_page_config(page_title="AI RECIPE GENERATOR", page_icon="🍛", layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍛 AI RECIPE GENERATOR</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>500+ Indian Recipes - AI Powered</h3>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Auto find file - csv or xlsx, root or folder la
    files = glob.glob("**/recipes.*", recursive=True) + glob.glob("recipes.*")
    for f in files:
        try:
            if f.endswith(".xlsx"):
                return pd.read_excel(f)
            else:
                return pd.read_csv(f)
        except:
            continue
    # If not found, create dummy data so site opens
    data = {"name":["Tomato Rice","Egg Bhurji","Chicken Curry"],"ingredients":["tomato, rice","egg, onion","chicken, masala"],"calories":[250,180,320],"protein_g":[6,12,25],"cook_time_min":[20,15,40],"rating":[4.5,4.6,4.8],"goal":["Balanced","Muscle Gain","Muscle Gain"],"diet_type":["Veg","Non-Veg","Non-Veg"]}
    return pd.DataFrame(data)

df = load_data()

st.sidebar.header("🔍 AI FILTER")
user_ing = st.sidebar.text_input("Ingredients (tomato, egg, rice)", "")
goal = st.sidebar.selectbox("Goal", ["All", "Weight Loss", "Muscle Gain", "Balanced"])
diet = st.sidebar.selectbox("Diet", ["All", "Veg", "Non-Veg"])

filtered = df.copy()
if user_ing:
    ings = [x.strip().lower() for x in user_ing.split(",")]
    filtered = filtered[filtered['ingredients'].astype(str).apply(lambda x: any(i in x.lower() for i in ings))]
if goal!= "All" and "goal" in filtered.columns:
    filtered = filtered[filtered['goal'] == goal]
if diet!= "All" and "diet_type" in filtered.columns:
    filtered = filtered[filtered['diet_type'] == diet]

st.subheader(f"✅ Found {len(filtered)} Recipes")
st.dataframe(filtered.head(30))

if user_ing and len(filtered)>0:
    st.success(f"🤖 AI Created: {user_ing.title()} Special Bowl - {filtered.iloc[0]['calories']} kcal!")

if len(filtered)>0 and "cook_time_min" in filtered.columns:
    fig = px.scatter(filtered.head(50), x="cook_time_min", y="calories", color="diet_type" if "diet_type" in filtered.columns else None, hover_name="name", title="AI Analysis - Calories vs Time")
    st.plotly_chart(fig)

st.balloons()
