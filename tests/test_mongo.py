import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")

if not uri:
    print("❌ Error: MONGO_URI not found in environment variables.")
    exit(1)

try:
    client = MongoClient(uri)
    client.admin.command('ping')
    print("✅ Success: Successfully connected to MongoDB Atlas!")
    
    dbs = client.list_database_names()
    print(f"📂 Available databases in cluster: {dbs}")

except Exception as e:
    print(f"❌ Connection failed: {e}")