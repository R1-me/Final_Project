import requests
import random
from utils.media_classes import Movie, Series

API_KEY = "c6a0d52ba0f3977064cacc87989e4326"
BASE_URL = "https://api.themoviedb.org/3"

# Dictionary to map API genre IDs to readable strings
GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi", 10770: "TV Movie",
    53: "Thriller", 10752: "War", 37: "Western",
    10759: "Action & Adventure", 10762: "Kids", 10763: "News",
    10764: "Reality", 10765: "Sci-Fi & Fantasy", 10766: "Soap",
    10767: "Talk", 10768: "War & Politics"
}

def get_real_genres(genre_ids: list):
    "Translates numeric genre IDs from API into readable text strings"
    genres = [GENRE_MAP.get(gid) for gid in genre_ids if gid in GENRE_MAP]
    return genres if genres else ["Unknown Genre"]

def get_cast(media_id: int, media_type: str):
    "Fetches the top 3 actors for a given movie or series"
    endpoint = f"{BASE_URL}/{media_type}/{media_id}/credits"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()
        cast_data = response.json().get("cast", [])
        top_actors = [person.get("name", "Unknown") for person in cast_data[:3]]
        return ", ".join(top_actors) if top_actors else "Unknown"
    except Exception:
        return "Unknown"

def get_tv_seasons(media_id: int):
    "Fetches the exact number of seasons for a TV show"
    endpoint = f"{BASE_URL}/tv/{media_id}"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("number_of_seasons", 1)
    except Exception:
        return 1

def get_movie_runtime(movie_id: int):
    "Makes a secondary API call to fetch the exact movie duration"
    endpoint = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    try:
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("runtime", 120)
    except Exception:
        return 120

def search_media(query: str):
    "Searches for movies or TV series using TMDb multi-search API"
    endpoint = f"{BASE_URL}/search/multi"
    params = {"api_key": API_KEY, "query": query, "language": "en-US", "page": 1}

    try:
        # Added timeout to prevent the bot from hanging during bad network conditions
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Filter out people and keep only movies and TV shows
        results = [res for res in data.get("results", []) if res.get("media_type") in ["movie", "tv"]]
        if not results:
            return None

        media_data = results[0]
        media_type = media_data.get("media_type")
        media_id = media_data.get("id")

        rating = media_data.get("vote_average", 0.0)
        overview = media_data.get("overview", "No description available.")
        poster_path = media_data.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

        genre_ids = media_data.get("genre_ids", [])
        actual_genres = get_real_genres(genre_ids)
        cast_str = get_cast(media_id, media_type)

        if media_type == "movie":
            title = media_data.get("title", "Unknown Title")
            release_date = media_data.get("release_date", "Unknown")
            release_year = release_date[:4] if release_date else "Unknown"

            # Dynamic runtime fetching
            runtime = get_movie_runtime(media_id)

            return Movie(
                title=title, rating=rating, overview=overview,
                genres=actual_genres, release_year=release_year,
                duration=runtime, poster_url=poster_url, cast=cast_str
            )

        elif media_type == "tv":
            title = media_data.get("name", "Unknown Title")
            first_air_date = media_data.get("first_air_date", "Unknown")
            release_year = first_air_date[:4] if first_air_date else "Unknown"
            seasons_count = get_tv_seasons(media_id)

            return Series(
                title=title, rating=rating, overview=overview,
                genres=actual_genres, seasons=seasons_count,
                release_year=release_year, poster_url=poster_url, cast=cast_str
            )

    except requests.exceptions.RequestException as e:
        print(f"Network error during API call: {e}")
        return None



def get_random_recommendation():
    "Fetches a random movie or TV series from the top 2000 popular items"
    media_type = random.choice(["movie", "tv"])
    random_page = random.randint(1, 100)

    endpoint = f"{BASE_URL}/discover/{media_type}"
    params = {"api_key": API_KEY, "page": random_page, "sort_by": "popularity.desc"}

    try:
        response = requests.get(endpoint, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results: return None

        random_media = random.choice(results)
        media_id = random_media.get("id")

        rating = random_media.get("vote_average", 0.0)
        overview = random_media.get("overview", "No description available.")
        poster_path = random_media.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""

        genre_ids = random_media.get("genre_ids", [])
        actual_genres = get_real_genres(genre_ids)
        cast_str = get_cast(media_id, media_type)

        if media_type == "movie":
            title = random_media.get("title", "Unknown Title")
            release_date = random_media.get("release_date", "Unknown")
            release_year = release_date[:4] if release_date else "Unknown"

            runtime = get_movie_runtime(media_id)

            return Movie(
                title=title, rating=rating, overview=overview,
                genres=actual_genres, release_year=release_year,
                duration=runtime, poster_url=poster_url, cast=cast_str
            )

        elif media_type == "tv":
            title = random_media.get("name", "Unknown Title")
            first_air_date = random_media.get("first_air_date", "Unknown")
            release_year = first_air_date[:4] if first_air_date else "Unknown"
            seasons_count = get_tv_seasons(media_id)

            return Series(
                title=title, rating=rating, overview=overview,
                genres=actual_genres, seasons=seasons_count,
                release_year=release_year, poster_url=poster_url, cast=cast_str
            )

    except requests.exceptions.RequestException as e:
        print(f"Error fetching random media: {e}")
        return None