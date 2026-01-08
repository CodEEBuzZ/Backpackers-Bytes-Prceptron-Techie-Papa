import easyocr
import google.generativeai as genai
import json
import cv2
import numpy as np

# --- CONFIGURATION ---
# PASTE YOUR API KEY HERE
API_KEY = "AIzaSyAWLZMveGT19FDWI0LWudbEuTXMQFqiwRQ"
genai.configure(api_key=API_KEY)

class MenuProcessor:
    def __init__(self):
        # Initialize EasyOCR (English is usually enough for OCR, AI handles translation)
        self.reader = easyocr.Reader(['en']) 
        # Use the model you confirmed works
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def extract_text_from_image(self, image_bytes):
        """
        Takes raw image bytes -> OpenCV Image -> Raw Text
        """
        file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        
        # detail=0 returns just the text list
        result = self.reader.readtext(image, detail=0)
        return " ".join(result)

    def structure_menu_data(self, raw_text, target_language="English", target_currency="INR"):
        """
        Uses Gemini to structure, translate, and enrich the menu data.
        """
        
        # We update the prompt to handle the User's specific requirements
        prompt = f"""
        You are an AI Menu Digitizer. 
        I will give you raw text from a restaurant menu. 
        
        Your tasks:
        1. Parse dish names, prices, and descriptions.
        2. TRANSLATE the 'translated_name' to {target_language}.
        3. CONVERT the price roughly to {target_currency} (assume current rates).
        4. CLASSIFY the dish type: 'Starter', 'Main Course', 'Dessert', or 'Beverage'.
        5. ENRICH data: Guess cuisine, regional cuisine (sub-region), spice level, is_veg, calories, possible food allergens, and main ingredients(2-5 commonly known ingredients).
           Allergens can include: Milk, Eggs, Nuts, Peanuts, Soy, Wheat/Gluten, Fish, Shellfish, Prawn.

        
        Raw Text: "{raw_text}"
        
        
        Return ONLY valid JSON matching this schema:
        [
            {{
                "dish_name": "Original Name on Menu",
                "language_original": "Original language of the menu (e.g. Italian)",
                "price": 120,
                "currency": "{target_currency}",
                "description": "Short description",
                "translated_name": "Name in {target_language}",
                "course_type": "Main Course",
                "enrichment": {{
                    "cuisine": "Italian/Indian/etc",
                    "region": "North Indian",
                    "spice_level": "High/Medium/Low",
                    "is_veg": true,
                    "calories_approx": 350,
                    "allergens": ["Milk", "Gluten", "Nuts", "Prawn"],
                    "ingredients": ["Paneer", "Tomato", "Butter", "Spices"]
                }}
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Cleaning logic to ensure JSON is valid
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            # Fallback if AI fails
            return [{"error": f"AI Parsing failed: {str(e)}"}]