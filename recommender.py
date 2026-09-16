import ast
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_movies():
    # Load the movie dataset.
    movies = pd.read_csv(
        "tmdb_5000_movies.csv"
    )

    movies = movies[
        [
            "id",
            "title",
            "genres",
            "overview",
            "release_date",
            "vote_average",
            "vote_count",
            "popularity"
        ]
    ].copy()

    movies["genres"] = movies["genres"].fillna("")
    movies["overview"] = movies["overview"].fillna("")
    movies["release_date"] = movies["release_date"].fillna("")

    movies["vote_average"] = pd.to_numeric(
        movies["vote_average"],
        errors="coerce"
    ).fillna(0)

    movies["vote_count"] = pd.to_numeric(
        movies["vote_count"],
        errors="coerce"
    ).fillna(0)

    movies["popularity"] = pd.to_numeric(
        movies["popularity"],
        errors="coerce"
    ).fillna(0)

    return movies


def extract_genres(text):
    # Extract genre names from the JSON-like string.
    try:
        genre_list = ast.literal_eval(text)

        return ", ".join(
            genre["name"]
            for genre in genre_list
        )

    except:
        return ""


def prepare_movies(movies):
    # Create the text used by TF-IDF.
    movies["genre_text"] = movies[
        "genres"
    ].apply(extract_genres)

    movies["tags"] = (
        movies["genre_text"]
        .str.replace(",", " ", regex=False)
        + " "
        + movies["overview"]
    )

    return movies


def create_model(movies):
    # Convert movie text into TF-IDF vectors.
    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        movies["tags"]
    )

    return vectorizer, tfidf_matrix


def get_movie_index(movie_id, movies):
    # Find the dataframe index of a movie.
    matches = movies[
        movies["id"] == movie_id
    ]

    if matches.empty:
        return None

    return matches.index[0]


def calculate_similarity(index, tfidf_matrix):
    # Calculate similarity between one movie and all movies.
    return cosine_similarity(
        tfidf_matrix[index],
        tfidf_matrix
    ).flatten()


def personalized_recommendations(
    selected_movie_id,
    history_movie_ids,
    favorite_movie_ids,
    movies,
    tfidf_matrix,
    number_of_movies=5
):
    # Generate recommendations using current movie and user data.

    total_scores = [0.0] * len(movies)

    selected_index = get_movie_index(
        selected_movie_id,
        movies
    )

    history_indices = []
    favorite_indices = []

    for movie_id in history_movie_ids:

        index = get_movie_index(
            movie_id,
            movies
        )

        if index is not None:
            history_indices.append(index)

    for movie_id in favorite_movie_ids:

        index = get_movie_index(
            movie_id,
            movies
        )

        if index is not None:
            favorite_indices.append(index)

    if selected_index is not None:

        selected_scores = calculate_similarity(
            selected_index,
            tfidf_matrix
        )

        total_scores = [
            score * 0.50
            for score in selected_scores
        ]

    if history_indices:

        history_scores = [
            0.0
        ] * len(movies)

        for index in history_indices:

            scores = calculate_similarity(
                index,
                tfidf_matrix
            )

            history_scores = [
                old + new
                for old, new in zip(
                    history_scores,
                    scores
                )
            ]

        history_scores = [
            score / len(history_indices)
            for score in history_scores
        ]

        total_scores = [
            old + (new * 0.30)
            for old, new in zip(
                total_scores,
                history_scores
            )
        ]

    if favorite_indices:

        favorite_scores = [
            0.0
        ] * len(movies)

        for index in favorite_indices:

            scores = calculate_similarity(
                index,
                tfidf_matrix
            )

            favorite_scores = [
                old + new
                for old, new in zip(
                    favorite_scores,
                    scores
                )
            ]

        favorite_scores = [
            score / len(favorite_indices)
            for score in favorite_scores
        ]

        total_scores = [
            old + (new * 0.20)
            for old, new in zip(
                total_scores,
                favorite_scores
            )
        ]

    excluded_ids = set(
        history_movie_ids
    )

    if selected_movie_id is not None:
        excluded_ids.add(
            selected_movie_id
        )

    sorted_indices = sorted(
        range(len(movies)),
        key=lambda index:
        total_scores[index],
        reverse=True
    )

    final_indices = []

    for index in sorted_indices:

        movie_id = movies.iloc[index]["id"]

        if movie_id not in excluded_ids:

            final_indices.append(index)

        if len(final_indices) >= number_of_movies:

            break

    recommendations = movies.loc[
        final_indices
    ].copy()

    recommendations["similarity"] = [
        total_scores[index]
        for index in final_indices
    ]

    return recommendations.reset_index(
        drop=True
    )