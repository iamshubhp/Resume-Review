import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()


def test_connection():
    try:
        # Get MongoDB URI from environment variable
        mongodb_uri = os.getenv("MONGODB_URI")

        # Create a client and connect to the server
        client = MongoClient(mongodb_uri)

        # Send a ping to confirm connection
        client.admin.command('ping')

        print("✅ Connected to MongoDB successfully!")

        # List available databases (optional)
        print("\nAvailable databases:")
        database_names = client.list_database_names()
        for db in database_names:
            print(f"- {db}")

        # Create a test entry (optional)
        db = client["resume_review_db"]
        test_collection = db["test_collection"]

        result = test_collection.insert_one(
            {"test": "connection", "status": "successful"})
        print(f"\n✅ Test document inserted with ID: {result.inserted_id}")

        # Clean up test entry
        test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")

    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        return False

    return True


if __name__ == "__main__":
    test_connection()
