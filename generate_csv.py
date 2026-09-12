import pandas as pd
import numpy as np
np.random.seed(42)
base = [("Tomato Rice","tomato"),("Egg Bhurji","egg"),("Chicken Curry","chicken"),("Sambar Rice","toor dal"),("Paneer Butter Masala","paneer"),("Lemon Rice","rice"),("Fish Fry","fish"),("Veg Pulao","rice"),("Chicken Biryani","chicken"),("Curd Rice","curd")]
pool = ["tomato","onion","egg","rice","chicken","paneer","potato","curd","milk","spinach","carrot","beans","cabbage","cauliflower","peas","mushroom","fish","mutton","garlic","ginger","lemon","peanut","coconut","tamarind","toor dal","moong dal","basmati rice","besan","butter","coriander"]
adj = ["Masala","Special","Chettinad","Hyderabadi","Quick","Healthy","Spicy","Homestyle","Village Style"]
recipes=[]
for i in range(1,501):
    b_name,b_ing = base[np.random.randint(0,len(base))]
    name = f"{adj[np.random.randint(0,len(adj))]} {b_name} {i}" if i>15 else b_name
    chosen = np.random.choice(pool, np.random.randint(3,6), replace=False).tolist()
    if b_ing not in chosen: chosen[0]=b_ing
    diet = ["Veg","Veg","Veg","Non-Veg"][np.random.randint(0,4)]
    cat = ["Breakfast","Lunch","Dinner","Snack"][np.random.randint(0,4)]
    recipes.append([f"RECIPE{i:03d}",name,", ".join(chosen),cat,diet,int(np.random.randint(10,70)),int(np.random.randint(120,550)),int(np.random.randint(4,35)),int(np.random.randint(10,60)),int(np.random.randint(3,25)),f"Cook {', '.join(chosen)} for {np.random.randint(10,70)} mins",round(float(np.random.uniform(3.8,4.9)),1),["Weight Loss","Muscle Gain","Balanced"][np.random.randint(0,3)]])
df=pd.DataFrame(recipes,columns=["id","name","ingredients","category","diet_type","cook_time_min","calories","protein_g","carbs_g","fat_g","steps","rating","goal"])
df.to_csv("recipes.csv",index=False)
print("500 recipes.csv created!")
