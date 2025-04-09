import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    AWS_REGION = os.environ.get("AWS_REGION", "your-aws-region")  # Default region if not in .env
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

settings = Settings()