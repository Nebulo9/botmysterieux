import os, json, requests
from .logger import LOGGER

DATA_DIR = 'data/'

def get_guild_data(guild_id:int):
    """Reads and returns the dictionnary of guild data from the guild's JSON data file."""
    path = os.path.join(DATA_DIR, f'{guild_id}.json')
    with open(path,'r') as f:
        return json.load(f)
    
def save_guild_data(guild_id:int, data):
    """Writes the dictionnary of guild data to the guild's JSON data file."""
    path = os.path.join(DATA_DIR, f'{guild_id}.json')
    with open(path,'w') as f:
        json.dump(data, f, indent=2)

def create_guild_data(guild_id:int):
    """Creates a new guild data file."""
    path = os.path.join(DATA_DIR, f'{guild_id}.json')
    with open(path,'w') as f:
        json.dump({'features':{'joke':{'enabled': False},'role':{'enabled': False}, 'reply': {'enabled': False}, 'ratio': {'enabled': False}}}, f, indent=2)
        LOGGER.debug(f'Created data file for guild {guild_id}.')

def delete_guild_data(guild_id:int):
    """Deletes the guild data file."""
    path = os.path.join(DATA_DIR, f'{guild_id}.json')
    os.remove(path)
    LOGGER.debug(f'Deleted data file for guild {guild_id}.')

def is_feature_enabled(feature:str,data=None,guild_id=0):
    """Returns True if the feature is enabled in the guild, False otherwise."""
    if data:
        return data['features'][feature]['enabled']
    else:
        return get_guild_data(guild_id)['features'][feature]['enabled']

def get_response(url:str,attr=""):
        try:
            if attr:
                return requests.get(url).json()[attr]
            else:
                return requests.get(url).json()
        except Exception as e:
            LOGGER.error(f"Error while getting response from {url}: {e}")
            return dict()