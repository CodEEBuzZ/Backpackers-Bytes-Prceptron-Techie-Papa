class DishRecommender:

    def recommend(self, menu_data, preferences):
        """
        Filters dishes based on:
        1. Dietary Type (Veg/Non-Veg/Mix)
        2. Budget
        3. Spice Tolerance
        4. Course Preference (Starter/Main/Dessert)
        """
        best_dish = None
        best_score = -100
        explanation = ""

        # Basic error check
        if not menu_data or "error" in menu_data[0]:
            return None, "Error in menu data processing."

        for dish in menu_data:

            dish.setdefault("language_original", "Unknown")
            score = 0
            reasons = []

            price = dish.get('price')
            price = float(price) if isinstance(price, (int, float, str)) and str(price).strip() != "" else 0

            course_type = dish.get('course_type', 'Main Course')

            enrichment = dish.get('enrichment', {})

            
            is_veg = enrichment.get('is_veg', False)
            spice_level = enrichment.get('spice_level', 'Medium')

            # Health-based preference (soft scoring)
            health_goal = preferences.get("health_goal", "No Preference")
            calories = enrichment.get("calories_approx", 0)
            ingredients = enrichment.get("ingredients", [])

            if health_goal == "Low Calorie 🥗":
                if isinstance(calories, (int, float)) and calories <= 350:
                    score += 15
                    reasons.append("Low in calories.")
                else:
                    score -= 5

            elif health_goal == "High Protein 💪":
                protein_keywords = ["chicken", "egg", "paneer", "tofu", "fish", "lentil", "dal"]
                if any(p in " ".join(ingredients).lower() for p in protein_keywords):
                    score += 15
                    reasons.append("High protein content.")

            elif health_goal == "Light & Easy to Digest 🧘":
                if spice_level == "Low":
                    score += 10
                    reasons.append("Light and easy to digest.")
                if isinstance(calories, (int, float)) and calories <= 400:
                    score += 5

            elif health_goal == "Low Spice 🌶️":
                if spice_level == "Low":
                    score += 15
                    reasons.append("Low spice as preferred.")
                elif spice_level == "High":
                    score -= 15


            dish_cuisine = enrichment.get("cuisine", "").lower()
            preferred_cuisines = [c.lower() for c in preferences.get("preferred_cuisines", [])]

            if preferred_cuisines:
                if any(cuisine in dish_cuisine for cuisine in preferred_cuisines):
                    score += 15
                    reasons.append("Matches your preferred cuisine.")
                else:
                    score -= 5

            eating_style = preferences.get("eating_style", "Balanced ⚖️ (Both)")

            if eating_style.startswith("Familiar"):
                if any(cuisine in dish_cuisine for cuisine in preferred_cuisines):
                    score += 10
                    reasons.append("Familiar taste for you.")
                else:
                    score -= 10

            elif eating_style.startswith("Experimental"):
                if not any(cuisine in dish_cuisine for cuisine in preferred_cuisines):
                    score += 10
                    reasons.append("Something new to explore!")



            user_diet = preferences['dietary_type']

            if "Vegetarian Only" in user_diet and not is_veg:
                continue
            if "Non-Vegetarian Only" in user_diet and is_veg:
                continue

            user_budget = preferences['budget']
            if price <= user_budget:
                score += 10
                reasons.append("Fits your budget.")
            else:
                score -= 20

            user_course = preferences['course_preference']

            if "Full Meal" in user_course:
                score += 5
            elif "Main Course" in user_course and course_type == "Main Course":
                score += 15
                reasons.append("It is a Main Course.")
            elif "Starter" in user_course and course_type == "Starter":
                score += 15
                reasons.append("It is a Starter.")
            elif "Dessert" in user_course and course_type == "Dessert":
                score += 15
                reasons.append("It is a Dessert.")
            elif user_course != "Surprise Me (Any)":
                score -= 10

            user_spice = preferences['spice_tolerance']
            if user_spice == spice_level:
                score += 5
                reasons.append(f"Perfect {user_spice} spice.")
            elif user_spice == "Low" and spice_level == "High":
                score -= 50

            if score > best_score:
                best_score = score
                best_dish = dish

                explanation = reasons.copy() if reasons else ["Matches your overall preferences."]

                region = enrichment.get("region")
                if region:
                    explanation.append(f"Belongs to the {region} cuisine.")

                if "Vegetarian" in user_diet:
                    explanation.append("Follows your vegetarian preference.")

                if preferred_cuisines:
                    explanation.append("Aligns with cuisines you usually enjoy.")

                if eating_style.startswith("Experimental"):
                    explanation.append("Encourages you to try something new.")

                ingredients = enrichment.get("ingredients", [])
                if ingredients:
                    explanation.append(
                        f"Key ingredients include {', '.join(ingredients[:3])}."
                    )


        return best_dish, explanation

    # MUST BE INSIDE THE CLASS
    def recommend_course_wise(self, menu_data, preferences):
        """
        Recommend the best dish for each selected course
        (Starter, Main Course, Dessert, Beverage).
        """
        selected_courses = preferences.get("multi_course_selection", [])
        results = {}

        for course in selected_courses:
            course_dishes = [
                dish for dish in menu_data
                if dish.get("course_type") == course
            ]

            if not course_dishes:
                continue

            best_dish, reason = self.recommend(course_dishes, preferences)
            if best_dish:
                results[course] = {
                    "dish": best_dish,
                    "reason": reason
                }

        return results
