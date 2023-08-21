import numpy as np
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity  

games = pd.read_csv('games.csv')  # Games information
users = pd.read_csv('users.csv')  # User_ID total games played/reviews information
recom = pd.read_csv('recommendations.csv')  # Game Recommended? by user_ID
gmd = pd.read_json('games_metadata.json', lines=True)  # Games description and tags




### -- Sample has 2500 games with > 2000 reviews -- ###
merged = pd.merge(games, gmd, how='inner', on='app_id')
merged.title = merged.title.apply(lambda x: x.replace('®','').replace('™','').lower())  # Clean titles for easier use
df = merged[merged.user_reviews > 2000].sample(n=2500, replace=False) 
df.shape # (2500,15)

### -- Initial sample cleaning -- ###
df['year'] = pd.to_datetime(df['date_release']).apply(lambda x: str(x).split('-')[0])
df['free'] = df['price_final'].apply(lambda x: 'free' if x==0 else 'paid')
df = df.drop(['date_release', 'win', 'mac', 'linux', 'price_final', 'price_original', 'discount', 'steam_deck'], axis=1)

### -- df ~~> clean_df after API usage -- ##
reorder = ['app_id', 'year', 'title', 'rating', 'positive_ratio', 'user_reviews', 'description','tags', 'Developer', 'Publisher', 'free']
clean_df = clean_df[reorder]
clean_df = clean_df.dropna()
clean_df.shape #(2433, 11) 




### -- Calculate weighted rating using IMDB formula -- ###
def weighted_rating(x):
    v = x['user_reviews'] # vote number for specific game
    R = x['positive_ratio'] # average rating for specific game
    return (v/(v+m)*R)+(m/(m+v)*C)
  
m = 2000  # Min reviews to be in chart, same criteria to be in sample
C = clean_df.positive_ratio.mean() # Average rating of sampled games
clean_df['wr'] = clean_df.apply(weighted_rating, axis=1)

clean_df.sort_values('wr', ascending=False).head(5)[['title','positive_ratio','wr']]
# ^ Wallpaper Engine, Stardew Valley, Portal 2, Vampire Survivors, People Playground




### -- Description Only based recommender -- ### 
def get_recommendations(title):
    idx = indices[title.lower()]  # Find location of game in dataframe
    sim_scores = list(enumerate(cosine_sim[idx]))  # Find similarity with other games
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # List scores in descending order
    sim_scores = sim_scores[1:31]
    game_indices = [i[0] for i in sim_scores]  # Get id's
    return titles.iloc[game_indices] # return top 30 most similar games

tf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tf.fit_transform(clean_df['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)  # This measures similarity
clean_df = clean_df.reset_index()  
indices = pd.Series(clean_df.index, index=clean_df.title)  

get_recommendations('call of duty').head(10)
# ^ returns games it deems similar by what its description said




### -- Metadata based recommender -- ### 
clean_df['equal'] = clean_df.apply(lambda x: 'yes' if x['Developer'] == x['Publisher'] else 'no', axis=1)  # If Developer/Publisher are the same we don't include twice
clean_df['Developer'] = clean_df['Developer'].apply(lambda x: str.lower(x.replace(" ", "")))
clean_df['Developer'] = clean_df['Developer'].apply(lambda x: f'{x} {x} {x} {x} {x} {x} {x} {x}') # Increase Weight                                                   
clean_df['Publisher'] = clean_df['Publisher'].apply(lambda x: str.lower(x.replace(" ", "")))                           
clean_df['Publisher'] = clean_df['Publisher'].apply(lambda x: f'{x} {x} {x} {x} {x}')  # Increase Weight

clean_df['tags'] = clean_df['tags'].apply(literal_eval) # Fix list 
s = clean_df.apply(lambda x: pd.Series(x['tags']),axis=1).stack().reset_index(level=1, drop=True) # Take out tags from list
s.name = 'tags'  
s = s.value_counts()
s = s[s > 1]  # includes all unique tags which are prevalent more than once

def filter_tags(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

clean_df['tags'] = clean_df.tags.apply(filter_tags)
clean_df['tags'] = clean_df.tags.apply(lambda x: [str.lower(i.replace(' ','')) for i in x])
clean_df['tags'] = clean_df['tags'].apply(lambda x: ' '.join(x))  # Joins tags into one line
clean_df['tags'] = clean_df['tags'].apply(lambda x: f'{x} {x} {x}')

clean_df['soup'] = clean_df.apply(lambda x: x['description'] + x['tags'] + x['Developer'] + x['Publisher'] + x['free'] if x['equal'] == 'no' else x['description'] + x['tags'] + x['Developer'] + x['free'], axis=1)
# ^ If Developer = Publisher to stop overweighing we only put Developer in this case

count = CountVectorizer(stop_words='english')  # 
count_matrix = count.fit_transform(clean_df.tags)
cosine_sim = cosine_similarity(count_matrix, count_matrix)  # Work out Cosine Similarity

indices = pd.Series(clean_df.index, index=clean_df.title)  
get_recommendations('call of duty').head(10)  # Get different results using same function




### -- Sort most similar by weighted rating  -- ### 

def improved_recomendations(title):
    idx = indices[title.lower()]  # Section same as get_recommendations
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    game_indices = [i[0] for i in sim_scores]
    
    games_ = clean_df.iloc[game_indices][['title','year','positive_ratio','user_reviews', 'Developer', 'Publisher','wr']].sort_values('wr', ascending=False)
    # ^ Sort the 20 most similar by the weighted rating to provide high quality suggestions
    return games_













