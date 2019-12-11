import csv
import os
import pickle

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

DATA_FILE = "/data/artists_and_lyrics.csv"
OUTPUT_FILE = "/data/artists_and_lyrics_vector.pickle"

def extract_features(corpus):
  vectorizer = TfidfVectorizer()
  feature_vector = vectorizer.fit_transform(corpus)
  print("Generated a feature vector of shape: " + str(feature_vector.shape))
  return feature_vector

def main():
  current_directory = os.getcwd()
  
  # Extract lyrics from data file
  with open(current_directory + DATA_FILE, 'r') as in_f:
    reader = csv.reader(in_f)
    input_list = list(reader)
    in_f.close()
    
  lyrics = np.asarray([item[2] for item in input_list])
  
  # Extract features from the lyrics
  feature_vector = extract_features(lyrics)

  # Save vectorizer object for later use
  with open(current_directory + OUTPUT_FILE, 'wb') as out_f:
    pickle.dump(feature_vector, out_f)
    out_f.close()

if __name__ == "__main__":
  main()