from pymongo import MongoClient, DESCENDING
import config

# Connect to MongoDB using connection string
MONGO_URI = "mongodb+srv://wvf5102:EyoExhSi2mOrwDqy@cluster0.hgnhzej.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_next_run_id(collection):
    last_run = collection.find_one(sort=[("RUN_ID", DESCENDING)])

    if last_run and "RUN_ID" in last_run:
        return int(last_run["RUN_ID"]) + 1
    
    return 1

def store_config():
    # Connect to MongoDB using connection string
    client = MongoClient(MONGO_URI)
    
    # Access the database
    db = client["RunData"]

    # Access the collection
    collection = db["Iterations"]

    run_id = get_next_run_id(collection=collection)

    # Insert data 
    config_dict = {
        "RUN_ID": run_id,
        "ENDPOINTS": config.ENDPOINTS,
        "GET_MODALITIES": config.GET_MODALITIES,
        "NCHANNELS": config.NCHANNELS,
        "SAMPWIDTH": config.SAMPWIDTH,
        "FRAMERATE": config.FRAMERATE,
        "VISUAL_INTERVAL": config.VISUAL_INTERVAL,
        "PHYSICAL_INTERVAL": config.PHYSICAL_INTERVAL,
        "MAX_VISUAL_HISTORY": config.MAX_VISUAL_HISTORY,
        "MAX_PHYSICAL_HISTORY": config.MAX_PHYSICAL_HISTORY,
    }

    result = collection.insert_one(config_dict)
    print(f"Inserted config with ID: {result.inserted_id}")