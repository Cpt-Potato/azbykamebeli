import os
from pathlib import Path

import sqlalchemy
from dotenv import load_dotenv
from databases import Database

dotenv_path = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path / ".env.dev")

DATABASE_URL = os.getenv("DATABASE_URL")

metadata = sqlalchemy.MetaData()
database = Database(DATABASE_URL)
