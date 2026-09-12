import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Recipe Generator", layout="wide")
st.title("🤖 AI POWERED RECIPE GENERATOR")

@st.cache_data
def load_data():
    return pd.read_csv("recipes.csv")

df = load_data()

# Sidebar - User Input
st.sidebar.header("Un kitta enna irukku?")
user_text = st.sidebar.text_input("Ingredients (ex: tomato, egg)")
goal = st.sidebar.selectbox("Goal", ["All", "Weight Loss", "Quick <15min"])
diet = st.sidebar.selectbox("Veg/Non-Veg", ["All", "Veg", "Non-Veg"])

# AI Logic
if st.sidebar.button("Generate Recipe"):
    if user_text == "":
        st.warning("Ingredients type pannu da!")
    else:
        user_ing = [x.strip().lower() for x in user_text.split(',')]

        # AI Filter Logic
        result = df[df['ingredients'].apply(lambda x: any(i in x.lower() for i in user_ing))]

        if goal == "Weight Loss":
            result = result[result['calories'] < 300]
        if goal == "Quick <15min":
            result = result[result['cook_time'] <= 15]
        if diet!= "All":
            result = result[result['diet_type'] == diet]

        st.success(f"AI Found {len(result)} recipes for {', '.join(user_ing)}")

        # Dashboard - ADSS maathiri
        c1,c2,c3 = st.columns(3)
        c1.metric("Total Found", len(result))
        if len(result)>0:
            c2.metric("Avg Calories", round(result['calories'].mean(),1))
            c3.metric("Avg Time", f"{round(result['cook_time'].mean(),1)} min")

        # Table
        st.dataframe(result[['recipe_id','recipe_name','cook_time','calories','diet_type']])

        # AI Generated New Recipe Card
        if len(result)>0:
            top = result.iloc[0]
            st.subheader(f"✨ AI SPECIAL: {top['recipe_name']}")
            st.write(f"**Ingredients:** {top['ingredients']}")
            st.write(f"**Steps:** {top['steps']}")
            st.write(f"**AI Nutrition Tip:** Idhu {goal} ku semma da! Protein high!")

        # Chart
        if len(result)>0:
            fig = px.scatter(result, x="cook_time", y="calories", color="diet_type", hover_data=["recipe_name"])
            st.plotly_chart(fig)
else:
    st.info("Sidebar la ingredients type panni Generate button ah click pannu da!")

    # Default dashboard
    fig2 = px.bar(df['category'].value_counts(), title="Category wise Recipes")
    st.plotly_chart(fig2)

