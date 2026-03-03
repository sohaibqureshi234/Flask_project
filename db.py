from pymongo import MongoClient

# Replace <password> with your MongoDB Atlas password
MONGO_URI = "mongodb+srv://sohaibqureshi1997_db_user:YcRHSwcl61SoAF1D@flask-learning.cuxuiwf.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Create or use database
db = client["flask_tasks_db"]

# Create or use collection
tasks_collection = db["tasks"]
users_collection = db.users
