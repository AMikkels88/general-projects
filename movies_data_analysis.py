# testing movies data analysis project
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_url = 'https://api.themoviedb.org/3'
api_key = "d7bcde821afbdc346d9f46af6be295bf"

endpoint = '/movie/popular'
params = {'api_key': api_key}
response = requests.get(base_url + endpoint, params=params)
data = response.json()

genre_map = {
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
    37: "Western"
}

movies = data['results']
df = pd.DataFrame(movies)

genre_counts = df['genre_ids'].explode().value_counts()
# Flatten genre_ids list
df['genre_ids'] = df['genre_ids'].apply(lambda x: [int(genre_id) for genre_id in x])
df['genre_map'] = df['genre_ids'].apply(lambda x: [genre_map[genre_id] for genre_id in x])


