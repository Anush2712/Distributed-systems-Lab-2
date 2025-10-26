# eventual_consistency_demo.py
from utils import get_client, wait_for_replication
import time

def eventual_consistency_demo():
    client = get_client()
    db = client["consistency_demo"]
    collection = db["ConsistencyTest"]

    doc = {"test": "eventual_consistency", "timestamp": 0}
    collection.insert_one(doc)
    print("Inserted document, checking secondary replication...")

    # Check repeatedly for propagation (simulate eventual consistency)
    for i in range(5):
        time.sleep(1)
        doc_check = collection.find_one({"test": "eventual_consistency"})
        print(f"Check {i+1}: {doc_check}")

if __name__ == "__main__":
    eventual_consistency_demo()
