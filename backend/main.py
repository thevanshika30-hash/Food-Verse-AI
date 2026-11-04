        response = generate_with_fallback(
            client,
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=file.content_type
                ),
                """
                You are a Food Hygiene Monitoring Assistant.

                Examine the uploaded image and provide:

                Food or Surface Identified:
                Visible Cleanliness:
                Visible Hygiene Concerns:
                Possible Contamination Indicators:
                Recommended Hygiene Improvements:
                Safe Food Handling Suggestions:

                Only report what can be observed in the image.
                Do not claim that food is contaminated or safe
                based only on its appearance.
                Mention that invisible microorganisms cannot
                be detected from an image.
                If the image is not related to food or food
                handling, clearly mention that.
                """
            ]
        )

        return {
            "status": "success",
            "result": response.text
        }

    except HTTPException:
        raise
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Meal Planner using Gemini AI

from pydantic import BaseModel

class MealPlanRequest(BaseModel):
    dietary_preference: str
    health_goal: str
    days: int

@app.post("/api/meal-planner")
async def meal_planner(request: MealPlanRequest):

    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "Gemini API key is missing."
        }

    if request.days < 1 or request.days > 7:
        return {
            "status": "error",
            "message": "Please select between 1 and 7 days."
        }

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        You are a professional meal planning assistant.

        Create a {request.days}-day meal plan.

        Dietary Preference: {request.dietary_preference}
        Health Goal: {request.health_goal}

        For each day, provide:
        1. Breakfast
        2. Morning Snack
        3. Lunch
        4. Evening Snack
        5. Dinner

        Also include:
        - Food names
        - Short descriptions
        - Approximate calories per meal
        - Daily calorie estimate
        - Simple nutrition tips

        Make the meals practical and use commonly
        available ingredients.

        Mention that calorie estimates are approximate
        and individual nutritional needs vary.
        Do not present the plan as medical advice.
        """

        response = generate_with_fallback(
            client,
            contents=prompt
        )

        return {
            "status": "success",
            "result": response.text
        }

    except HTTPException:
        raise
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

