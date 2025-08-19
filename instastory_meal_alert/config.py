import os
from dotenv import load_dotenv

load_dotenv()

# NEIS API
NEIS_API_KEY = os.getenv("NEIS_API_KEY")
OFFICE_CODE = "D10"
SCHOOL_CODE = "7240454"

# Instagram
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Image
BACKGROUND_IMAGE_PATH = "assets/background.png"
MEAL_STORY_IMAGE_PATH = "meal_story.png"
FONT_BOLD_PATH = "assets/font/Pretendard-Bold.ttf"
FONT_REGULAR_PATH = "assets/font/Pretendard-Regular.ttf"
