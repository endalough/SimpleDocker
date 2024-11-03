from fastapi import FastAPI
from sqlalchemy import create_engine, text
import redis
import os

app = FastAPI()

# PostgreSQL setup
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_name = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"
engine = create_engine(DATABASE_URL)

# redis setup
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT", 6379))
cache = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.get("/")
async def root():
    # check redis cache for value
    cached_value = cache.get("hello")
    if cached_value:
        return {"message": f"Cached: {cached_value.encode()}"}
    
    # if not cached, then query db
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello, Database'")).fetchone()
        message = result[0]
        cache.set("hello", message) # caching the result
        return {"message": f"Fetched from the db: {message}"}