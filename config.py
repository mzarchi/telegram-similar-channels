# Using dotenv to use environment variables
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
env = os.environ

API_ID = env["API_ID"]
API_HASH = env["API_HASH"]
SESSION_FILE_NAME = 'telegram'
