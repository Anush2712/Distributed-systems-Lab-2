# strong_consistency_demo.py
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern
from utils import get_client, wait_for_replication

def strong_consistency_demo():
    client = get_client()
    db = client.get_database("consistency_demo", write_concern=WriteConcern("majority"))
    collection = db.get_collection("ConsistencyTest", read_concern=ReadConcern("majority"))

    doc = {"test": "strong_consistency", "timestamp": 0}
    collection.insert_one(doc)
    wait_for_replication(2)

    result = collection.find_one({"test": "strong_consistency"})
    print("Strong Consistency Demo Result:", result)

if __name__ == "__main__":
    strong_consistency_demo()
