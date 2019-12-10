import csv
import os
import random
import re
import requests
import string

from bs4 import BeautifulSoup
from time import sleep
from urllib.request import urlopen

# Start and end index of the in_file to gather data for
DATA_RETR_START_INDEX = 0
DATA_RETR_END_INDEX = 102

# Range of time to wait between gathering each song's lyrics in seconds
TIME_LOW_BOUND = 2
TIME_HIGH_BOUND = 5

# Number of songsto be collected for each artist
NUM_SONGS_PER_ARTIST = 50



USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
HEADERS = {'User-Agent': USER_AGENT}
BASE_URL = "https://www.azlyrics.com"


# Use file 
  # Get artist name
  # Get artist page
    # Pick x random songs
    # Get lyrics from song and write to file

# =============================================================================
# get_data: Using an artist's name, retrieve NUM_SONGS_PER_ARTIST song lyrics
# Input:
#     - artist: the artist name to query
# Output: A list of song lyrics (each index is a song)
# =============================================================================
def get_data(artist):
  # Get the artist's page url
  artist_url = get_artist_url(artist)
  
  # Get list of lyrics
  artist_songs = get_songs(artist_url)
  
  return(artist_songs)

# =============================================================================
# get_artist_url: Using an artist's name, retrieve the url of their page
# Input:
#     - artist: the artist name to query
# Output: the artist's page url
# =============================================================================
def get_artist_url(artist):
  # Make the search
  response = requests.get("https://search.azlyrics.com/search.php?q=" + str(artist), headers=HEADERS)
  html = response.content
  
  soup = BeautifulSoup(html, "html.parser")
  artist_list = soup.find("td", {"class": "text-left visitedlyr"})
  
  # Return first result
  return(artist_list.find("a")["href"])
  

# =============================================================================
# get_songs: retrieve NUM_SONGS_PER_ARTIST lyrics from an artist's page
# Input:
#     - artist_url: the artist's page url
# Output: A 3D list:
#     [["title", "lyrics"],
#      ["title", "lyrics"]
# =============================================================================
def get_songs(artist_url):
  # Get NUM_SONGS_PER_ARTIST random songs and append lyrics to a list
  response = requests.get(artist_url, headers=HEADERS)
  html = response.content
  
  soup = BeautifulSoup(html, "html.parser")
  
  # Collect all songs
  songs = soup.find("div", {"id": "listAlbum"}).findAll("a")
  
  song_list = []
  for song in songs:
    song_list.append(song["href"].replace("..", BASE_URL))
  
  # Get lyrics for NUM_SONGS_PER_ARTIST random songs in list
  lyrics_for_artist = []
  # If the artist has the same or fewer number of songs - do all of them
  if (len(song_list) <= NUM_SONGS_PER_ARTIST):
    for song_url in song_list:
      lyrics_for_artist.append(get_lyrics(song_url))
      # Set timer to not overload the server
      sleep_time = random.randint(TIME_LOW_BOUND, TIME_HIGH_BOUND)
      print("Sleep: " + str(sleep_time))
      sleep(sleep_time)
  else:
    for song_url in random.sample(song_list, NUM_SONGS_PER_ARTIST):
      lyrics_for_artist.append(get_lyrics(song_url))
      # Set timer to not overload the server
      sleep_time = random.randint(TIME_LOW_BOUND, TIME_HIGH_BOUND)
      print("Sleep: " + str(sleep_time))
      sleep(sleep_time)
    
  # Return full list
  return(lyrics_for_artist)

