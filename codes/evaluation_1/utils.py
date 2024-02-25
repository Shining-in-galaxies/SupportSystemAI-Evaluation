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
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.3, max_tokens=500):
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

import products
import json 
from collections import defaultdict

# Generate customer prompt
def generate_comment():
    system_message_comment=f"""
    Product details can be found as below
    Assume that you are a customer to an electronic product company.
    Products information delimited by tripe backticks in its own language. 
    Products: ```{products.products_data}```
    """
    
    user_message_comment=f"""
    A less than 100 words comment about the products"""

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

def get_product_by_name(name):
    return products.products_data.get(name, None)

def get_products_by_category(category):
    return [product for product in products.products_data.values() if product["category"] == category]


def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None   
    
def get_products():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, 'product.json')
    
    with open(file_path, 'r') as file:
        products = json.load(file)
    return products
    
def get_products_and_category():
    products = get_products()
    products_by_category = defaultdict(list)
    for product_name, product_info in products.items():
        category = product_info.get('category')
        if category:
            products_by_category[category].append(product_info.get('name'))
    return dict(products_by_category)

def get_products_from_query(user_msg):
    products_and_category = get_products_and_category()
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of json objects, where each object has the following format:
        'category': <one of Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
    OR
        'products': <a list of products that must be found in the allowed products below>

    Where the categories and products must be found in the customer service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.

    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    Allowed products: {products_and_category}

    """
    
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{user_msg}{delimiter}"},  
    ] 
    category_and_product_response = get_completion_from_messages(messages)
    
    return category_and_product_response

def get_mentioned_product_info(data_list):
    product_info_l = []

    if data_list is None:
        return product_info_l

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        product_info_l.append(product)
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    product_info_l.append(product)
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")
            
    return product_info_l

def answer_user_msg(user_msg,product_info):
    system_message = f"""
    You are a customer service assistant for a large electronic store. \
    Respond in a friendly and helpful tone, with concise answers. \
    Make sure to ask the user relevant follow up questions.
    """
    # user_msg = f"""
    # tell me about the smartx pro phone and the fotosnap camera, the dslr one. Also what tell me about your tvs"""
    messages =  [  
    {'role':'system', 'content': system_message},   
    {'role':'user', 'content': f"{delimiter}{user_msg}{delimiter}"},  
    {'role':'assistant', 'content': f"Relevant product information:\n{product_info}"},   
    ] 
    response = get_completion_from_messages(messages)
    return response