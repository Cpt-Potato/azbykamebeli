import os
from pathlib import Path

import sqlalchemy
from dotenv import load_dotenv
from databases import Database

dotenv_path = Path(__file__).resolve()
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

metadata = sqlalchemy.MetaData()
database = Database("DATABASE_URL")
