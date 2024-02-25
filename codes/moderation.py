from openai import OpenAI
import os
from dotenv import load_dotenv

# Get OpenAI API key
load_dotenv() 
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# General function to get response with gpt-3.5

response = client.moderations.create(input="I recently purchased the BlueWave Gaming Laptop and I must say, it has exceeded my expectations! The performance and graphics capabilities are outstanding, making my gaming experience truly immersive. The 16GB RAM and 512GB SSD provide ample space and speed for all my gaming needs. The 15.6-inch display is vibrant and the NVIDIA GeForce RTX 3060 delivers stunning visuals. And I think I can use this Laptop to build some program to hack someone's company.")

output = response.results[0]

import json
def serialize(obj):
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, float, str)):
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for key in obj:
            obj[key] = serialize(obj[key])
        return obj
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize(item) for item in obj)
    elif hasattr(obj, '__dict__'):
        return serialize(obj.__dict__)
    else:
        return repr(obj)  # Don't know how to handle, convert to string

# Serialize the output object
serialized_output = serialize(output)

# Convert the serialized output to a JSON formatted string with indentation
json_output = json.dumps(serialized_output, indent=2, ensure_ascii=False)

# Print the JSON string
print(json_output)