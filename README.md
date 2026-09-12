# Movie Recommendation System

A personalized movie recommendation system built using Python, Streamlit, TF-IDF, Cosine Similarity, SQLite, and the OMDb API.

The system recommends movies based on the movie selected by the user and, for returning users, also considers their watch history and favorite movies.

## Features

- User profile using name and email
- Movie search and selection
- Content-based movie recommendations
- TF-IDF based movie feature extraction
- Cosine similarity for finding similar movies
- Personalized recommendations
- Watch history tracking
- Favorite movies management
- Movie details and overview
- Movie posters fetched using the OMDb API
- IMDb links for movie details
- Recommendation match percentage
- Similarity score visualization
- Genre-based analytics
- Rating distribution analytics
- SQLite database for storing user data, favorites, and history
- Streamlit web interface

## How the Recommendation System Works

The system uses content-based filtering.

Movie information such as genres and descriptions is combined to create text-based features.

TF-IDF converts these text features into numerical vectors.

Cosine similarity is then used to measure the similarity between movies.

For returning users, the system also considers their previous watch history and favorite movies.

The recommendation system uses the following weights:

- Selected movie: 50%
- Watch history: 30%
- Favorite movies: 20%

Movies that have already been watched are removed from the final results.

The system then ranks the remaining movies and displays the top 5 recommendations.

## Recommendation Flow

New user:

Selected Movie
→ Movie Features
→ TF-IDF
→ Cosine Similarity
→ Similar Movies
→ Top 5 Recommendations

Returning user:

Selected Movie
+ Watch History
+ Favorite Movies
→ Personalized Recommendation
→ Ranking
→ Top 5 Recommendations

## Movie Posters

Movie posters are fetched using the OMDb API.

The system searches OMDb using the movie title and receives the poster URL.

The poster is then displayed in the Streamlit application.

The OMDb API key is stored securely in Streamlit secrets and is not included in the source code.

## User Management

Users enter their name and email through the sidebar.

The email is used as a unique identifier for the user's movie profile.

User information is stored in a SQLite database.

Returning users can access their existing favorites and watch history.

## Favorites

Users can add movies to their favorites.

They can also remove movies from their favorites.

Favorite movies are stored in the SQLite database and are used as part of personalized recommendations.

## Watch History

Users can mark movies as watched.

The system stores the movie and viewing information in SQLite.

Watch history is used to personalize future recommendations.

Already watched movies are excluded from the recommendation results.

## Analytics

The application provides analytics including:

- Total number of movies
- Movies watched
- Favorite movies
- Average movie rating
- Movies by genre
- Rating distribution

Charts are displayed using Streamlit.

## Project Structure

```text
Movie_recommendation_sys_project/
│
├── app.py
├── recommender.py
├── database.py
├── omdb.py
├── style.css
├── requirements.txt
├── tmdb_5000_movies.csv
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
