# 🍽️ Backpackers’ Bytes  
### Smart Visual Menu Translator & Food Recommendation System  

---

## 🚩 Problem Statement

Travelers and backpackers often struggle to understand restaurant menus due to **language barriers, unfamiliar dish names, unclear pricing, and lack of dietary or health information**.  
This makes ordering food confusing, risky, and inconvenient—especially in new cities or countries.

---

## 🤔 Why This Is a Real Problem

- 📜 Menus are usually written in **local languages**
- 🍛 Dish names don’t explain **ingredients, spice level, or health impact**
- 💰 Prices may not match the user’s **currency or budget**
- 🥗 No guidance for **dietary or health-based choices**
- ❌ Static menus offer **no personalization or recommendations**

---

## 🎯 Why We Chose This Problem

- 🌍 A **real-world issue** faced by travelers every day  
- 🧠 Perfect use case for **AI + Computer Vision + Personalization**  
- 🤝 Promotes **accessibility, inclusivity, and better user experience**  
- 🚀 Scalable solution for restaurants, cafés, hotels, and travel platforms  

---

## 💡 Our Solution – Backpackers’ Bytes

**Backpackers’ Bytes** is an AI-powered smart menu assistant that transforms ordinary menu images into **interactive, personalized, and understandable experiences**.

### What It Does:
- 📸 Reads menu images using OCR  
- 🌐 Translates dish names into the user’s preferred language  
- 💱 Converts prices into the user’s selected currency  
- 🧾 Enriches dishes with:
  - Cuisine type  
  - Calories (approx.)  
  - Spice level  
  - Vegetarian / Non-Vegetarian tags  
- ⭐ Recommends the best dishes based on:
  - Budget  
  - Dietary preference  
  - Health goals (Low calorie, High protein, Low spice, etc.)  
  - Cuisine preference & eating style  

Each recommendation comes with a **clear, point-wise explanation** so users know *exactly why* a dish is suggested.

---

## 🌟 Outcome

✔ Faster decision making  
✔ Health-aware food choices  
✔ Language & currency independence  
✔ Better dining experience for travelers  

---


## 🏗️ System Architecture

Backpackers’ Bytes follows a **modular, AI-driven pipeline architecture**, ensuring scalability, clarity, and ease of integration.

---

### 🔹 1. User Interface (Streamlit Frontend)
- Users upload **one or multiple menu images**
- Select preferences such as:
  - Language
  - Currency
  - Budget
  - Dietary & health goals
  - Cuisine and eating style
- Displays:
  - Translated digital menu
  - Dish images
  - Personalized recommendations with explanations

---

### 🔹 2. Image Processing & OCR Layer
- Menu images are processed using OCR techniques
- Handles:
  - Multiple languages
  - Skewed images
  - Low lighting and noisy backgrounds
- Extracts raw textual content from menu images

---

### 🔹 3. Menu Processing Engine (`processor.py`)
- Converts raw OCR text into **structured menu data**
- Responsibilities:
  - Dish name normalization
  - Language translation
  - Currency conversion
  - Course classification (Starter, Main, Dessert, Beverage)
- Enriches dishes with metadata:
  - Calories (approx.)
  - Cuisine
  - Ingredients
  - Spice level
  - Veg / Non-Veg tags

---

### 🔹 4. Recommendation Engine (`recommender.py`)
- Scores each dish using a **multi-criteria decision logic**
- Considers:
  - User budget
  - Dietary restrictions
  - Health preferences
  - Cuisine & eating style
  - Spice tolerance
- Produces:
  - Best dish per course
  - Clear, point-wise explanation for each recommendation

---

### 🔹 5. Image Retrieval Layer
- Maps normalized dish names to stored dish images
- Enhances visual understanding of recommended items

---

### 🔹 6. Output & Explanation Layer
- Displays recommendations with:
  - Dish image
  - Price & currency
  - Health indicators
  - Bullet-point “Why this dish is recommended”
- Ensures transparency and user trust

---

### 🧠 Architecture Highlights
- ✅ Modular & maintainable design  
- ✅ AI-driven personalization  
- ✅ Supports multi-page & multi-language menus  
- ✅ Easily extendable for voice, reviews, or restaurant APIs  

---


## 🛠️ Tools, APIs & Datasets Used

### 🔧 Tools & Libraries
- **Python** – Core backend logic
- **Streamlit** – Interactive web interface
- **OCR Engine** – Text extraction from menu images
- **gTTS (optional)** – Text-to-speech support (extensible)
- **JSON** – Structured menu representation
- **OS & File Handling** – Image and dataset management

---

### 🔑 APIs
- **Google Generative AI (Gemini)**  
  Used for:
  - Menu understanding
  - Language translation
  - Dish enrichment (ingredients, cuisine, health metadata)  
  *(API key kept commented for security)*

---

### 📊 Datasets
- **Kaggle Food & Restaurant Menu Datasets**  
  Can be used as reference datasets for:
  - Dish names
  - Ingredients
  - Calories
  - Cuisine types

**Steps to use Kaggle dataset:**
1. Download a food/menu dataset from Kaggle  
2. Clean irrelevant columns  
3. Convert to structured JSON format  
4. Map dishes with enrichment fields (calories, cuisine, veg/non-veg)

---

### 🧪 Custom Dataset (Used in This Project)
- We created our **own curated dataset** by:
  - Extracting real menu images
  - Structuring dishes manually + via AI enrichment
  - Adding health, cuisine, and ingredient metadata
- Enables better personalization and real-world accuracy

---

## ▶️ How to Run the Project (Step-by-Step)

### ✅ Prerequisites
- Python **3.10 or above**
- Git installed
- Internet connection (for AI processing)

---

### 📥 1. Clone the Repository
```bash
git clone <your-github-repo-link>
cd Menu_AI
```

## 📦 2. Install Required Dependencies
```bash
pip install -r requirements.txt
```
- (If requirements.txt is not present, install manually:)
```bash
pip install streamlit easyocr opencv-python pandas numpy "skewed images" google-generativeai Structuring" & "Translation" python-dotenv Pillow requests opencv-python-headless
```

## 🔐 3. API Key Setup
- Open **processor.py**
- Add your Google Generative AI (Gemini) API key
```bash
API_KEY = "YOUR_API_KEY_HERE"
```

## ▶️ 4. Run the Application
```bash
API_KEY = "YOUR_API_KEY_HERE"
```
- The app will open automatically in your browser
- Default URL: **http://localhost:8501**

## 🖼️ How to Use the Application
📤 Upload Menu Images
- Click “Upload Menu Image(s)”
- Upload one or multiple menu images (JPG / PNG / JPEG)

## ⚙️ Set Preferences (Sidebar)
- Select:
  - Language
  - Currency
  - Budget
  - Dietary preference
  - Cuisine choice
  - Health goal
  - Spice tolerance
  - Meal plan (Starter / Main / Dessert)
 
## 🚀 Analyze Menu
- Click “Analyze Menu 🚀”
- System will:
  - Extract text using OCR
  - Translate menu items
  - Enrich dishes with AI
  - Generate structured menu data
 
## 🌟 View Recommendations
- Get course-wise smart recommendations
- See:
  - Dish image
  - Price & currency
  - Ingredients & allergens
  - Point-wise explanation for why the dish was recommended
  - Health-based reasoning (low calorie / high protein etc.)
 
## 🔁 Try Again
- Change preferences anytime
- Upload new menu images
- Re-analyze for updated recommendations
