import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
BOT_TOKEN = os.environ["BOT_TOKEN"]
DATA_BASE = os.environ["DATA_BASE"]
