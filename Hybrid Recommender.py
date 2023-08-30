import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

clean_df = pd.read_csv('completed_df.csv')  # File from the end of Metadata Recommender.py
reviews_df = pd.read_csv('reviews_df.csv')  # File from start of Collaborative Filtering.py (top users reviews)






### --- Add your own personal reviews --- ###
list_IDs = [214510, 945360, 400, 1593500, 292030, 990080, 1888930, 1245620, 285160, 629820, 1030840, 1030830, 271590, 1817190,
        356190, 391220, 393080, 1233570, 1238840, 1222140, 1174180, 782330, 379720, 1151640, 1238080, 1817070, 225540, 552520,
        517630, 447040]  # Some games i've played

def add_personal_reviews(app_id):
    title = clean_df[clean_df.app_id == app_id].title.item()   
    row = {'app_id': app_id,
          'title': title,
          'helpful': 0,
          'funny': 0,
          'is_recommended': True,
          'hours': 5,
          'user_id': 1,
          'products' : 3,
          'reviews' : 3}
    return row

data = []
for id in list_IDs:
    if id in clean_df['app_id'].values:
        data.append(add_personal_reviews(id))

data = pd.DataFrame(data)
reviews_df = pd.concat([reviews_df, data], ignore_index=True)






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
new_df = pd.Dataframe(0, index = range(5001), columns = C) 
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

    score = df_matrix.dot(user_rating_vector).div(df_matrix.sum(axis=1))  # Calculate relveance score
    score = score.drop(known_games) # drop all known games from rankings
    score = score.nlargest(20)

    top_games = clean_df[clean_df['app_id'].isin(score.index)][['title','wr']]
    top_games['relevance'] = score.values  # create relevance score column
    top_games = top_games.head(20).sort_values('wr', ascending=False)  # sort by best rated
    
    known_games = clean_df[clean_df['app_id'].isin(known_recom)][['title','Developer', 'Publisher']]
    return top_games, known_games


### --- How it Works --- ###
user_id = reviews_df.user_id.sample().item()  # random user_id
# user_id = 1  # To check your own preferences 

hybrid(user_id)[0].head(10)  # Games they're recommended
hybrid(user_id)[1] # Games they've played


