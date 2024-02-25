from openai import OpenAI
import os
from dotenv import load_dotenv

# Get OpenAI API key
load_dotenv() 
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define delimiter
delimiter = "####"

# General function to get response with gpt-3.5
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.6, max_tokens=2000):
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
    
def generate_comment():
    system_message_comment=f"""
    Product details can be found as below

        "TechPro Ultrabook": 
            "name": "TechPro Ultrabook",
            "category": "Computers and Laptops",
            "brand": "TechPro",
            "model_number": "TP-UB100",
            "warranty": "1 year",
            "rating": 4.5,
            "features": ["13.3-inch display", "8GB RAM", 
                    "256GB SSD", "Intel Core i5 processor"],
            "description": "A sleek and lightweight ultrabook for everyday use.",
            "price": 799.99
        
        "BlueWave Gaming Laptop": 
            "name": "BlueWave Gaming Laptop",
            "category": "Computers and Laptops",
            "brand": "BlueWave",
            "model_number": "BW-GL200",
            "warranty": "2 years",
            "rating": 4.7,
            "features": ["15.6-inch display", "16GB RAM", 
                    "512GB SSD", "NVIDIA GeForce RTX 3060"],
            "description": "A high-performance gaming laptop for 
                    an immersive experience.",
            "price": 1199.99
        
        "PowerLite Convertible": 
            "name": "PowerLite Convertible",
            "category": "Computers and Laptops",
            "brand": "PowerLite",
            "model_number": "PL-CV300",
            "warranty": "1 year",
            "rating": 4.3,
            "features": ["14-inch touchscreen", "8GB RAM", 
                    "256GB SSD", "360-degree hinge"],
            "description": "A versatile convertible laptop with 
                    a responsive touchscreen.",
            "price": 699.99
        
        "TechPro Desktop": 
            "name": "TechPro Desktop",
            "category": "Computers and Laptops",
            "brand": "TechPro",
            "model_number": "TP-DT500",
            "warranty": "1 year",
            "rating": 4.4,
            "features": ["Intel Core i7 processor", "16GB RAM", 
                    "1TB HDD", "NVIDIA GeForce GTX 1660"],
            "description": "A powerful desktop computer for work 
                    and play.",
            "price": 999.99

    "BlueWave Chromebook": 
            "name": "BlueWave Chromebook",
            "category": "Computers and Laptops",
            "brand": "BlueWave",
            "model_number": "BW-CB100",
            "warranty": "1 year",
            "rating": 4.1,
            "features": ["11.6-inch display", "4GB RAM", 
                    "32GB eMMC", 
                    "Chrome OS"],
            "description": "A compact and affordable Chromebook 
                    for everyday tasks.",
            "price": 249.99
        
        "SmartX ProPhone": 
            "name": "SmartX ProPhone",
            "category": "Smartphones and Accessories",
            "brand": "SmartX",
            "model_number": "SX-PP10",
            "warranty": "1 year",
            "rating": 4.6,
            "features": ["6.1-inch display", "128GB storage", 
                    "12MP dual camera", "5G"],
            "description": "A powerful smartphone with advanced 
                    camera features.",
            "price": 899.99
        
        "MobiTech PowerCase": 
            "name": "MobiTech PowerCase",
            "category": "Smartphones and Accessories",
            "brand": "MobiTech",
            "model_number": "MT-PC20",
            "warranty": "1 year",
            "rating": 4.3,
            "features": 
                ["5000mAh battery", "Wireless charging", 
                "Compatible with SmartX ProPhone"],
            "description": 
                "A protective case with built-in battery 
                for extended usage.",
            "price": 59.99
        
        "SmartX MiniPhone": 
            "name": "SmartX MiniPhone",
            "category": "Smartphones and Accessories",
            "brand": "SmartX",
            "model_number": "SX-MP5",
            "warranty": "1 year",
            "rating": 4.2,
            "features": ["4.7-inch display", "64GB storage", 
                    "8MP camera", "4G"],
            "description": "A compact and affordable smartphone 
                    for basic tasks.",
            "price": 399.99
        
        "MobiTech Wireless Charger": 
            "name": "MobiTech Wireless Charger",
            "category": "Smartphones and Accessories",
            "brand": "MobiTech",
            "model_number": "MT-WC10",
            "warranty": "1 year",
            "rating": 4.5,
            "features": ["10W fast charging", "Qi-compatible", 
                    "LED indicator", "Compact design"],
            "description": "A convenient wireless charger for 
                    a clutter-free workspace.",
            "price": 29.99
        
        "SmartX EarBuds": 
            "name": "SmartX EarBuds",
            "category": "Smartphones and Accessories",
            "brand": "SmartX",
            "model_number": "SX-EB20",
            "warranty": "1 year",
            "rating": 4.4,
            "features": ["True wireless", "Bluetooth 5.0", 
                    "Touch controls", "24-hour battery life"],
            "description": "Experience true wireless freedom with 
                    these comfortable earbuds.",
            "price": 99.99

        "CineView 4K TV": 
            "name": "CineView 4K TV",
            "category": "Televisions and Home Theater Systems",
            "brand": "CineView",
            "model_number": "CV-4K55",
            "warranty": "2 years",
            "rating": 4.8,
            "features": ["55-inch display", "4K resolution", 
                    "HDR", "Smart TV"],
            "description": "A stunning 4K TV with vibrant colors 
                    and smart features.",
            "price": 599.99

    """

    user_message_comment=f"""
    Imgine you're an e-commerce store customer. Assume that you already bought one of products above and used for a period, please generate a comment based on your experience. You can choose sentiment to be either positive or negative.Words limit: 100 words in total."""

    messages_comment =  [  
    {'role':'system', 
    'content': system_message_comment},    
    {'role':'user', 
    'content': f"{delimiter}{user_message_comment}{delimiter}"},  
    {'role':'assistant',
    'content':'talk as a customer'}
    ] 
    comment = get_completion_from_messages(messages_comment)
    print("Comment from customers: ")
    print(comment+"\n")
    return comment

generate_comment()