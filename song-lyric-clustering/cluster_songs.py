import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics.pairwise import cosine_similarity

CUR_DIRECTORY = os.getcwd()
DATA_FILE = "/data/artists_and_lyrics.csv"
OUT_FILE = "/results/song_cluster.png"

GENERATE_IMAGE = 1


# =============================================================================
# extract_features: Use TF-IDF to extract numerical data from corpus
# Input:
#     - corpus: a 3d list contianing: ["lyrics", "lyrics", etc...]
#     - row_labels: list of artists and song names to use as the row names in 
#         the data frame 
# Output: A pandas data frame containing the TF-IDF feature vector
# =============================================================================
def extract_features(corpus, row_labels):
  # Create feature vector using scikit learn TfidfVectorizer
  vectorizer = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
  feature_vector = vectorizer.fit_transform(corpus)
  print("Generated a feature vector of shape: " + str(feature_vector.shape))
  
  feature_vector = feature_vector.toarray()
  labels = vectorizer.get_feature_names()
  
  # generate a pandas dataframe to hold the feature vector
  feature_dataframe = pd.DataFrame(np.round(feature_vector, 2), 
                                   columns=labels, 
                                   index = row_labels)
  '''tfidf_vectorizer = TfidfVectorizer(max_df=0.8, min_df=0.2, use_idf=True)

  tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
  
  return tfidf_matrix'''
  
  return feature_dataframe
  

# =============================================================================
# get_feature_vector: retrieve a feature vector for corpus from input file
# Input: None
# Output: A scikit learn feature vector
# =============================================================================
def get_feature_dataframe():
  # Extract lyrics from data file
  with open(CUR_DIRECTORY + DATA_FILE, 'r') as in_f:
    reader = csv.reader(in_f)
    input_list = list(reader)
    in_f.close()
  
  # Data from file used for labels and corpus
  artists = np.asarray([item[0] for item in input_list])
  songs = np.asarray([item[1] for item in input_list])
  lyrics = np.asarray([item[2] for item in input_list])
  dataframe_indices = []
  for i in range(len(artists)):
    artist_and_song = str(artists[i]) + ": " + str(songs[i])
    dataframe_indices.append(artist_and_song)
    
  # Extract features from the lyrics
  feature_dataframe = extract_features(lyrics, dataframe_indices)
    

  return feature_dataframe
  

# =============================================================================
# get_distance_matrix: compute cosine distance between each document in the 
#     feature_vector
# Input:
#     - feature_vector: TF-IDF feature vector
# Output: A scikit learn feature vector
# =============================================================================
def get_distance_matrix(feature_dataframe, row_labels):
  similarity_matrix = cosine_similarity(feature_dataframe)
  similarity_dataframe = pd.DataFrame(similarity_matrix, index = row_labels)
  
  return similarity_dataframe


def main():  
  # Get a feature vector for the corpus
  feature_dataframe = get_feature_dataframe()
  
  # Compute cosine distance between each document
  with open(CUR_DIRECTORY + DATA_FILE, 'r') as in_f:
      reader = csv.reader(in_f)
      input_list = list(reader)
      in_f.close()
  # Data from file used for labels and corpus
  artists = np.asarray([item[0] for item in input_list])
  songs = np.asarray([item[1] for item in input_list])
  dataframe_indices = []
  for i in range(len(artists)):
    artist_and_song = str(artists[i]) + ": " + str(songs[i])
    dataframe_indices.append(artist_and_song)
  similarity_matrix = get_distance_matrix(feature_dataframe, dataframe_indices)
  
  # Compute hierarchical cluster using Ward's clustering algorithm
  Z = linkage(similarity_matrix, 'ward')
  plt.figure(figsize=(100, 250))
  plt.title('Song Lyric Clustering')
  plt.xlabel('Songs and Aritsts')
  plt.ylabel('Distance')
  dendrogram(Z, orientation='left', labels = artists)
  plt.axhline(y=1.0, c='k', ls='--', lw=0.5)
  
  
  if GENERATE_IMAGE:
    plt.savefig(CUR_DIRECTORY + OUT_FILE, dpi=800) #save figure as ward_clusters
  
  
  

  

if __name__ == "__main__":
  main()