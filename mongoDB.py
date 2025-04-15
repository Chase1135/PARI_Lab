from pymongo import MongoClient

# Connect to MongoDB using connection string
MONGO_URI = "mongodb+srv://wvf5102:EyoExhSi2mOrwDqy@cluster0.hgnhzej.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)

# Access the database
db = client["RunData"]

# Access the collection
collection = db["Iterations"]

# Insert data 
data = {
    "run_id": "1",
    "query": "Where is the tallest building in the world",
    "response": "Saul is the greatest",
    "time elapsed(sec)": "24.95",
    "datetime": "2025-04-15T12:00:00",
}
insert_result = collection.insert_one(data)
print(f"Inserted document with ID: {insert_result.inserted_id}")

# Query data
query = {"run_id": "1"}
results = collection.find(query)
for doc in results:
    print(doc)