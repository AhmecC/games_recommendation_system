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


### --- Get User-Game matrix --- ###
pivot_df = reviews.pivot(index='user_id', columns='app_id', values='is_recommended')  # 
pivot_df = pivot_df * 1  # Convert True/False into Binary values
pivot_df = pivot_df.fillna(0)  # Assume games not played are not recommended 


### --- Normalise to give more weight to users with less reviews --- ###
df = pivot_df.reset_index()
df_items = df.drop('user_id', axis=1)  # Dataset without user_id column

magnitude = np.sqrt(np.square(df_items).sum(axis=1))
df_items = df_items.divide(magnitude, axis='index')  # Normalised


### --- Calculate Cosine Similarity --- ###
def calculate_similarity(df_items):
    df_sparse = sparse.csr_matrix(df_items)
    sim = cosine_similarity(df_items.transpose())
    sim = pd.DataFrame(data=similarities, index=df_items.columns, columns=df_items.columns)
    return sim

df_items = df_items.fillna(0)
df_matrix = calculate_similarity(df_items)  # Returns similarity matrix between all games

df_matrix.loc[10].nlargest(11)  # Returns 10 most similar games to counter-strike based on just other users recommendations




### --- Adding a Neighborhood --- ###
user = 8159759
user_index = df[df.user_id == user].index.to_list()[0]  # Location of user_id in df

df_nghbrs = pd.DataFrame(index=df_matrix.columns, columns=range(1,11))
for i in range(0, len(df_matrix.columns)):
    df_nghbrs.iloc[i,:10] = df_matrix.iloc[0:,i].sort_values(ascending=False)[:10].index  
# ^^ df_nghbrs is a  matrix of 10 most similar games for each game

known_recom = df_items.iloc[user_index]
known_recom = known_recom[known_recom > 0].index.values  # Games user has recommended


most_sim_likes = df_nghbrs[df_nghbrs.index.isin(known_recom)]  # Nghbr matrix but just for games they recommended
sim_list = most_sim_likes.values.tolist() 
sim_list = list(set([item for sublist in sim_list for item in sublist]))
# ^^ Creates single list of all similar app_id's


nghbrd = df_matrix[sim_list].loc[sim_list]  # Matrix of all neighbour app_id's in a smaller matrix


user_vector = df_items.iloc[user_index].loc[sim_list]  # Vector of user's recommendations (including weight)
score = nghbrd.dot(user_vector).div(nghbrd.sum(axis=1))  # Work out Score
score = score.drop(known_recom) # Drop games they've already played
clean_df[clean_df['app_id'].isin(score.nlargest(20).index)].head(10)[['title','wr']]





