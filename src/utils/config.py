"""Configuration management for the Mental Health Support Companion"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Application Settings
APP_NAME = os.getenv("APP_NAME", "Mental Health Support Companion")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# User Settings
DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "UTC")
DEFAULT_CHECKIN_TIMES = os.getenv("DEFAULT_CHECKIN_TIMES", "09:00,21:00").split(",")

# Database Configuration
DATABASE_PATH = PROJECT_ROOT / os.getenv("DATABASE_PATH", "data/mental_health.db")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / os.getenv("LOG_FILE", "logs/app.log")

# Model Configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"
TEMPERATURE = 0.7
MAX_OUTPUT_TOKENS = 2048

# Crisis Resources
CRISIS_RESOURCES = {
    "US": {
        "name": "National Suicide Prevention Lifeline",
        "phone": "988",
        "text": "Text HOME to 741741",
        "url": "https://988lifeline.org"
    },
    "International": {
        "name": "Find A Helpline",
        "url": "https://findahelpline.com"
    }
}

# Mood Scale
MOOD_SCALE = {
    1: "Very Bad",
    2: "Bad",
    3: "Poor",
    4: "Below Average",
    5: "Neutral",
    6: "Slightly Good",
    7: "Good",
    8: "Very Good",
    9: "Great",
    10: "Excellent"
}

# System Instruction for Gemini
SYSTEM_INSTRUCTION = """You are a compassionate mental health support companion AI.

Your role is to:
- Provide empathetic, non-judgmental support
- Listen actively and validate emotions
- Suggest evidence-based coping strategies when appropriate
- Encourage healthy behaviors and self-care
- Detect crisis situations and provide immediate resources

Important guidelines:
- NEVER diagnose mental health conditions
- NEVER prescribe medication or treatments
- ALWAYS encourage professional help when needed
- Maintain confidentiality and respect privacy
- Be culturally sensitive and inclusive
- Recognize your limitations as an AI assistant

Your tone should be:
- Warm and supportive
- Professional yet approachable
- Hopeful and encouraging
- Patient and understanding"""