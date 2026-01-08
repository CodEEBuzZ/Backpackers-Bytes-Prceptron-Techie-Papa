import streamlit as st
import os
from processor import MenuProcessor
from recommender import DishRecommender

def normalize_dish_name(name):
    name = (
        name.lower()
        .strip()
        .replace("&", "and")
        .replace("-", "_")
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
        .replace("*", "")
        .replace(",", "")
        .replace(".", "")
        .replace("/", "")
    )

    while "__" in name:
        name = name.replace("__", "_")

    return name.strip("_")


def get_dish_image_path(dish_name):
    base_dir = os.path.join(os.getcwd(), "dish_images")
    normalized = normalize_dish_name(dish_name)

    dish_dir = os.path.join(base_dir, normalized)

    if os.path.exists(dish_dir):
        images = [
            f for f in os.listdir(dish_dir)
            if f.lower().endswith((".jpg", ".png", ".jpeg"))
        ]
        if images:
            return os.path.join(dish_dir, images[0])

    return None


# Page Configuration
st.set_page_config(page_title="Menu AI - Backpackers' Bytes", layout="wide")

st.title("🍽️ Smart Visual Menu Translator")
st.markdown("**Perceptron 2026 Hackathon Project**")

# ==========================================
# SIDEBAR: ADVANCED USER PREFERENCES
# ==========================================
st.sidebar.header("User Customization")

# 1. Output Language
language_options = [
    "English", "Hindi", "Bengali", "Korean", "Japanese", "French",
    "Spanish", "German", "Chinese (Simplified)", "Italian", "Russian",
    "Arabic", "Portuguese", "Tamil", "Telugu", "Marathi", "Urdu"
]
target_language = st.sidebar.selectbox(
    "Translate Dish Names To:",
    options=language_options,
    index=0
)

# 2. Currency Selection
currency_options = [
    "INR (₹)", "USD ($)", "EUR (€)", "GBP (£)",
    "JPY (¥)", "KRW (₩)", "AUD ($)", "CAD ($)", "AED (dh)"
]
target_currency = st.sidebar.selectbox(
    "My Currency:",
    options=currency_options,
    index=0
)

# 3. Budget
budget = st.sidebar.number_input(
    "My Budget (per person):",
    min_value=0,
    value=1000,
    step=50
)

# 4. Dietary Preference
st.sidebar.write("### Dietary Preference")
dietary_choice = st.sidebar.radio(
    "I prefer to eat:",
    options=["Vegetarian Only 🥦", "Non-Vegetarian Only 🍗", "Mix (Any) 🥘"],
    index=2
)

# 4.1 Cuisine Preference
st.sidebar.write("### Cuisine Preference")
preferred_cuisines = st.sidebar.multiselect(
    "Choose cuisines you like:",
    options=[
        "Indian", "Italian", "Chinese", "Japanese", "Korean",
        "Mexican", "Thai", "French", "Mediterranean", "American"
    ],
    default=[]
)

# 4.2 Eating Style
st.sidebar.write("### Eating Style")
eating_style = st.sidebar.radio(
    "How do you want to eat today?",
    options=[
        "Familiar 😌 (Known tastes)",
        "Experimental 🧪 (Try something new)",
        "Balanced ⚖️ (Both)"
    ],
    index=2
)


# 5. Spice Tolerance
spice = st.sidebar.select_slider(
    "Spice Tolerance:",
    options=["Low", "Medium", "High"]
)

# 5.1 Health Preference
st.sidebar.write("### Health Preference")
health_goal = st.sidebar.radio(
    "I want food that is:",
    options=[
        "No Preference",
        "Low Calorie 🥗",
        "High Protein 💪",
        "Light & Easy to Digest 🧘",
        "Low Spice 🌶️"
    ],
    index=0
)

# 6. Meal Plan
st.sidebar.write("### Meal Plan")
course_preference = st.sidebar.radio(
    "What are you looking for?",
    options=[
        "Full Meal (Starter + Main + Dessert)",
        "Main Course Only",
        "Starter Only",
        "Dessert Only",
        "Surprise Me (Any)"
    ]
)

# ------------------------------------------
# ADVANCED COURSE SELECTION
# ------------------------------------------
multi_course_selection = []

if course_preference in ["Surprise Me (Any)", "Full Meal (Starter + Main + Dessert)"]:
    multi_course_selection = ["Starter", "Main Course", "Dessert", "Beverage"]
else:
    st.sidebar.write("### Choose Course(s)")
    multi_course_selection = st.sidebar.multiselect(
        "Select one or more:",
        options=["Starter", "Main Course", "Dessert", "Beverage"],
        default=[
            "Main Course" if "Main Course" in course_preference else
            "Starter" if "Starter" in course_preference else
            "Dessert"
        ]
    )

