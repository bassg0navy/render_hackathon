from pyexpat.errors import messages
import requests
from .api import MARTA
import openai

# Set your API keys here
MARTA_API_KEY = '3db0ab30-d7a8-4b08-9a0e-9b153e51de2a'
OPENAI_API_KEY = 'your_openai_api_key'
base_url = 'http://developer.itsmarta.com'
#CACHE_EXPIRE = int(getenv('MARTA_CACHE_EXPIRE', 30))
TRAIN_PATH = '/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals'
BUS_PATH = '/BRDRestService/RestBusRealTimeService/GetAllBus'
BUS_ROUTE_PATH = '/BRDRestService/RestBusRealTimeService/GetBusByRoute/'



# Function to fetch data from MARTA's API
def get_marta_bus(BUS_PATH, **kwergs):
    headers = {
        'api_key': MARTA_API_KEY
    }
    response = requests.get(f'{base_url}/{BUS_PATH}', headers=headers, **kwergs)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def get_marta_bus_route(BUS_ROUTE_PATH, **kwergs):
    headers = {
        'api_key': MARTA_API_KEY
    }
    response = requests.get(f'{base_url}/{BUS_ROUTE_PATH}', headers=headers, **kwergs)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

def get_marta_train(TRAIN_PATH,**kwergs):
    headers = {
        'api_key': MARTA_API_KEY
    }
    response = requests.get(f'{base_url}/{TRAIN_PATH}', headers=headers, **kwergs)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

# Example function to link MARTA's API to ChatGPT
def marta_to_chatgpt(BUS_PATH, **kwergs):
    # Fetch data from MARTA API
    marta_bus_data = get_marta_bus(BUS_PATH, **kwergs)
    
    # Get response from ChatGPT
    chatgpt_response = chatgpt_interaction(marta_bus_data)
    
    return chatgpt_response

def martabusroute_to_chatgpt(BUS_ROUTE_PATH, **kwergs):
    marta_busroute_data = get_marta_bus_route(BUS_ROUTE_PATH, **kwergs)
    chatgpt_response = chatgpt_interaction(marta_busroute_data)
    
    return chatgpt_response

def martatrain_to_chatgpt(TRAIN_PATH, **kwergs):
    marta_train_data = get_marta_train(BUS_ROUTE_PATH, **kwergs)
    chatgpt_response = chatgpt_interaction(marta_train_data)
    
    return chatgpt_response

# Function to interact with ChatGPT API
def chatgpt_interaction(marta_bus_data):
    #for loop to extract value from key value pairs
    bus_data = marta_bus_data.keys();
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",  # Choose the appropriate engine
        messages=[
            {"role":"system", "content":""},
            {"role":"system", "content":""},
            {"role":"system", "content":""}
            ],
        max_tokens=150  # Adjust as necessary
    )
    return response.choices[0].text.strip()


# Example usage
if __name__ == '__main__':
    endpoint = 'your_endpoint_here'  # e.g., 'buses'
    params = {'route': '100'}  # Example parameters
    response = marta_to_chatgpt(endpoint, params)
    print(response)
