
import os
import time
from pathlib import Path
from io import BytesIO

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

from google import genai
from google.genai import types


# Load environment variables
load_dotenv(Path(__file__).with_name(".env"), override=False)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
GEMINI_FALLBACK_MODELS = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite"
]

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}


# Create FastAPI application
app = FastAPI(
    title="Food Verse AI",
    description="AI-powered Food Intelligence Platform",
    version="1.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://food-verse-ai-orpin.vercel.app",
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Gemini client
def get_gemini_client():

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key is missing. Add GEMINI_API_KEY to Render Environment settings."
        )

    return genai.Client(api_key=GEMINI_API_KEY)


# Gemini retry and fallback system
def generate_with_fallback(client, contents):

    models_to_try = [GEMINI_MODEL] + GEMINI_FALLBACK_MODELS
    last_error = None

    for model_name in models_to_try:

        for attempt in range(2):

            try:
                print(
                    f"Calling Gemini model {model_name}; "
                    f"attempt {attempt + 1}/2"
                )

                response = client.models.generate_content(
                    model=model_name,
                    contents=contents
                )

                if not response.text:
                    raise HTTPException(
                        status_code=502,
                        detail="Gemini returned an empty response. Please try another image."
                    )

                return response

            except HTTPException:
                raise

            except Exception as exc:

                last_error = exc
                error_text = str(exc).lower()

                temporary_error = any(
                    marker in error_text
                    for marker in (
                        "503",
                        "unavailable",
                        "high demand",
                        "429",
                        "resource_exhausted",
                        "rate limit",
                        "too many requests"
                    )
                )

                if not temporary_error:

                    print(f"Gemini request failed: {exc}")

                    raise HTTPException(
                        status_code=502,
                        detail=f"Gemini request failed: {exc}"
                    ) from exc

                print(
                    f"Gemini model {model_name} "
                    f"temporarily unavailable: {exc}"
                )

                if attempt == 0:
                    time.sleep(2)

    print(
        f"All configured Gemini models failed. "
        f"Last error: {last_error}"
    )

    raise HTTPException(
        status_code=503,
        detail=(
            "Gemini is temporarily busy or rate-limited. "
            "Please try again in a few minutes."
        )
    )


# Validate image type
def validate_image_type(file: UploadFile):

    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG, PNG or WEBP image."
        )


# Validate uploaded image
def verify_image(image_data: bytes):

    try:
        with Image.open(BytesIO(image_data)) as image:
            image.verify()

    except (UnidentifiedImageError, OSError, ValueError) as exc:

        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image."
        ) from exc


# Shared image analysis function
async def analyze_uploaded_image(file: UploadFile, prompt: str):

    validate_image_type(file)

    image_data = await file.read()

    if not image_data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty."
        )

    verify_image(image_data)

    client = get_gemini_client()

    response = generate_with_fallback(
        client,
        contents=[
            types.Part.from_bytes(
                data=image_data,
                mime_type=file.content_type
            ),
            prompt
        ]
    )

    return {
        "status": "success",
        "result": response.text
    }


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


# Image upload API
@app.post("/api/upload-image")
async def upload_food_image(file: UploadFile = File(...)):

    validate_image_type(file)

    image_data = await file.read()

    if not image_data:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty."
        )

    verify_image(image_data)

    with Image.open(BytesIO(image_data)) as image:

        return {
            "status": "success",
            "filename": file.filename,
            "image_format": image.format,
            "width": image.width,
            "height": image.height,
            "message": "Food image uploaded successfully!"
        }


# 1. Food Recognition API
@app.post("/api/recognize-food")
async def recognize_food(file: UploadFile = File(...)):

    prompt = """
    You are a food recognition assistant.

    Examine this image and identify the food or dish.

    Give your answer in this format:

    Food Name:
    Description:
    Main Ingredients:

    If the image does not contain food, clearly say so.
    Do not invent ingredients that cannot be identified.
    """

    return await analyze_uploaded_image(file, prompt)


# 2. Nutrition Analysis API
@app.post("/api/nutrition-analysis")
async def nutrition_analysis(file: UploadFile = File(...)):

    prompt = """
    You are a professional nutrition analysis assistant.

    Analyze the food shown in this image.

    Provide:

    Food Name:
    Estimated Serving Size:
    Estimated Calories (kcal):
    Protein (g):
    Carbohydrates (g):
    Fat (g):
    Fiber (g):
    Health Benefits:
    Dietary Suggestions:

    Give approximate nutritional values only.

    Clearly state that values are estimates based on
    visible food and assumed serving size.

    Do not claim exact nutritional measurements.

    If the image does not contain food, say so.
    """

    return await analyze_uploaded_image(file, prompt)


# 3. Freshness Detection API
@app.post("/api/freshness-detection")
async def freshness_detection(file: UploadFile = File(...)):

    prompt = """
    You are a food freshness analysis assistant.

    Examine the food shown in this image.

    Provide:

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

    Base your assessment only on visible signs.

    Do not claim that food is safe to eat based only
    on an image.

    Mention that smell, texture, storage history and
    expiry information may be needed for a reliable assessment.

    If the image does not contain food, clearly say so.
    """

    return await analyze_uploaded_image(file, prompt)


# 4. Smart Cooking API
@app.post("/api/smart-cooking")
async def smart_cooking(file: UploadFile = File(...)):

    prompt = """
    You are a Smart Cooking Assistant.

    Examine the food image and suggest a suitable recipe.

    Provide:

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

    return await analyze_uploaded_image(file, prompt)


# 5. Hygiene Monitoring API
@app.post("/api/hygiene-monitoring")
async def hygiene_monitoring(file: UploadFile = File(...)):

    prompt = """
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

    return await analyze_uploaded_image(file, prompt)


# Meal Planner request model
class MealPlanRequest(BaseModel):

    dietary_preference: str
    health_goal: str
    days: int


# 6. Meal Planner API
@app.post("/api/meal-planner")
async def meal_planner(request: MealPlanRequest):

    if request.days < 1 or request.days > 7:

        raise HTTPException(
            status_code=400,
            detail="Please select between 1 and 7 days."
        )

    client = get_gemini_client()

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