# Preferences dictionary
preferences = {
    "language": target_language,
    "currency": target_currency,
    "budget": budget,
    "dietary_type": dietary_choice,
    "spice_tolerance": spice,
    "course_preference": course_preference,
    "multi_course_selection": multi_course_selection,
    "preferred_cuisines": preferred_cuisines,
    "eating_style": eating_style,
    "health_goal": health_goal

}

# ==========================================
# MAIN APP LOGIC
# ==========================================

uploaded_files = st.file_uploader(
    "Upload Menu Image(s)",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    col1, col2 = st.columns(2)

    # --------------------
    # IMAGE PREVIEW
    # --------------------
    with col1:
        st.subheader("📷 Uploaded Menu Images")
        img_cols = st.columns(len(uploaded_files))

        for idx, file in enumerate(uploaded_files):
            with img_cols[idx]:
                st.image(file, caption=f"Menu {idx + 1}", use_container_width=True)

    # --------------------
    # ANALYZE BUTTON
    # --------------------
    with col2:
        if st.button("Analyze Menu 🚀"):

            with st.spinner(f"Reading Menu & Translating to {target_language}..."):
                processor = MenuProcessor()
                recommender = DishRecommender()

                combined_menu = []

                for file in uploaded_files:
                    raw_text = processor.extract_text_from_image(file)

                    menu_json = processor.structure_menu_data(
                        raw_text,
                        target_language=target_language,
                        target_currency=target_currency
                    )

                    if isinstance(menu_json, list):
                        combined_menu.extend(menu_json)

                st.success("Menu Digitized!")

            # --------------------
            # DISPLAY MENU JSON
            # --------------------
            st.subheader(f"📖 Menu in {target_language}")
            st.json(combined_menu)

            # --------------------
            # RECOMMENDATION
            # --------------------

            with st.spinner("Finding the perfect dish based on your settings..."):

                course_results = recommender.recommend_course_wise(
                    combined_menu,
                    preferences
                )

                st.divider()
                st.subheader("🌟 Recommended for You")

                if course_results:
                    for course, data in course_results.items():
                        dish = data["dish"]
                        reason = data["reason"]

                        st.markdown(f"### 🍽️ Best {course}")
                        st.write(f"**{dish.get('translated_name')}** ({dish.get('dish_name')})")
                        # 🔹 Always use English name for image lookup
                        image_key_name = dish.get("dish_name") or dish.get("translated_name")
                    
                        image_path = get_dish_image_path(image_key_name)
                        # 🔍 DEBUG: show resolved image path

                        if image_path:
                            st.image(image_path, caption=image_key_name, use_container_width=True)
                        else:
                            st.warning("📷 Image not available for this dish")
                        st.write(f"💰 Price: {dish.get('price')} {dish.get('currency')}")
                        st.markdown("### ✅ Why this dish is recommended")

                        for r in reason:
                            st.markdown(f"- {r}")

                        st.write(f"📝 Description: {dish.get('description')}")
                        # 🧾 Ingredient list (if available)
                        enrich = dish.get("enrichment", {})
                        ingredients = enrich.get("ingredients", [])
                        if ingredients:
                            st.write(f"🧾 Ingredients: {', '.join(ingredients)}")

                        # 🔔 Allergen Indicators
                        enrich = dish.get("enrichment", {})
                        allergens = enrich.get("allergens", [])

                        if allergens:
                            st.write(f"⚠️ Allergens: {', '.join(allergens)}")
                        else:
                            st.write("✅ No common allergens detected")
                        dish_name = dish.get("translated_name") or dish.get("dish_name")

                    st.stop()

                # Fallback single recommendation
                best_dish, reason = recommender.recommend(combined_menu, preferences)

                if best_dish:
                    st.info(f"**{best_dish.get('translated_name')}** ({best_dish.get('dish_name')})")
                    st.write(f"💰 Price: {best_dish.get('price')} {best_dish.get('currency')}")
                    st.markdown("### ✅ Why this dish is recommended")
                    for r in reason:
                        st.markdown(f"- {r}")

                    st.write(f"📝 Description: {best_dish.get('description')}")

                    enrich = best_dish.get("enrichment", {})
                    st.write(f"🔥 Calories: {enrich.get('calories_approx', 'N/A')} kcal")
                    st.write(f"🌍 Cuisine: {enrich.get('cuisine', 'Unknown')}")
                    # 🔹 Regional cuisine display
                    region = enrich.get("region")
                    if region:
                        st.write(f"📍 Region: {region}")

                    allergens = enrich.get("allergens", [])
                    if allergens:
                        st.write(f"⚠️ Allergens: {', '.join(allergens)}")
                    else:
                        st.write("✅ No common allergens detected")

                else:
                    st.warning(
                        "No dish matched all filters perfectly. "
                        "Try adjusting budget or course selection."
                    )
