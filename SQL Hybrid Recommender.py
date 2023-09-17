# >>> This version uses SQL to improve efficiency
import numpy as np
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

# ----- CONNECT TO MySQL DATABASE ----- #
cnx = sqlite3.connect('recommender.db')
cursor = cnx.cursor()



# ----- CREATING DATABASE TABLES ----- #
cursor.execute("""CREATE TABLE games_data
        (app_id INTEGER, year INTEGER, title TEXT, rating TEXT,
        positive_ratio FLOAT, user_reviews INTEGER, description TEXT, tags TEXT,
        Developer TEXT, Publisher TEXT, free TEXT, wr FLOAT, equal TEXT, soup TEXT)""")
clean_df.to_sql('games_data', cnx, if_exists='append', index=False)  # Easily append df like this

cursor.execute("""CREATE TABLE review_data
        (app_id INTEGER, title TEXT, helpful INTEGER, funny INTEGER, is_recommended BOOLEAN, 
        hours REAL, user_id INTEGER, review_id INTEGER, products INTEGER, reviews INTEGER)""")
reviews_df.to_sql('review_data', cnx, if_exists='append', index=False)



# ----- ADD PERSONAL GAMES ----- #
def add_reviews(app_id):
    cursor.execute(f"SELECT title FROM games_data WHERE app_id = {app_id}")
    title = cursor.fetchall()[0][0]
    return (app_id, title, 0, 0, True, 5, 1, 0, 3, 3)  # returns correct format to add to table

list_IDs = [214510, 945360, 400, 1593500, 292030, 990080, 1888930, 1245620, 285160, 629820, 1030840, 1030830, 271590, 1817190,
        356190, 391220, 393080, 1233570, 1238840, 1222140, 1174180, 782330, 379720, 1151640, 1238080, 1817070, 225540, 552520,
        517630, 447040]

cursor.execute("SELECT app_id FROM games_data")
ordering = [app_id[0] for app_id in cursor.fetchall()]  # Get list of all app_id's

data = []  # only contains games that exist
for id in list_IDs:
    if id in clean_df['app_id'].values:
        data.append(add_reviews(id)) 

data = pd.DataFrame(data, columns=['app_id', 'title', 'helpful', 'funny', 'is_recommended', 'hours', 'user_id', 'review_id', 'products', 'reviews'])
data.to_sql('review_data', cnx, if_exists='append', index=False)  # Append personal games



# ----- CALCULATE COSINE SIMILARITY ----- #
cursor.execute('SELECT soup FROM games_data')
soup = [row[0] for row in cursor.fetchall()]  # Soup contains description, tags, developer, publisher and if free!

tfv = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfv.fit_transform(soup) 
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)  # Similarity metric uses game metadata



# ----- CREATE MATRIX ----- #
og = pd.read_sql('SELECT user_id, app_id, is_recommended FROM review_data', con=cnx)
og = og.pivot(index='user_id', columns='app_id', values='is_recommended').reset_index().fillna(0)  # If not played assumed not recommended

cursor.execute("SELECT app_id FROM games_data WHERE app_id NOT IN (SELECT app_id FROM review_data)")
app_ids = [app_id[0] for app_id in cursor.fetchall()]
new_df = pd.DataFrame(0, index=range(5001), columns=app_ids)
og = pd.concat([og, new_df], axis=1)  # Add missing ID's to reviews_df

cursor.execute("SELECT app_id FROM games_data")
ordering = [app_id[0] for app_id in cursor.fetchall()]
og = og[['user_id'] + ordering]

og_items = og.drop('user_id', axis=1)
og_matrix = pd.DataFrame(cosine_sim, index=ordering, columns=ordering)



# ----- HYBRID MATRIX ----- #
def hybrid(user):
    cursor.execute(f"SELECT app_id FROM review_data WHERE user_id = {user}")
    known_games = [app_id[0] for app_id in cursor.fetchall()]
    
    user_index = og[og.user_id == user].index.to_list()[0]
    user_rating_vector = og_items.iloc[user_index] 

    score = og_matrix.dot(user_rating_vector).div(og_matrix.sum(axis=1))
    score = score.drop(known_games)    
    score = score.nlargest(20)
    
    app_ids = ','.join(map(str, score.index))
    top_games = pd.read_sql(f'SELECT title, wr FROM games_data WHERE app_id IN ({app_ids})', con=cnx)
    top_games['relevance'] = score.values
    top_games = top_games.head(10).sort_values('wr', ascending=False)
    
    known_games = ','.join(map(str, known_games))
    known_games = pd.read_sql(f'SELECT title FROM games_data WHERE app_id IN ({known_games})', con=cnx).title
    return top_games, known_games

user_id = 1
hybrid(user_id)[0].head(10)
hybrid(user_id)[1]