# =============================================================================
# get_lyrics: Retrieve lyrics from a song page
# Input:
#     - song_url: page containing song lyrics
# Output: list: ["title", "lyrics"]
# =============================================================================
def get_lyrics(song_url):
  html = urlopen(song_url)
  soup = BeautifulSoup(html, "html.parser")
  
  # Find the song
  song_title = str(soup.find("div", {"class": "ringtone"}).next_sibling.next_sibling).replace("\"", "")
  cleanr = re.compile('<.*?>')
  song_title = re.sub(cleanr, '', song_title)
  
  print("Gathering lyrics for: " + song_title)
  
  # If there is a feature the page is set up differently
  if (str(soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"}).contents[12]) == "<br/>"):
    target_div = soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"}).contents[14]
  else:
    target_div = soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"}).contents[17]
  
  # Save and process the lyrics
  lyrics = ""
  for item in target_div.contents[2:]:
    lyrics = lyrics + str(item)
  
  lyrics = preprocess_text(lyrics)
  
  title_lyric_pair = [song_title, lyrics]
  return(title_lyric_pair)


# =============================================================================
# preprocess_text: clean the lyrics by removing unnecessary elements
# Input:
#     - in_str: dirty text
# Output: A string containing cleaned lyrics
# =============================================================================
def preprocess_text(in_str):
  #print(in_str)
  # Remove capital letters
  in_str = in_str.lower()
  
  # Remove html tags
  cleanr = re.compile('<.*?>')
  in_str = re.sub(cleanr, '', in_str)
  
  # Remove hidden characters
  in_str = in_str.replace("\n\n", " ")
  in_str = in_str.replace("\n", " ")
  in_str = in_str.replace("\r", "")
  
  # Remove accents  - Nothing yet - i cant find a good way to do this
  
  # Remove contractions
  contractions_dict = {
    "ain't": "are not",
    "aren't": "are not",
    "can't": "can not",
    "can't've": "can not have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how're": "how are",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you shall have",
    "you're": "you are",
    "you've": "you have"}
  for key in contractions_dict:
    in_str = in_str.replace(key, contractions_dict[key])
    
  # Remove punctuation
  in_str = in_str.translate(str.maketrans('', '', string.punctuation))
    
  # Remove possessive contractions
  in_str = in_str.replace("\'s", "")
  
  # Remove first and last characters - always blank from source
  in_str = in_str[1:-1]
  
  # Minimal stemming  - Too difficult to do right now
  #in_str = in_str.replace("ing ", " ")
  #in_str = in_str.replace("es ", " ")
  #in_str = in_str.replace("ed ", " ")
  
  # Remove stopwords
  stopwords = ["i", 
               "me", 
               "my", 
               "myself", 
               "we", 
               "our", 
               "ours", 
               "ourselves", 
               "you", 
               "your", 
               "yours", 
               "yourself", 
               "yourselves", 
               "he", 
               "him", 
               "his", 
               "himself", 
               "she", 
               "her", 
               "hers", 
               "herself", 
               "it", 
               "its", 
               "itself", 
               "they", 
               "them", 
               "their", 
               "theirs", 
               "themselves", 
               "what", 
               "which", 
               "who", 
               "whom", 
               "this", 
               "that", 
               "these", 
               "those", 
               "am", 
               "is", 
               "are", 
               "was", 
               "were", 
               "be", 
               "been", 
               "being", 
               "have", 
               "has", 
               "had", 
               "having", 
               "do", 
               "does", 
               "did", 
               "doing", 
               "a", 
               "an", 
               "the", 
               "and", 
               "but", 
               "if", 
               "or", 
               "because", 
               "as", 
               "until", 
               "while", 
               "of", 
               "at", 
               "by", 
               "for", 
               "with", 
               "about", 
               "against", 
               "between", 
               "into", 
               "through", 
               "during", 
               "before", 
               "after", 
               "above", 
               "below", 
               "to", 
               "from", 
               "up", 
               "down", 
               "in", 
               "out", 
               "on", 
               "off", 
               "over", 
               "under", 
               "again", 
               "further", 
               "then", 
               "once", 
               "here", 
               "there", 
               "when", 
               "where", 
               "why", 
               "how", 
               "all", 
               "any", 
               "both", 
               "each", 
               "few", 
               "more", 
               "most", 
               "other", 
               "some", 
               "such", 
               "no", 
               "nor", 
               "not", 
               "only", 
               "own", 
               "same", 
               "so", 
               "than", 
               "too", 
               "can", 
               "will", 
               "just", 
               "should", 
               "now"]
  
  in_str = in_str.split(" ")
  for word in reversed(stopwords):
    for i in in_str:
      try:
        in_str.remove(word)
      except:
        continue
  in_str = " ".join(in_str)
  
  return(in_str)

# =============================================================================
# extract_features: Convert the corpus into a feature vector ready for analysis
# Input:
#     - 
# Output: 
# =============================================================================
# Use TF-iDF to determine word importance
def extract_features():
  pass

def main():
  # Get path to in/out files
  current_directory = os.getcwd()
  in_file_path = current_directory + "/data/artists.csv"
  out_file_path = current_directory + "/data/artists_and_lyrics.csv"
  
  artists = []
  
  # Loop through artist list to get lyrics for an artist
  with open(in_file_path, "r") as in_f:
    # Append the artist's lyrics to .csv file
    artists = list(csv.reader(in_f))
    in_f.close()
  
  # Use the web scraper to gether artist data
  with open(out_file_path, "a+") as out_f:
    # Run web scraper on artists
    for artist in artists[DATA_RETR_START_INDEX:DATA_RETR_END_INDEX]:
      lyrics_for_artist = get_data(artist)
      
      # Append each song to data file
      for song in lyrics_for_artist:
        out_f.write(song[0] + "," + song[1] + "\n")
    out_f.close()
  
if __name__ == '__main__':
  main()