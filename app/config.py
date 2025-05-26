import os
from dotenv import load_dotenv

load_dotenv()

# DB_MODE = os.getenv("DB_MODE", "sqlite")
# SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "data/popviz.db")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

APP_NAME = "POPViz"
