## Steam Games Recommendation System
This Game recommender creates personalised recommendations based on the games that a user has played. It uses the similarity between games, user-based collaborative filtering and the weighted rating to deliver the best recommendations possible. ```SQL Hybrid Recommender.py``` is the final product :)


## Skills Used
I adeptly used the **steamAPI** to further enrich the dataset, creating an essential algorithm to obtain more meaningful data. I identified the significant potential of **TF-IDF** to acquire insights from a wealth of text, which helped create a sophisticated similarity metric. I demonstrated proficiency in **pandas** and **SQL**, by creating a clean structured and organised database, which boosted the efficiency of the Recommender. My **Mathematical** knowledge was tested in this project, especially in the field of matrices and vectors. I used this knowledge to fuse the weightings from collaborative filtering and the similarity metrics, allowing for a meticulously curated list for recommendation.


## Extra Information
- Dataset is from [Kaggle](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam) but used SteamAPI to get additional information
- Only top 2500 games and top 5000 reviewers (400,000 total reviews) looked at to mantain performance
- Similarity metric uses description, tags, developer, publisher and if free.
- Files go from Scraper >> Metadata Recommender >> Collaborative Filtering >> Hybrid Recommender >> SQL Hybrid Recommender
