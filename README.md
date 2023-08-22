# Steam Games Recommendation System
Original [Dataset](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam) from Kaggle

In this project I aimed to create a gaming recomendation system using an appropriate similarity metric and collaborative filtering to provide personal recommendations. Each file represents a different stage in the project, ending with an efficient Hybrid Recommender.



## [Scraper.py](https://github.com/AhmecC/games_recommendation_system/blob/main/scraper.py)
Sampled top 2500 games from Kaggle dataset:
> - Used steamAPI to attain Developer & Publisher information
> - Ran again to obtain as much missing possible as possible (left with 2433 games) 

## [Metadata Recommender.py](https://github.com/AhmecC/games_recommendation_system/blob/main/Metadata%20Recommender.py)

Created sample of top 2500 games by number of recommendations:
> - Cleaned data by removing irrelevant columns and creating new worthwhile ones

Used IMDB weighted rating formula:
> - [v/(v+m)*R + m/(m+v)*C]
> - v is game specific total recommendations, m is minumim number of reviews to be included
> - R is game specific average rating, C is average rating of all sampled games

Created Similarity Metric:
> - Initially tested using just description test as metadata
>   - *Dataset contained short description, but i believe that the long description would've aided much greater*
> - Extended to also include tags, developer, publisher and if the game was free
>   - Increased weights for tags, developer & publisher
> - Most similar games were ordered by weighted rating to ensure high quality games were recommended     

## [Collaborative Filtering.py'](https://github.com/AhmecC/games_recommendation_system/blob/main/Collaborative%20Filtering.py)

I first attained a dataframe of users with their recommendations (a binary value of True or False), and kept only reviews that were part of the sampled games. As my sample kept the top 2500 most reviewed games, i was left with just under 26 million reviews. I then shorted this down to 400,000 by taking the top 5000 users with most reviews.  I made an assumption that if games were not played they were not recommended and thus set to 0.

... to be continued

## [Hybrid Recommender.py](https://github.com/AhmecC/games_recommendation_system/blob/main/Hybrid%20Recommender.py)

This combined the final models from the previous section into one efficient system. I used the metadata to calculate the similarity between games. I then used collaborative filtering to find games similar to what they've recommended. This returned the most similar games given what they've played, thus personalising their recommendations.

### Potential Further Improvements:

This project could be improved further:
- Use long description instead of short description, as for some games it does not effectively describe it harming similarity calculations
- Naturally allow for more games and reviews, given computing power availability!
