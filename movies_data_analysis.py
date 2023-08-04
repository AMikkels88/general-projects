# testing movies data analysis project idea quickly
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import logging

# API details
BASE_URL = "https://api.themoviedb.org/3"
API_KEY = "d7bcde821afbdc346d9f46af6be295bf"
# endpoint = "/movie/popular"
ENDPOINT = "/discover/movie"
MAX_PAGE = 500  # set by API limits
GENRE_MAP = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentary",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "Thriller",
    10752: "War",
    37: "Western",
}

# Common parameters for both time periods
common_params = {
    'api_key': API_KEY,
    'vote_average.gte': 5
}
# Currently run 2 time periods, 1990s and 2010s
time_periods = [
    {'primary_release_date.gte': '1990-01-01', 'primary_release_date.lte': '2000-12-31'},
    {'primary_release_date.gte': '2010-01-01', 'primary_release_date.lte': '2020-12-31'}
]

# Get data from API
all_movies = []
for time_period in time_periods:
    page = 1
    params = {**common_params, **time_period, 'page': page}
    
    while page < MAX_PAGE:
        response = requests.get(BASE_URL + ENDPOINT, params=params)
        data = response.json()
        try:
            movies = data['results']
        except KeyError as e:
            logging.error(f"Data not returned correctly, likely a page limit exceeded")
            logging.error(f"KeyError: {e}")
            break        
        
        all_movies.extend(movies)
        print(movies[0]["release_date"])
        print(page)
        page += 1
        params['page'] = page

# Data processing
df = pd.DataFrame(all_movies)
df.drop(columns=[
    "adult",
    "backdrop_path",
    "original_language",
    "original_title",
    "video",
    "vote_count"],
    axis=1,
    inplace=True,
)
genre_counts = df["genre_ids"].explode().value_counts()
# Flatten genre_ids list
df["genre_ids"] = df["genre_ids"].apply(lambda x: [int(genre_id) for genre_id in x])
df["genre_map"] = df["genre_ids"].apply(
    lambda x: [GENRE_MAP[genre_id] for genre_id in x]
)
df['release_date'] = pd.to_datetime(df['release_date'])


# TODO:
# perform some basic genre analysis
# use NLP (spaCy / scikit)? to analyse the title text and maybe overview text, looking
# for repeated franchise words, numbered movies etc, to get a sense of rate of sequels / remakes
# compare these from say 90s to 2010s

