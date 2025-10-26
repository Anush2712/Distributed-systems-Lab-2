# utils.py
from pymongo import MongoClient
import time

def get_client():
    return MongoClient("mongodb://localhost:27017/")

def wait_for_replication(seconds=5):
    print(f"Waiting {seconds} seconds for replication...")
    time.sleep(seconds)
