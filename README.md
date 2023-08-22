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
>   - *Dataset contained short description, but i believe that the long description would've been more beneficial*
> - Extended to also include tags, developer, publisher and if the game was free
>   - Increased weights for tags, developer & publisher
> - Most similar games were ordered by weighted rating to ensure high quality games were recommended     



## [Collaborative Filtering.py'](https://github.com/AhmecC/games_recommendation_system/blob/main/Collaborative%20Filtering.py)

Very helpful [article](https://medium.com/radon-dev/item-item-collaborative-filtering-with-binary-or-unary-data-e8f0b465b2c3) to help deal with binary data

Reduced dataframe of user reviews to just contain sampled games:
> - Left with 26 million reviews, so reduced further by only including reviews of top 5000 reviews (400,000 reviews)
> - Created user-game matrix and assumed if not played its not recommended (set to 0)

Building Collaborative filtering model:
> - Normalised user reviews so those with less ratings are worth more
> - Calculated item-item similarity using article formula
> - Defined neighbourhood to improve efficiency
> - used similarity matrix and weighted ratings to determine best user recommendations



## [Hybrid Recommender.py](https://github.com/AhmecC/games_recommendation_system/blob/main/Hybrid%20Recommender.py)

Combined aspects from previous models to build more efficient model:
> - Use metadata recommender to create a similarity matrix
> - Created 2 user-item matrices, one with assumption not played are 0 and one without
> - Use matrices without assumption to obtain known games so games they have reviewed are not recommended
> - Use same scoring metric as in collaborative filtering model
> - sort most relevant games by their weighted rating and return personalised recommendations
