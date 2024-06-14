from pyexpat.errors import messages
import requests
from .api import MARTA
import openai
from google.transit import gtfs_realtime_pb2

# Set your API keys here
MARTA_API_KEY = '3db0ab30-d7a8-4b08-9a0e-9b153e51de2a'
OPENAI_API_KEY = 'your_openai_api_key'
base_url = 'http://developer.itsmarta.com'
#CACHE_EXPIRE = int(getenv('MARTA_CACHE_EXPIRE', 30))
TRAIN_PATH = '/RealtimeTrain/RestServiceNextTrain/GetRealtimeArrivals'
MARTA_GTFS_REALTIME_URL = 'https://gtfs-rt.itsmarta.com/TMGTFSRealTimeWebService/tripupdate'



# Function to fetch data from MARTA's API
def get_marta_train(TRAIN_PATH,**kwergs):
    headers = {
        'api_key': MARTA_API_KEY
    }
    response = requests.get(f'{base_url}/{TRAIN_PATH}', headers=headers, **kwergs)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

# Function to fetch and parse GTFS Realtime data
def fetch_gtfs_realtime_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    return feed

# Function to format GTFS Realtime data for ChatGPT
def format_gtfs_data(feed):
    formatted_data = []
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            formatted_data.append(f"Trip ID: {trip_update.trip.trip_id}, Start Time: {trip_update.trip.start_time}, Route ID: {trip_update.trip.route_id}")
            return "\n".join(formatted_data)

# Function to link Marta Train info to ChatGPT
def martatrain_to_chatgpt(TRAIN_PATH, **kwergs):
    marta_train_data = get_marta_train(TRAIN_PATH, **kwergs)
    chatgpt_response = chatgpt_interaction(marta_train_data)
    
    return chatgpt_response

# Function to interact with ChatGPT API
def chatgpt_interaction(marta_train_data):
    #for loop to extract value from key value pairs
    train_data = marta_train_data.keys();
    
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(
        engine="gpt-3.5-turbo", 
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
