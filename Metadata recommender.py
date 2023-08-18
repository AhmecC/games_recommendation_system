import numpy as np
import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity  
from nltk.stem.snowball import SnowballStemmer

games = pd.read_csv('games.csv')  # Games information
users = pd.read_csv('users.csv')  # User_ID total games played/reviews information
recom = pd.read_csv('recommendations.csv')  # Game Recommended? by user_ID
gmd = pd.read_json('games_metadata.json', lines=True)  # Games description and tags




### -- Sample has 2500 games with > 2000 reviews -- ##
merged = pd.merge(games, gmd, how='inner', on='app_id')
merged.title = merged.title.apply(lambda x: x.replace('®','').replace('™','').lower())  # Clean titles for easier use
df = merged[merged.user_reviews > 2000].sample(n=2500, replace=False) 
df.shape # (2500,15)

### -- Initial sample cleaning -- ##
df['year'] = pd.to_datetime(df['date_release']).apply(lambda x: str(x).split('-')[0])
df['free'] = df['price_final'].apply(lambda x: 'free' if x==0 else 'paid')
df = df.drop(['date_release', 'win', 'mac', 'linux', 'price_final', 'price_original', 'discount', 'steam_deck'], axis=1)

### -- df ~~> clean_df after API usage -- ##
reorder = ['app_id', 'year', 'title', 'rating', 'positive_ratio', 'user_reviews', 'description','tags', 'Developer', 'Publisher', 'free']
clean_df = clean_df[reorder]
clean_df = clean_df.dropna()
clean_df.shape #(2433, 11) 




### -- Calculate weighted rating using IMDB formula -- ##
def weighted_rating(x):
    v = x['user_reviews'] # vote number for specific game
    R = x['positive_ratio'] # average rating for specific game
    return (v/(v+m)*R)+(m/(m+v)*C)
  
m = 2000  # Min reviews to be in chart, same criteria to be in sample
C = clean_df.positive_ratio.mean() # Average rating of sampled games
clean_df['wr'] = clean_df.apply(weighted_rating, axis=1)

clean_df.sort_values('wr', ascending=False).head(5)[['title','positive_ratio','wr']]
# ^ Wallpaper Engine, Stardew Valley, Portal 2, Vampire Survivors, People Playground




### -- Content Based Recommender -- ## 












