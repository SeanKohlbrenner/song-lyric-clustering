from bs4 import BeautifulSoup
import re
import string
from urllib.request import urlopen

  
# Retrieve lyrics from AZLyrics.com by letter of artist name
def get_data(data_file):
  print(repr(get_lyrics("https://www.azlyrics.com/lyrics/billwithers/aintnosunshine.html")))
  
# Helper function to retrieve lyrics from a song page
  # Returns a string containing lyrics
def get_lyrics(url):
  html = urlopen(url)
  soup = BeautifulSoup(html, "html.parser")

  song_title = soup.find("div", {"class": "ringtone"}).next_sibling.next_sibling
  
  if (str(soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"}).contents[12]) == "<br/>"):
    target_div = soup.find("div", 
                           {"class": "col-xs-12 col-lg-8 text-center"}
                           ).contents[14]
  else:
    target_div = soup.find("div", 
                           {"class": "col-xs-12 col-lg-8 text-center"}
                           ).contents[17]
  
  lyrics = ""
  for item in target_div.contents[2:]:
    lyrics = lyrics + str(item)
  
  lyrics = preprocess_text(lyrics)
  return(lyrics)


# Remove stopwords, accents, tags, contractions, special characters, and 
#   prefixes/affixes
def preprocess_text(in_str):
  print(in_str)
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
  stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "can", "will", "just", "should", "now"]
  in_str = in_str.split(" ")
  for word in reversed(stopwords):
    for i in in_str:
      try:
        in_str.remove(word)
      except:
        continue
  in_str = " ".join(in_str)
  
  return(in_str)

# Use TF-iDF to determine word importance
def extract_features():
  pass

def main():
  data_file = open("lyrics.csv", "a+")
  get_data(data_file)
  
if __name__ == '__main__':
  main()