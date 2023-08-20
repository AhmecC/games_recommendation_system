from surprise import Reader, Dataset, SVDpp
from surprise.model_selection import cross_validate
from scipy import sparse

### --- Get Dataframe of recommendations for sampled games only --- ###
recommended = pd.merge(clean_df, recom, how='inner', on='app_id')
recommended = recommended.drop(['index', 'rating', 'positive_ratio', 'user_reviews', 'description', 'tags', 'year', 'equal', 'soup', 'date','free','Developer','Publisher','wr'], axis=1)
recommened = recommended.drop([2109460, 13560, 327890, 942970, 1517960], axis=0)  # Have less than 98 reviews not helpful
recommended.shape  # (25891173, 8)


### --- Get users with lots of reviews --- ###
top_users = users.sort_values('reviews', ascending=False).head(3000).user_id  # 142 is lowest
reviews = pd.merge(recommended, top_users, how='inner', on='user_id')  # Only reviews for sampled games
how_much.shape  # 54,489 False and 243,792 True


### --- Get user-game matrix --- ###
pivot_df = reviews.pivot(index='user_id', columns='app_id', values='is_recommended')  # 
pivot_df = pivot_df * 1  # Convert True/False into Binary values
pivot_df = pivot_df.fillna(0)  # Assume games not played are not recommended 


### --- Normalise to give more weight to users with less reviews --- ###
df = pivot_df.reset_index()
df_items = df.drop('user_id', axis=1)

magnitude = np.sqrt(np.square(df_items).sum(axis=1))
df_items = df_items.divide(magnitude, axis='index')  # Normalised


### --- Calculate Cosine Similarity --- ###
def calculate_similarity(df_items):
    df_sparse = sparse.csr_matrix(df_items)
    sim = cosine_similarity(df_items.transpose())
    sim = pd.DataFrame(data=similarities, index=df_items.columns, columns=df_items.columns)
    return sim

df_items = df_items.fillna(0)
df_matrix = calculate_similarity(df_items)  # Returns 

df_matrix.loc[10].nlargest(11)  # Returns 10 most similar games to counter-strike based on just other users recommendations




### --- --- ###
user = 32444
user_index = df[df.user_id == user].index.to_list()[0]













