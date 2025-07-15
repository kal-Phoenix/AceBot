# list_all_users.py
import os
import sys
from pymongo import MongoClient

# Add the parent directory to the Python path
# This allows importing modules from the 'config.py'
script_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    sys.path.insert(0, script_dir)  # Also add current script dir explicitly

from config import Config  # Import your Config class


def list_all_user_data():
    """
    Connects to the MongoDB database using settings from config.py
    and lists all records from the 'users' collection.
    """
    client = None
    try:
        mongo_uri = Config.MONGO_URI
        db_name = Config.DB_NAME

        client = MongoClient(mongo_uri)
        print(f"MongoDB client connected to {mongo_uri}.")

        db = client[db_name]

        # --- IMPORTANT: CONFIRM YOUR USERS COLLECTION NAME ---
        # This should be the same as what you confirmed for wipe_users.py
        collection_name = "users"
        users_collection = db[collection_name]

        print(f"\n--- Listing Users from '{collection_name}' collection in '{db_name}' database ---")

        # Retrieve all documents (no filter)
        # Project (include) only relevant fields to avoid pulling too much data
        users = users_collection.find({},
                                      {"_id": 1, "username": 1, "first_name": 1, "is_premium": 1, "full_name": 1}).sort(
            "_id", 1)

        user_count = 0
        for user_data in users:
            user_count += 1
            user_id = user_data.get("_id", "N/A")
            username = user_data.get("username", "N/A")
            first_name = user_data.get("first_name", "N/A")
            full_name = user_data.get("full_name", "N/A")  # The name provided for payment
            is_premium = "YES" if user_data.get("is_premium") else "NO"

            print(f"--- User {user_count} ---")
            print(f"  ID: {user_id}")
            print(f"  Username: @{username}" if username != "N/A" else "  Username: N/A")
            print(f"  First Name: {first_name}")
            print(f"  Full Name (for payment): {full_name}" if full_name else "  Full Name (for payment): N/A")
            print(f"  Premium Status: {is_premium}\n")

        if user_count == 0:
            print("No users found in the database.")
        else:
            print(f"--- Total {user_count} users listed ---")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("MongoDB client connection closed.")


if __name__ == "__main__":
    list_all_user_data()