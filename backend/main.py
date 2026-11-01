
import os
from pathlib import Path
from io import BytesIO

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from google import genai
from google.genai import types


# Load environment variables from backend/.env
load_dotenv(Path(__file__).with_name(".env"), override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Create FastAPI application
app = FastAPI(
    title="Food Verse AI",
    description="AI-powered Food Intelligence Platform",
    version="1.0"
)


# Allow React frontend to communicate with Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://food-verse-ai-orpin.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Home route
@app.get("/")
def home():
    return {
        "message": "Welcome to Food Verse AI Backend!"
    }


# Health check API
@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "Food Verse AI backend is running!"
    }


# Food image upload API
@app.post("/api/upload-image")
async def upload_food_image(file: UploadFile = File(...)):

    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]:
        return {
            "status": "error",
            "message": "Please upload a JPG, PNG or WEBP image."
        }

    try:
        image_data = await file.read()
        image = Image.open(BytesIO(image_data))

        return {
            "status": "success",
            "filename": file.filename,
            "image_format": image.format,
            "width": image.width,
            "height": image.height,
            "message": "Food image uploaded successfully!"
        }

    except Exception:
        return {
            "status": "error",
            "message": "Unable to process this image."
        }


# AI Food Recognition API using Gemini
@app.post("/api/recognize-food")
async def recognize_food(file: UploadFile = File(...)):

    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]:
        return {
            "status": "error",
            "message": "Please upload a JPG, PNG or WEBP image."
        }

    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "Gemini API key is missing. Check your backend .env file."
        }

    try:
        image_data = await file.read()

        # Check that the uploaded file is a valid image
        Image.open(BytesIO(image_data)).verify()

        # Connect to Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Send the image and recognition instructions
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=file.content_type
                ),
                """
                You are a food recognition assistant.

                Examine this image and identify the food or dish.

                Give your answer in this format:

                Food Name: [name of the food]
                Description: [short description]
                Main Ingredients: [main ingredients]

                If the image does not contain food, clearly say so.
                Do not invent ingredients that cannot be identified.
                """
            ]
        )

        return {
            "status": "success",
            "result": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
# AI Nutrition Analysis API using Gemini
@app.post("/api/nutrition-analysis")
async def nutrition_analysis(file: UploadFile = File(...)):

    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]:
        return {
            "status": "error",
            "message": "Please upload a JPG, PNG or WEBP image."
        }

    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "Gemini API key is missing."
        }

    try:
        image_data = await file.read()

        # Check whether the uploaded file is a valid image
        Image.open(BytesIO(image_data)).verify()

        # Connect to Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Analyze nutritional information
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=file.content_type
                ),
                """
                You are a professional nutrition analysis assistant.

                Analyze the food shown in this image.

                Provide the following information:

                Food Name:
                Estimated Serving Size:
                Estimated Calories (kcal):
                Protein (g):
                Carbohydrates (g):
                Fat (g):
                Fiber (g):
                Health Benefits:
                Dietary Suggestions:

                Important:
                - Give approximate nutritional values.
                - Clearly mention that values are estimates based on
                  the visible food and assumed serving size.
                - Do not claim exact nutritional measurements.
                - If the image does not contain food, say so.
                """
            ]
        )

        return {
            "status": "success",
            "result": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        # AI Food Freshness Detection API using Gemini
@app.post("/api/freshness-detection")
async def freshness_detection(file: UploadFile = File(...)):

    if file.content_type not in [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]:
        return {
            "status": "error",
            "message": "Please upload a JPG, PNG or WEBP image."
        }

    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "Gemini API key is missing."
        }

    try:
        image_data = await file.read()

        # Check whether the uploaded file is a valid image
        Image.open(BytesIO(image_data)).verify()

        # Connect to Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Analyze food freshness
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=file.content_type
                ),
                """
                You are a food freshness analysis assistant.

                Examine the food shown in this image.

                Provide your answer in this format:

                Food Name:
                Visible Condition:
                Freshness Assessment:
                Possible Signs of Spoilage:
                Storage Recommendations:
                Safety Advice:

                Classify the visible condition as:
                - Appears Fresh
                - Possibly Stale
                - Possible Spoilage

                Important:
                - Base your assessment only on visible signs.
                - Do not claim that food is safe to eat based only on an image.
                - Mention that smell, texture, storage history and expiry
                  information may be needed for a reliable assessment.
                - If the image does not contain food, clearly say so.
                """
            ]
        )

        return {
            "status": "success",
            "result": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        
# Smart Cooking using Gemini AI

@app.post("/api/smart-cooking")
async def smart_cooking(file: UploadFile = File(...)):

    # Check image format
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        return {
            "status": "error",
            "message": "Please upload a JPG, PNG, or WEBP image."
        }

    # Check API key
    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "Gemini API key is missing."
        }

    try:
        # Read uploaded image
        image_data = await file.read()

        # Validate image
        Image.open(BytesIO(image_data)).verify()

        # Connect to Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Generate cooking recipe
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type=file.content_type
                ),
                """
                You are a Smart Cooking Assistant.

                Examine the food image and suggest a suitable recipe.

                Provide the following:

                Recipe Name:
                Ingredients:
                Required Quantity:
                Preparation Time:
                Cooking Time:
                Step-by-Step Cooking Instructions:
                Cooking Tips:
                Serving Suggestions:

                If the image is not food, clearly say so.
                If the food cannot be identified confidently,
                mention that the recipe is only a suggestion.
                """
            ]
        )

        return {
            "status": "success",
            "result": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Hygiene Monitoring using Gemini AI

@app.post("/api/hygiene-monitoring")
async def hygiene_monitoring(file: UploadFile = File(...)):

    # Check image format
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        return {
            "status": "error",
            "message": "Please upload a JPG, PNG, or WEBP image."
        }

    if not GEMINI_API_KEY:
        return {
            "status": "error",
            "message": "Gemini API key is missing."
        }

    try:
        # Read uploaded image
        image_data = await file.read()

        # Validate image
        Image.open(BytesIO(image_data)).verify()

        # Connect to Gemini
        client = genai.Client(api_key=GEMINI_API_KEY)

        # Analyze visible hygiene conditions
        response = client.models.generate_content(
            model="gemini-3.8-flash",
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

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return {
            "status": "success",
            "result": response.text
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
