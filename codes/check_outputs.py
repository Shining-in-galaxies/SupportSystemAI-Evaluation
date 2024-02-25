# ___________________SET UP_______________________
from openai import OpenAI
import os
from dotenv import load_dotenv

# Get OpenAI API key
load_dotenv() 
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Delimeter
delimiter = "####"

# General complete function
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.4, max_tokens=500):
    messages_payload = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
    response = client.chat.completions.create(
        model=model,
        messages=messages_payload,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if response.choices and len(response.choices) > 0:
        last_message = response.choices[-1].message
        last_message_content = last_message.content
        return last_message_content
    else:
        return "No response generated."
# ___________________End of SET UP_______________________

# _________________STEP1: Moderation Check_______________
final_response_to_customer = f"""
The SmartX ProPhone has a 6.1-inch display, 128GB storage, \
12MP dual camera, and 5G. The FotoSnap DSLR Camera \
has a 24.2MP sensor, 1080p video, 3-inch LCD, and \
interchangeable lenses. We have a variety of TVs, including \
the CineView 4K TV with a 55-inch display, 4K resolution, \
HDR, and smart TV features. We also have the SoundMax \
Home Theater system with 5.1 channel, 1000W output, wireless \
subwoofer, and Bluetooth. Do you have any specific questions \
about these products or any other products we offer?
"""

response = client.moderations.create(input = final_response_to_customer )

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
# _________________End of STEP1: Moderation Check_______________

# _________________STEP 2: factually based Check_______________
system_message = f"""
You are an assistant that evaluates whether \
customer service agent responses sufficiently \
answer customer questions, and also validates that \
all the facts the assistant cites from the product \
information are correct.
The product information and user and customer \
service agent messages will be delimited by \
3 backticks, i.e. ```.

Respond with a Y or N character, with no punctuation:
Y - if the output sufficiently answers the question \
    AND the response correctly uses product information
N - otherwise

Output a single letter only.
"""

customer_message = f"""
tell me about the smartx pro phone and \
the fotosnap camera, the dslr one. \
Also tell me about your tvs"""

product_information = """{ "name": "SmartX ProPhone", 
"category": "Smartphones and Accessories", 
"brand": "SmartX", "model_number": "SX-PP10", "warranty": 
"1 year", "rating": 4.6, 
"features": [ "6.1-inch display", "128GB storage", 
"12MP dual camera", "5G" ], 
"description": "A powerful smartphone with advanced camera 
features.", "price": 899.99 } 
{ "name": "FotoSnap DSLR Camera", "category": 
"Cameras and Camcorders", "brand": "FotoSnap", 
"model_number": "FS-DSLR200", "warranty": "1 year", 
"rating": 4.7, "features": [ "24.2MP sensor", 
"1080p video", "3-inch LCD", "Interchangeable lenses" ], 
"description": 
"Capture stunning photos and videos with this versatile 
DSLR camera.", "price": 599.99 } 
{ "name": "CineView 4K TV", "category": "Televisions and 
Home Theater Systems", 
"brand": "CineView", "model_number": "CV-4K55", "warranty": 
"2 years", "rating": 4.8, 
"features": [ "55-inch display", "4K resolution", "HDR", 
"Smart TV" ], "description": 
"A stunning 4K TV with vibrant colors and smart features.", 
"price": 599.99 } { "name": 
"SoundMax Home Theater", "category": "Televisions and Home 
Theater Systems", "brand": 
"SoundMax", "model_number": "SM-HT100", "warranty": "1 year", 
"rating": 4.4, "features": 
[ "5.1 channel", "1000W output", "Wireless subwoofer", 
"Bluetooth" ], "description": 
"A powerful home theater system for an immersive audio 
experience.", "price": 399.99 } 
{ "name": "CineView 8K TV", "category": "Televisions and 
Home Theater Systems", "brand":
 "CineView", "model_number": "CV-8K65", "warranty": 
"2 years", "rating": 4.9, "features": 
[ "65-inch display", "8K resolution", "HDR", 
"Smart TV" ], "description": 
"Experience the future of television with this 
stunning 8K TV.", "price": 2999.99 } 
{ "name": "SoundMax Soundbar", "category": 
"Televisions and Home Theater Systems", 
"brand": "SoundMax", "model_number": "SM-SB50", 
"warranty": "1 year", "rating": 4.3, 
"features": [ "2.1 channel", "300W output", 
"Wireless subwoofer", "Bluetooth" ], 
"description": "Upgrade your TV's audio with this sleek 
and powerful soundbar.", 
"price": 199.99 } { "name": "CineView OLED TV", "category": 
"Televisions and Home Theater Systems", "brand": "CineView", 
"model_number": "CV-OLED55", "warranty": "2 years", 
"rating": 4.7, 
"features": [ "55-inch display", "4K resolution", 
"HDR", "Smart TV" ], 
"description": "Experience true blacks and vibrant 
colors with this OLED TV.", 
"price": 1499.99 }"""

q_a_pair = f"""
Customer message: ```{customer_message}```
Product information: ```{product_information}```
Agent response: ```{final_response_to_customer}```

Does the response use the retrieved information correctly?
Does the response sufficiently answer the question

Output Y or N
"""
# _________________End of STEP 2: factually based Check_______________

# ______________TEST 1____________________
messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': q_a_pair}
]

# Response from chatGPT
response = get_completion_from_messages(messages, max_tokens=1)
print(response)
# ______________end of TEST 1____________________

# ______________TEST 2____________________
another_response = "life is like a box of chocolates"

q_a_pair = f"""
Customer message: ```{customer_message}```
Product information: ```{product_information}```
Agent response: ```{another_response}```

Does the response use the retrieved information correctly?
Does the response sufficiently answer the question?

Output Y or N
"""
# Message to be sent to chatGPT
messages = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': q_a_pair}
]

# Response from chatGPT
response = get_completion_from_messages(messages)
print(response)
# ______________end of TEST 2____________________