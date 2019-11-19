import configparser
import spotipy

config = configparser.ConfigParser()
config.read('../docs/config.ini')
spotipy_client_id = config['Spotipy']['client_id']
spotipy_client_secret = config['Spotipy']['client_secret']

print(spotipy_client_id)