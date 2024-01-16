import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '../../', '.env')
load_dotenv(dotenv_path)
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")
ROOT_DIR = dotenv_path = os.path.join(os.path.dirname(__file__), '../../', '/app')
KAKAO_API_BURL = os.getenv("KAKAO_API_BURL")
ENV_IS_GITHUB = os.getenv("GITHUB_ACTIONS")
