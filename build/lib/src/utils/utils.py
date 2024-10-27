import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

#change it to your path
base_path="c:/Users/snavn/Desktop/premji invest/src/data"

def  get_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    return driver

def check_status_file(path):
    columns = ['date', 'status']
    try:
        df = pd.read_csv(path)
        return df
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)
        df.to_csv(path, index=False)
        return df
    
def update_status(pipeline:str, status:str, date):
    path = f"{pipeline}/status.csv"
    path = os.path.join(base_path, path)
    df = check_status_file(path)
    if str(date) in df['date'].values:
        df.loc[df['date'] == str(date), 'status'] = status
    else:
        new_row = pd.DataFrame({'date': [str(date)], 'status': [status]})
        df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(path, index=False)

def get_status(pipeline:str, date):
    path = f"{pipeline}/status.csv"
    path = os.path.join(base_path, path)
    try:
        df = pd.read_csv(path)
        status = list(df.loc[df['date'] == str(date), 'status'].values)[0]
        return status
    except:
        return "failed"

def get_ml_100_data():
    # Define file paths (adjust paths if necessary)
    ratings_file = os.path.join(base_path, 'pipeline2/landing/ml-100k/u.data')
    movies_file =  os.path.join(base_path, 'pipeline2/landing/ml-100k/u.item')
    users_file =  os.path.join(base_path, 'pipeline2/landing/ml-100k/u.user')

    ratings = pd.read_csv(
        ratings_file, 
        sep='\t', 
        names=['user_id', 'movie_id', 'rating', 'timestamp']
    )

    movies = pd.read_csv(
        movies_file, 
        sep='|', 
        names=['movie_id', 'title', 'release_date', 'video_release_date', 'IMDb_URL', 
            'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 
            'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'],
        encoding='latin-1'
    )

    users = pd.read_csv(
        users_file, 
        sep='|', 
        names=['user_id', 'age', 'gender', 'occupation', 'zip_code']
    )

    return ratings, movies, users

  
def age_group(age):
    age = int(age)
    if 20 <= age < 25:
        return '20-25'
    elif 25 <= age < 35:
        return '25-35'
    elif 35 <= age < 45:
        return '35-45'
    else:
        return '45 and older'

def get_top_similar_movies(movie_id, similarity_df, ratings_df, top_n=10, similarity_threshold=0.70, co_occurrence_threshold=50):

    similar_movies = similarity_df[movie_id].reset_index()
    similar_movies.columns = ['movie_id', 'similarity_score']
    similar_movies = similar_movies[similar_movies['similarity_score'] >= similarity_threshold]

    co_occurrence_counts = {}
    for other_movie_id in similar_movies['movie_id']:
        users_movie = set(ratings_df[ratings_df['movie_id'] == movie_id]['user_id'])
        users_other_movie = set(ratings_df[ratings_df['movie_id'] == other_movie_id]['user_id'])
        co_occurrence_counts[other_movie_id] = len(users_movie.intersection(users_other_movie))
    
    similar_movies['strength'] = similar_movies['movie_id'].map(co_occurrence_counts)
    similar_movies = similar_movies[similar_movies['strength'] >= co_occurrence_threshold]
    similar_movies = similar_movies[similar_movies['movie_id'] != movie_id]
    similar_movies = similar_movies.sort_values(by=['similarity_score', 'strength'], ascending=[False, False])
    
    return similar_movies.head(top_n)
