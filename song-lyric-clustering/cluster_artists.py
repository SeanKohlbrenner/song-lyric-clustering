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
OUT_FILE = "/results/artist_cluster.png"

# Control program execution
# If values are set to 0 the program will read objects from pickle files
GEN_FEATURE_DATAFRAME = 0
GEN_DISTANCE_MATRIX = 0


# =============================================================================
# cluster_and_plot: Compute hierarchical cluster using Ward's clustering 
#     algorithm. Generate a plot of the dendrogram
# Input:
#     - similarity_matrix: cosine similarity of the feature dataframe
#     - artists: list of all artists
# Output: None
# =============================================================================
def cluster_and_plot(similarity_matrix, artists):
  # Compute hierarchical cluster using Ward's clustering algorithm
  Z = linkage(similarity_matrix, 'ward')
  plt.figure(figsize=(10, 25))
  plt.tick_params(axis='x', 
                  which='both', 
                  bottom=False, 
                  top=False, 
                  labelbottom=False)
  plt.title('Billboard 2019 Top Artists Clustering')
  plt.xlabel('Distance')
  plt.ylabel('Artists')
  dendrogram(Z, 
             orientation = "left", 
             labels = artists, 
             leaf_font_size = 7, 
             color_threshold = 2)
  plt.savefig(CUR_DIRECTORY + OUT_FILE)
  
  
# =============================================================================
# generate_feature_dataframe: Use TF-IDF to extract numerical data from corpus
# Input:
#     - artist_lyrics: a list containing [artist, lyrics]
# Output: A pandas data frame containing the TF-IDF feature vector
# =============================================================================
def generate_feature_dataframe(artist_lyrics):
  corpus = np.asarray([item[1] for item in artist_lyrics])
  vectorizer = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
  feature_vector = vectorizer.fit_transform(corpus)
  print("Generated a feature vector of shape: " + str(feature_vector.shape))
  
  feature_vector = feature_vector.toarray()
  feature_dataframe = pd.DataFrame(np.round(feature_vector, 2))
  
  return feature_dataframe


# =============================================================================
# combine_artist_lyrics: Combine song lyrics in the data file together under 
#     each artist
# Input: None
# Output: An array [artist, lyrics]
# =============================================================================
def combine_artist_lyrics():
  # Extract lyrics from data file
  with open(CUR_DIRECTORY + DATA_FILE, 'r') as in_f:
    reader = csv.reader(in_f)
    input_list = list(reader)
    in_f.close()
  
  # Combine artists songs into a dictionary {artist: lyrics}
  artist_lyrics_dict = {}
  for item in input_list:
    if item[0] in artist_lyrics_dict:
      artist_lyrics_dict[item[0]] = \
        str(artist_lyrics_dict[item[0]]) + " " + str(item[2])
    else:
      artist_lyrics_dict[item[0]] = str(item[2])
  
  # Convert dictionary back to array [artist, lyrics]
  artist_lyrics = []
  for key, value in artist_lyrics_dict.items():
    temp = [key,value]
    artist_lyrics.append(temp)
  
  return artist_lyrics


# =============================================================================
# main: drive program that generates a hierarchical cluster of artists based on 
#     their song lyrics
# =============================================================================
def main():
  # Combine all lyrics for an artist to generate the dataframe
  artist_lyrics = combine_artist_lyrics()
  # Save artist names for dendrogram label
  artists = np.asarray([item[0] for item in artist_lyrics])
  
  # Retrieve feature dataframe
  feature_dataframe = generate_feature_dataframe(artist_lyrics)
  
  # Compute cosine similarity
  similarity_matrix = cosine_similarity(feature_dataframe)
  
  # Compute cluster and plot
  cluster_and_plot(similarity_matrix, artists)
  
  
if __name__ == "__main__":
  main()