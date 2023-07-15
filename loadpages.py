import os
import json
from pymongo import MongoClient

# Establish a connection to the MongoDB instance
client = MongoClient('mongodb://admin:password@localhost:27017')

# Access (or create, if it doesn't exist) the database 'testdb'
db = client['tutorial']

# Access (or create, if it doesn't exist) the collection 'pages'
pages = db['pages']

# Directory where the JSON files are stored
dir_path = './user_data'

# Iterate over each file in the directory
for filename in os.listdir(dir_path):
    # Only process JSON files
    if filename.endswith('.json'):
        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'r') as f:
            file_data = json.load(f)
            
            # Ensure the file data matches the 'Page' structure
            if all(key in file_data for key in ('pageId', 'title', 'body', 'comments', 'labels', 'editors', 'fuzzy', 'url')):
                # Insert the data into the 'pages' collection
                pages.insert_one(file_data)
            else:
                print(f"File {filename} is missing some fields. Skipping...")
            print(f"File {filename} has been loaded")

print("All JSON files have been processed.")


