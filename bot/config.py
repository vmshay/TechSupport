import os
from dotenv import load_dotenv


load_dotenv()
env_path = '.env'
load_dotenv(dotenv_path=env_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
CHAT_ID = os.getenv('CHAT_ID')
ADMINS = os.getenv('ADMINS')
TRASH_CHAT = os.getenv('TRASH_CHAT')
