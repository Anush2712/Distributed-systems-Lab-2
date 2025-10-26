# failover_demo.py
from pymongo import MongoClient
from utils import wait_for_replication

def failover_demo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["consistency_demo"]
    collection = db["ConsistencyTest"]

    print("Simulate failover: Insert before primary failure")
    collection.insert_one({"failover_test": "before_failure"})
    wait_for_replication(2)

    print("Simulate stopping primary node manually (check Docker)")

    collection.insert_one({"failover_test": "after_failure"})
    result = collection.find()
    print("Documents after failover simulation:")
    for doc in result:
        print(doc)

if __name__ == "__main__":
    failover_demo()
