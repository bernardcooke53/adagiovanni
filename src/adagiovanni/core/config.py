import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

API_V1_PREFIX = "/api/v1"
SANDWICH_PREP_TIME_SECS = int(60 * 2.5)  # 2.5 minutes
SANDWICH_SERVICE_TIME_SECS = 60  # 1 minute

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME", __package__)
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "password")
MONGO_DB = os.getenv("MONGO_DB", "adagiovanni")

MONGO_URL = f"mongodb://{quote_plus(MONGO_USER)}:{quote_plus(MONGO_PASSWORD)}@{MONGO_HOST}:{MONGO_PORT}"

MIN_MONGO_CONNECTION_POOL_SIZE = int(os.getenv("MIN_MONGO_CONNECTION_POOL_SIZE", 10))
MAX_MONGO_CONNECTION_POOL_SIZE = int(os.getenv("MAX_MONGO_CONNECTION_POOL_SIZE", 10))
MAX_DOCUMENT_FETCH_LIMIT = int(os.getenv("MAX_DOCUMENT_FETCH_LIMIT", 1000))
# SANDWICH_COLLECTION_NAME = "sandwiches"
ORDERS_COLLECTION_NAME = "orders"
