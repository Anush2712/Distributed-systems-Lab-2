# seed.py
from pymongo import MongoClient
from datetime import datetime

def seed_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['consistency_demo']

    # Drop collections if they exist
    db.UserProfile.drop()
    db.ConsistencyTest.drop()

    # Sample User Profiles
    users = [
        {"username": "Alice", "email": "alice@example.com", "last_login": datetime(2025, 10, 20)},
        {"username": "Bob", "email": "bob@example.com", "last_login": datetime(2025, 10, 21)},
        {"username": "Charlie", "email": "charlie@example.com", "last_login": datetime(2025, 10, 22)}
    ]

    db.UserProfile.insert_many(users)
    print("Seed data inserted successfully!")

if __name__ == "__main__":
    seed_data()
