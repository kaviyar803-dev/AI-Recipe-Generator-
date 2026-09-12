import streamlit as st
import random

st.set_page_config(page_title="AI Recipe Maker", page_icon="🍛", layout="centered")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #FFF8E1 0%, #FFE0B2 100%);}
.recipe-box {
    background:white; border-radius:20px; padding:25px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1); border:2px solid #FF8C00;
}
.ing-pill {
    display:inline-block; background:linear-gradient(90deg,#FF4B4B,#FF8C00);
    color:white; padding:8px 15px; border-radius:25px; margin:5px; font-weight:600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center; color:#FF4B4B'>🍛 Random Ingredients to Recipe Magic ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center'>Nee ingredients type pannu da, naan recipe create pannuren!</p>", unsafe_allow_html=True)

# INPUT
st.markdown("### 🧾 1. Enter Your Ingredients (comma la pirichu type pannu):")
user_input = st.text_input("", placeholder="Ex: tomato, egg, onion, cheese, bread", label_visibility="collapsed")

st.markdown("### 🎯 OR Click Random:")
if st.button("🎲 Random 5 Ingredients Kudu"):
    pool = ["tomato", "onion", "egg", "chicken", "rice", "potato", "paneer", "cheese", "bread", "milk", "oats", "mushroom", "capsicum", "carrot", "garlic", "butter", "spinach", "corn", "curd", "pepper"]
    picked = random.sample(pool, 5)
    st.session_state['random_ings'] = ", ".join(picked)
    user_input = st.session_state['random_ings']
    st.info(f"Random Pick: {user_input}")

if 'random_ings' in st.session_state and not user_input:
    user_input = st.session_state['random_ings']

# GENERATE BUTTON
if st.button("✨ Generate My Recipe!", type="primary", use_container_width=True):
    if not user_input or len(user_input.split(",")) < 2:
        st.error("Da atleast 2 ingredients type pannu da!")
    else:
        ings = [x.strip().title() for x in user_input.split(",") if x.strip()!=""]

        # AI LOGIC TO CREATE RECIPE NAME
        dish_types = ["Masala Fry", "Cheesy Delight", "Spicy Curry", "Tawa Special", "Magic Mix", "Fusion Bowl", "Quick Stir Fry"]
        dish_name = f"{ings[0]} {ings[1]} {random.choice(dish_types)}"

        # Random time & cal
        time = random.choice([10, 15, 20, 25])
        cal = random.randint(180, 450)
        protein = random.randint(8, 22)

        st.balloons()

        st.markdown(f"""
        <div class="recipe-box">
            <h2 style="color:#FF4B4B; text-align:center">👨‍🍳 {dish_name}</h2>
            <p style="text-align:center">
                <span style="background:#E3F2FD; padding:5px 12px; border-radius:20px;">🔥 {cal} kcal</span>
                <span style="background:#E8F5E9; padding:5px 12px; border-radius:20px;">💪 {protein}g Protein</span>
                <span style="background:#FFF3E0; padding:5px 12px; border-radius:20px;">⏱️ {time} min</span>
            </p>
            <hr>
            <h4>🧾 Your Ingredients:</h4>
            <p>{" ".join([f'<span class="ing-pill">{i}</span>' for i in ings])}</p>

            <h4>📝 Full Ingredients List (AI Added):</h4>
            <ul>
                <li>{", ".join(ings)} - (Your Main)</li>
                <li>1 Onion (finely chopped) - if not in your list</li>
                <li>2 tbsp Oil, Salt to taste</li>
                <li>1 tsp Chilli Powder, 1/2 tsp Garam Masala, 1/2 tsp Turmeric</li>
                <li>Coriander leaves for garnish</li>
            </ul>

            <h4>👩‍🍳 How to Cook - Step by Step:</h4>
            <p>
            <b>Step 1:</b> Kadai la oil sooda panni, <b>{ings[-1] if len(ings)>1 else 'onion'}</b> ah light brown vara vathakku.<br><br>
            <b>Step 2:</b> Ippo <b>{ings[0]}</b> add panni 2 mins saute pannu. Nalla smell varum.<br><br>
            <b>Step 3:</b> <b>{", ".join(ings[1:3])}</b> add pannu, salt, chilli, garam masala ellam potu mix pannu.<br><br>
            <b>Step 4:</b> Konjam thanni (50ml) vittu moodi vechu <b>{time-5} mins</b> low flame la cook pannu.<br><br>
            <b>Step 5:</b> Last ah mela coriander thooti, 1 min aprom stove off pannu. <b>{dish_name} Ready da! 😋</b>
            </p>

            <div style="background:#FFF3E0; padding:12px; border-radius:12px; margin-top:15px">
                <b>💡 Chef Tip:</b> Itha <b>{ings[0]} Rice</b> kooda illa <b>Hot Roti</b> kooda sapta semma combo da! Konjam Lemon juice vitta taste innum super!
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"🎉 {dish_name} created using only your: {', '.join(ings)}")

# Footer
st.markdown("<p style='text-align:center; margin-top:30px; color:#999'>Made with ❤️ - User Ingredients = AI Recipe Magic</p>", unsafe_allow_html=True)
