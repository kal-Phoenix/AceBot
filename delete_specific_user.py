# delete_specific_user.py
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


def delete_specific_user_data(user_id_to_delete: int) -> bool:
    """
    Connects to the MongoDB database using settings from config.py
    and deletes the record for a specific user by their Telegram User ID.
    Returns True if a user was deleted, False otherwise.
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

        # Delete one document based on the '_id' field, which is the user_id
        result = users_collection.delete_one({"_id": user_id_to_delete})

        if result.deleted_count > 0:
            print(f"Successfully deleted data for user ID: {user_id_to_delete}.")
            return True
        else:
            print(f"User with ID: {user_id_to_delete} not found in the database. No data deleted.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if client:
            client.close()
            print("MongoDB client connection closed.")


if __name__ == "__main__":
    print("WARNING: This script will delete data for a SPECIFIC user from the MongoDB database!")

    user_id_input = input("Enter the Telegram User ID of the user to delete: ")

    try:
        user_id = int(user_id_input)
    except ValueError:
        print("Invalid input. Please enter a numerical Telegram User ID.")
        sys.exit(1)

    confirm = input(f"Type 'yes' to confirm deletion of data for user ID {user_id}: ")
    if confirm.lower() == 'yes':
        delete_specific_user_data(user_id)
    else:
        print("Deletion cancelled.")