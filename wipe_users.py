# wipe_users.py
import os
import sys
from pymongo import MongoClient

# Add the parent directory to the Python path
# This allows importing modules from the 'database' directory and 'config.py'
script_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    sys.path.insert(0, script_dir)  # Also add current script dir explicitly

from config import Config  # Import your Config class


# Assuming your User model/collection is accessed through a specific collection object
# If your models.py creates a direct 'users_collection' object, you might import that.
# Otherwise, we'll access it via the client.
# For simplicity, we'll access it via the client directly in this script.

def wipe_all_user_data():
    """
    Connects to the MongoDB database using settings from config.py
    and deletes all records from the 'users' collection.
    """
    client = None
    try:
        # Use MONGO_URI from Config for connection
        mongo_uri = Config.MONGO_URI
        db_name = Config.DB_NAME  # Use DB_NAME from Config

        client = MongoClient(mongo_uri)
        print(f"MongoDB client connected to {mongo_uri}.")

        db = client[db_name]

        # --- IMPORTANT: CONFIRM YOUR USERS COLLECTION NAME ---
        # Based on typical setups, it's often 'users' or 'User' (lowercase).
        # If your User model in database/models.py uses a different collection name,
        # you MUST change 'users' here to match it.
        collection_name = "users"  # <--- VERY LIKELY 'users', but double-check your models.py
        #      or where the User model is defined/used with MongoDB

        users_collection = db[collection_name]

        # Delete all documents in the collection
        result = users_collection.delete_many({})
        print(
            f"Successfully deleted {result.deleted_count} user records from collection '{collection_name}' in database '{db_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if client:
            client.close()
            print("MongoDB client connection closed.")


if __name__ == "__main__":
    print("WARNING: This script will delete ALL user data from the MongoDB database!")
    confirm = input("Type 'yes' to confirm deletion: ")
    if confirm.lower() == 'yes':
        wipe_all_user_data()
    else:
        print("Deletion cancelled.")