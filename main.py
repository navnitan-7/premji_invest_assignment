import os
from datetime import date, datetime
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.api.your_story import ys_get_top_5_search, ys_get_article_body
from src.api.fin_shots  import fin_get_top_5_search, fin_get_article_body
from src.api.sentiment_analysis  import sentiment_analysis
from src.api.raise_alert  import raise_alert
from src.utils.utils  import get_driver, update_status, get_status,age_group, get_ml_100_data, base_path, get_top_similar_movies

def pipeline1():
    try:
        driver = get_driver()
        today = date.today()
        # update_status("pipeline1", "in_progress", today)
        #Your Story
        keywords = ["HDFC","Tata Motors"]
        df_ys = None
        for keyword in keywords:
            if df_ys is None:
                df_ys = ys_get_top_5_search(driver, keyword)
            else:
                df_temp = ys_get_top_5_search(driver, keyword)
                df_ys =  pd.concat([df_ys,  df_temp], ignore_index=True, axis=0)

        df_ys[['title', 'body']] = df_ys['url'].apply(lambda url: pd.Series(ys_get_article_body(url)))

        #Fin Shots
        df_fin = None
        for keyword in keywords:
            if df_fin is None:
                df_fin = fin_get_top_5_search(keyword)
            else:
                df_temp = fin_get_top_5_search(keyword)
                df_fin =  pd.concat([df_fin,  df_temp], ignore_index=True, axis=0)
        df_fin['body'] = df_fin['url'].apply(lambda url: pd.Series(fin_get_article_body(url)))

        df_article = pd.concat([df_fin,  df_ys], ignore_index=True, axis=0)
        df_article["sentiment_score"] = df_article[["company", "title","body"]].apply(lambda x: sentiment_analysis())
        df_article.to_csv(f"{base_path}/pipeline1/staging/{today}.csv", index=False)
        df_final =  df_article.groupby(['company']).agg(
            sentiment=('sentiment_score', 'mean')
        )
        df_final.to_csv(f"{base_path}/pipeline1/published/{today}.csv", index=False)
        update_status("pipeline1", "success", today)
        print("Success")
    except:
        update_status("pipeline1", "failed", today)
        raise_alert()

def pipeline2():
    try:
        today = date.today()
        status = get_status("pipeline1", today)
        while(status != "success"):
            raise Exception("previous job did not succeed")

        ratings, movies, users = get_ml_100_data()

        #Task1
        mean_age = users.groupby(['occupation']).agg(
            mean_age=('age', 'mean')
        )
        mean_age = mean_age.reset_index()
        mean_age_path = os.path.join(base_path, "pipeline2/published/mean_age_per_occupation.csv")
        mean_age.to_csv(mean_age_path, index=False)

        #Task2
        top_ratings = ratings.groupby(['movie_id']).agg(
            rating=('rating', 'mean'),
            user_count=('user_id', 'count'),
        )
        top_ratings = top_ratings.reset_index()
        top_ratings = top_ratings[top_ratings["user_count"]>=35]
        top_ratings = top_ratings.sort_values(by=['rating'], ascending=False)
        top_ratings = top_ratings.head(20)
        top_ratings = top_ratings.join(movies[["movie_id","title"]], how="inner", on="movie_id", lsuffix="_")
        top_ratings = top_ratings.drop(["movie_id_", "user_count", "movie_id"], axis=1)
        top_ratings_path = os.path.join(base_path, "pipeline2/published/top_rated_movies.csv")
        top_ratings.to_csv(top_ratings_path, index=False)

        #Task3
        users['age_group'] = users['age'].apply(age_group)
        merged_df = ratings.merge(users, on="user_id").merge(movies, on="movie_id")
        genre_cols = ["Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", 
                    "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", 
                    "Thriller", "War", "Western"]
        merged_df = merged_df.melt(id_vars=['user_id', 'age', 'gender', 'occupation', 'age_group', 'rating'], 
                                value_vars=genre_cols, var_name="genre", value_name="is_genre")
        merged_df = merged_df[merged_df["is_genre"] == 1] 
        merged_df.drop(columns=["is_genre"], inplace=True)
        genre_ratings = (merged_df.groupby(['age_group', 'occupation', 'genre'])
                                    .size()
                                    .reset_index(name='rating_count'))
        top_genres = (genre_ratings.sort_values(['age_group', 'occupation', 'rating_count'], ascending=[True, True, False])
                                    .groupby(['age_group', 'occupation'])
                                    .head(1))  # Get the top genre per occupation and age group
        top_genres_path = os.path.join(base_path, "pipeline2/published/top_genre_movies.csv")
        top_genres.to_csv(top_genres_path, index=False)

        #Task4
        user_item_matrix = ratings.pivot_table(index='user_id', columns='movie_id', values='rating')
        user_item_matrix = user_item_matrix.fillna(0)
        movie_similarity = pd.DataFrame(cosine_similarity(user_item_matrix.T), 
                                        index=user_item_matrix.columns, 
                                        columns=user_item_matrix.columns)
        df_similar_movie = get_top_similar_movies(movie_id=50,
                                    similarity_df=movie_similarity, 
                                    ratings_df=ratings, 
                                    top_n=10, 
                                    similarity_threshold=0.70, 
                                    co_occurrence_threshold=50)
        
        similar_movie_path = os.path.join(base_path, "pipeline2/published/top_similar_movies.csv")
        df_similar_movie.to_csv(similar_movie_path, index=False)
    except:
        raise_alert()

if __name__ == "__main__":
    t1 = datetime.now()
    pipeline1()
    pipeline2()
    t2 = datetime.now()
    print(t2-t1)
