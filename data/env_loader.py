import os

from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Load constants from environment
MAX_NUMBER_OF_PROJECT = int(os.getenv('MAX_NUMBER_OF_PROJECT', 1000))
MAX_NUMBER_OF_TASK = int(os.getenv('MAX_NUMBER_OF_TASK', 10000))
