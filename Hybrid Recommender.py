import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

clean_df = pd.read_csv('completed_df.csv')  # File from the end of Metadata Recommender.py
reviews_df = pd.read_csv('reviews_df.csv')  # File from start of Collaborative Filtering.py (top users reviews)




### --- Cosine Similarity Section --- ###
tf = TfidfVectorizer(stop_words = 'english')
tfidf_matrix = tf.fit_transform(clean_df.soup)
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix
                     



### --- Collaborative Filtering Section --- ###
original = reviews_df.pivot(index='user_id', columns = 'app_id', values = 'is_recommended') * 1
original = original.reset_index()
original_items = original.drop('user_id', axis = 1)  # Doesn't assume not played games aren't recommended
df = original.fillna(0)  # Assumed if not played, it's not recommended

A,B = clean_df.app_id.value_counts().index, reviews_df.appp_id.value_counts().index
C = list(set(A) - set(B))  # some games in clean_df (2433 games) not in reviews_df (2200 games)
new_df = pd.Dataframe(0, index = range(5000), columns = C)
df = pd.concat([df, new_df], axis=1) # To keep matrix the same size as cosine_sim, we add missing games as 0's to df

D = clean_df.app_id.tolist()
E = [x for x in D if x not in C]
df = df[['user_id'] + D]  # Set ordering the same as clean_df (for consistency with cosine_sim)
original = original[['user_id'] + E]  # Set ordering the same for original too (just without the missing games)

df_items = df.drop('user_id', axis=1)
df_matrix = pd.Dataframe(cosine_sim, index = clean_df.app_id, columns = clean_df.app_id)  # similarity matrix with app_id index and columns




### --- Hybrid Recommender --- ###
def hybrid(user):
    original_index = original[original.user_id == user].index.to_list()[0]  
    original_vector = original_items.iloc[original_index]
    known_games = original_vector[original_vector.notnull()].index.values  # Ensurd all played games are not recommended
  
    user_index = df[df.user_id == user].index.to_list()[0]  # get index of user
    user_rating_vector = df_items.iloc[user_index] 
    score = score.nlargest(20)

    
    score = df_matrix.dot(user_rating_vector).div(df_matrix.sum(axis=1))  # Calculate relveance score
    score = score.drop(known_games) # drop all known games from rankings
    
    top_games = clean_df[clean_df['app_id'].isin(score.index)][['title','wr']]
    top_games['relevance'] = score.values  # create relevance score column
    top_games = top_games.head(20).sort_values('wr', ascending=False)  # sort by best rated
    
  
    known_games = clean_df[clean_df['app_id'].isin(known_recom)][['title','Developer', 'Publisher']]
    return top_games, known_games


### --- How it Works --- ###
user_id = reviews_df.user_id.sample().item()

hybrid(user_id)[0].head(10)  # Games they're recommended
hybrid(user_id)[1] # Games they've played


