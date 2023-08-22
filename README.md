# Steam Games Recommendation System
Original Dataset : https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam 

This project aimed to create a recommendation system using similarity between games given metadata (description, tags, developer, publisher, free?) and user-user collaborative filtering to help personalise recommendations given games they've recommended. Each file represents a different stage in the project, ending with an efficient Hybrid recommender.

## Scraper.py

After sampling the large dataset attained from kaggle, i used the steamAPI to get the Developer and Publisher information for the 2500 sampled games. I then obtained some final missing information for games (description, tags). After removing missing data i was left with 2433 games.

## Metadata Recommender.py

The first part included creating the sample and then running this through scraper.py to get as much information as possible. I then cleaned the data by removing unnecesary columns and creating new relevant columns. 

I then created the weighted rating using IMDB formula of [v/(v+m)*R + m/(m+v)*C] where v is the game specific number of reviews, m is the min reviews to be included, R is the game specific average rating, and C the average rating of all sampled games. 

I then first tested creating the similarity metric using only the description text as metadata. This achieved promising results but could be further improved. Thus i extended the model to include also the tags, developer, publisher and if the game was free or not. I increased the weights for tags, developer and publisher to make sure they had a strong effect on determing if games were similar. Once the most similar games were returned i ordered them by the weigted rating to ensure high quality games are recommended despite them being potentially less relevant tha others.

## Collaborative Filtering.py

I first attained a dataframe of users with their recommendations (a binary value of True or False), and kept only reviews that were part of the sampled games. As my sample kept the top 2500 most reviewed games, i was left with just under 26 million reviews. I then shorted this down to 400,000 by taking the top 5000 users with most reviews.  I made an assumption that if games were not played they were not recommended and thus set to 0.

... to be continued

## Hybrid Recommender.py

This combined the final models from the previous section into one efficient system. I used the metadata to calculate the similarity between games. I then used collaborative filtering to find games similar to what they've recommended. This returned the most similar games given what they've played, thus personalising their recommendations.

### Potential Further Improvements:

This project could be improved further:
- Use long description instead of short description, as for some games it does not effectively describe it harming similarity calculations
- Naturally allow for more games and reviews, given computing power availability!
