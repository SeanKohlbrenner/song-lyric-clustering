import csv
import os
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import dendrogram, linkage, ward
from sklearn.metrics.pairwise import cosine_similarity

CUR_DIRECTORY = os.getcwd()
DATA_FILE = "/data/artists_and_lyrics.csv"
FEATURE_DATAFRAME_FILE = "/data/artists_and_lyrics_dataframe.pickle"
COSINE_SIMILARITY_FILE = "/data/cosine_similarity.pickle"

# Control program execution
# If values are set to 0 the program will read objects from pickle files
GEN_FEATURE_DATAFRAME = 0
GEN_DISTANCE_MATRIX = 0


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
  # Generate feature vector using DATA_FILE
  if GEN_FEATURE_DATAFRAME:
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
    
    # Save vectorizer object for later use
    with open(CUR_DIRECTORY + FEATURE_DATAFRAME_FILE, 'wb') as out_f:
      pickle.dump(feature_dataframe, out_f)
      out_f.close()
    
  # Load feature vector from FEATURE_VECTOR_FILE
  else:
    with open(CUR_DIRECTORY + FEATURE_DATAFRAME_FILE, "rb") as in_f:
      feature_dataframe = pickle.load(in_f)
      in_f.close()
  
  return feature_dataframe
  

# =============================================================================
# get_distance_matrix: compute cosine distance between each document in the 
#     feature_vector
# Input:
#     - feature_vector: TF-IDF feature vector
# Output: A scikit learn feature vector
# =============================================================================
def get_distance_matrix(feature_dataframe, row_labels):
  # Compute cosine distance using feature_vector and save it to pickle file
  if GEN_DISTANCE_MATRIX:
    similarity_matrix = cosine_similarity(feature_dataframe)
    similarity_dataframe = pd.DataFrame(similarity_matrix, index = row_labels)
    
    # Save cosine similarity object for later use
    with open(CUR_DIRECTORY + COSINE_SIMILARITY_FILE, 'wb') as out_f:
      pickle.dump(similarity_dataframe, out_f)
      out_f.close()
      
  # Load cosine distance matrix from pickle file
  else:
    with open(CUR_DIRECTORY + COSINE_SIMILARITY_FILE, "rb") as in_f:
        similarity_dataframe = pickle.load(in_f)
        in_f.close()
  
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
  '''Z = linkage(similarity_matrix, 'ward')
  #pd.DataFrame(Z, columns=dataframe_indices, dtype='object')
  #plt.figure(figsize=(8, 3))
  plt.title('Song Lyric Clustering')
  plt.xlabel('Songs and Aritsts')
  plt.ylabel('Distance')
  dendrogram(Z, orientation='right')
  plt.axhline(y=1.0, c='k', ls='--', lw=0.5)
  #plt.savefig('cluster.png')'''
  
  linkage_matrix = ward(similarity_matrix) #define the linkage_matrix using ward clustering pre-computed distances

  fig, ax = plt.subplots(figsize=(15, 20)) # set size
  ax = dendrogram(linkage_matrix, orientation="right", labels=artists);

  plt.tick_params(\
      axis= 'x',          # changes apply to the x-axis
      which='both',      # both major and minor ticks are affected
      bottom='off',      # ticks along the bottom edge are off
      top='off',         # ticks along the top edge are off
      labelbottom='off')

  plt.tight_layout() #show plot with tight layout
  
  #uncomment below to save figure
  plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters
  
  #max_dist = 1.0

  #cluster_labels = fcluster(Z, max_dist, criterion='distance')
  #cluster_labels = pd.DataFrame(cluster_labels, columns=['ClusterLabel'])
  #pd.concat([corpus_df, cluster_labels], axis=1)
  
  

  

if __name__ == "__main__":
  main()