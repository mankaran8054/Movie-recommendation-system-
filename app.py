import pandas as pd
import streamlit as st

from recommender import (
    load_movies,
    prepare_movies,
    create_model,
    personalized_recommendations
)

from database import (
    initialize_database,
    get_user_by_email,
    create_user,
    add_history,
    get_history,
    get_unique_history,
    add_favorite,
    remove_favorite,
    is_favorite,
    get_favorites,
    get_user_stats
)

from omdb import search_movie, get_poster_url


st.set_page_config(
    page_title="Movie Recommender",

    layout="wide"
)


def load_css():
    with open("style.css", "r") as file:
        st.markdown(
            f"<style>{file.read()}</style>",
            unsafe_allow_html=True
        )


load_css()
initialize_database()


@st.cache_data
def get_movies():
    movies = load_movies()
    return prepare_movies(movies)


@st.cache_resource
def get_model(movies):
    return create_model(movies)


movies = get_movies()

vectorizer, tfidf_matrix = get_model(
    movies
)


if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "signin"

if "page" not in st.session_state:
    st.session_state.page = "Recommendations"

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "selected_movie" not in st.session_state:
    st.session_state.selected_movie = None

if "detail_movie" not in st.session_state:
    st.session_state.detail_movie = None

# Authentication

if st.session_state.user_id is None:

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:

        st.html("""
        <div class="auth-brand">
            
            <div class="auth-brand-title">Movie Recommender</div>
            <div class="auth-brand-text">
                Discover movies you'll love based on your taste.
            </div>

            <div class="auth-features">
                <div class="auth-feature">
                    
                    <div>
                        <strong>Personalized Recommendations</strong>
                        <small>Get movie suggestions based on your interests.</small>
                    </div>
                </div>

                <div class="auth-feature">
                    
                    <div>
                        <strong>Save Your Favorites</strong>
                        <small>Keep track of movies you never want to forget.</small>
                    </div>
                </div>

                <div class="auth-feature">
                    
                    <div>
                        <strong>Track Your History</strong>
                        <small>Build your personal movie watching profile.</small>
                    </div>
                </div>

                <div class="auth-feature">
                    
                    <div>
                        <strong>View Your Analytics</strong>
                        <small>Explore your movie activity and preferences.</small>
                    </div>
                </div>
            </div>
        </div>
        """)

    with right:

        st.html("""
        <div class="auth-panel">
            <div class="auth-panel-label">ACCOUNT</div>
            <div class="auth-panel-title">Welcome to Movie Recommender </div>
            <div class="auth-panel-subtitle">
                Sign in to continue or create a new profile.
            </div>
        </div>
        """)

        signin_col, signup_col = st.columns(2)

        with signin_col:

            if st.button(
                "Sign In",
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.auth_page == "signin"
                    else "secondary"
                ),
                key="auth_signin_tab"
            ):
                st.session_state.auth_page = "signin"
                st.rerun()

        with signup_col:

            if st.button(
                "Sign Up",
                use_container_width=True,
                type=(
                    "primary"
                    if st.session_state.auth_page == "signup"
                    else "secondary"
                ),
                key="auth_signup_tab"
            ):
                st.session_state.auth_page = "signup"
                st.rerun()

        if st.session_state.auth_page == "signin":

            st.html("""
            <div class="auth-form-title">Welcome Back</div>
            <div class="auth-form-subtitle">
                Sign in to continue discovering movies.
            </div>
            """)

            email = st.text_input(
                "Email",
                placeholder="Enter your registered email",
                key="signin_email"
            )

            if st.button(
                "Sign In",
                use_container_width=True,
                type="primary",
                key="signin_button"
            ):

                email = email.strip().lower()

                if not email:
                    st.warning("Please enter your email.")

                else:
                    user = get_user_by_email(email)

                    if user:
                        st.session_state.user_id = user[0]
                        st.session_state.user_name = user[1]
                        st.session_state.user_email = user[2]
                        st.rerun()

                    else:
                        st.error(
                            "No account found with this email. "
                            "Please sign up first."
                        )

        else:

            st.html("""
            <div class="auth-form-title">Create Your Profile</div>
            <div class="auth-form-subtitle">
                Join Movie Recommender and discover your next favorite.
            </div>
            """)

            name = st.text_input(
                "Name",
                placeholder="Enter your name",
                key="signup_name"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email",
                key="signup_email"
            )

            if st.button(
                "  Create Account",
                use_container_width=True,
                type="primary",
                key="signup_button"
            ):

                name = name.strip()
                email = email.strip().lower()

                if not name or not email:
                    st.warning("Please enter your name and email.")

                else:
                    existing_user = get_user_by_email(email)

                    if existing_user:
                        st.error(
                            "An account with this email already exists. "
                            "Please sign in."
                        )

                    else:
                        user = create_user(name, email)

                        st.session_state.user_id = user[0]
                        st.session_state.user_name = user[1]
                        st.session_state.user_email = user[2]

                        st.success("Account created successfully.")
                        st.rerun()

        st.html("""
        <div class="auth-note">
            🔒 Your profile, favorites and watch history are securely stored
            in the application database.
        </div>
        """)

    st.stop()
# Sidebar

with st.sidebar:

    st.title("Movie")
    st.caption("Recommender")

    st.divider()

    st.html(f"""
    <div class="profile-box">
        <h3>{st.session_state.user_name}</h3>
        <p>{st.session_state.user_email}</p>
        <p class="small-text">Personalized recommendations</p>
    </div>
    """)

    st.divider()

    watched_count, favorite_count = (
        get_user_stats(
            st.session_state.user_id
        )
    )

    st.caption(
        f"Movies watched: {watched_count}"
    )

    st.caption(
        f"Favorites: {favorite_count}"
    )

    st.divider()

    if st.button(
        "Logout",
        use_container_width=True,
        key="logout_button"
    ):

        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None
        st.session_state.recommendations = None
        st.session_state.selected_movie = None
        st.session_state.detail_movie = None
        st.session_state.page = "Recommendations"

        st.rerun()


# Top navigation

st.html("""
<div class="top-title">
    Movie Recommendation System
</div>
<div class="top-subtitle">
    Discover movies based on what you like and watch.
</div>
""")

nav1, nav2, nav3, nav4, nav5 = st.columns(5)


with nav1:

    if st.button(
        "Recommendations",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Recommendations"
            else "secondary"
        ),
        key="nav_recommendations"
    ):

        st.session_state.page = "Recommendations"
        st.rerun()


with nav2:

    if st.button(
        "Favorites",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Favorites"
            else "secondary"
        ),
        key="nav_favorites"
    ):

        st.session_state.page = "Favorites"
        st.rerun()


with nav3:

    if st.button(
        "History",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "History"
            else "secondary"
        ),
        key="nav_history"
    ):

        st.session_state.page = "History"
        st.rerun()


with nav4:

    if st.button(
        "Analytics",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "Analytics"
            else "secondary"
        ),
        key="nav_analytics"
    ):

        st.session_state.page = "Analytics"
        st.rerun()


with nav5:

    if st.button(
        "How It Works",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page == "How It Works"
            else "secondary"
        ),
        key="nav_how_it_works"
    ):

        st.session_state.page = "How It Works"
        st.rerun()


st.divider()


# Recommendations

if st.session_state.page == "Recommendations":

    history = get_unique_history(
        st.session_state.user_id
    )

    favorites = get_favorites(
        st.session_state.user_id
    )

    history_ids = [
        movie[0]
        for movie in history
    ]

    favorite_ids = [
        movie[0]
        for movie in favorites
    ]

    st.title(
        "Find Your Next Favorite Movie"
    )

    st.write(
        "Discover movies based on what you "
        "like and watch."
    )

    if history_ids or favorite_ids:

        st.success(
            "Your recommendations are personalized "
            "using your current selection, watch history "
            "and favorites."
        )

    else:

        st.info(
            "You are a new user. Select a movie you like "
            "to get your first recommendations."
        )

    st.divider()

    search_text = st.text_input(
        "Search movies",
        placeholder="Search for a movie..."
    )

    filtered_movies = movies.copy()

    if search_text:

        filtered_movies = filtered_movies[
            filtered_movies["title"].str.contains(
                search_text,
                case=False,
                na=False
            )
        ]

    if filtered_movies.empty:

        st.warning(
            "No movies found."
        )

    else:

        selected_movie = st.selectbox(
            "Select a movie",
            filtered_movies["title"].tolist()
        )

        selected_row = movies[
            movies["title"] == selected_movie
        ]

        selected_movie_id = int(
            selected_row.iloc[0]["id"]
        )

        if st.button(
            "✨ Recommend Movies",
            type="primary",
            use_container_width=True,
            key="recommend_button"
        ):

            recommendations = (
                personalized_recommendations(
                    selected_movie_id,
                    history_ids,
                    favorite_ids,
                    movies,
                    tfidf_matrix,
                    5
                )
            )

            st.session_state.recommendations = (
                recommendations
            )

            st.session_state.selected_movie = (
                selected_movie
            )


    # Recommendation results

    if (
        st.session_state.recommendations
        is not None
        and not st.session_state.recommendations.empty
    ):

        recommendations = (
            st.session_state.recommendations
        )

        st.divider()

        st.subheader(
            "Top 5 Recommended Movies"
        )

        st.caption(
            f"Based on: "
            f"{st.session_state.selected_movie}"
        )

        columns = st.columns(5)

        for index, row in recommendations.iterrows():

            with columns[index]:

                movie_id = int(
                    row["id"]
                )

                movie_title = row["title"]

                similarity = (
                    row["similarity"] * 100
                )

                omdb_movie = search_movie(
                    movie_title
                )

                poster_url = get_poster_url(
                    omdb_movie
                )

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No poster available"
                    )

                st.html(f"""
                <div class="movie-title">
                    {movie_title}
                </div>
                """)

                year = str(
                    row["release_date"]
                )[:4]

                if year:

                    st.caption(
                        year
                    )

                st.markdown(
                    f"⭐ {row['vote_average']:.1f}/10"
                )

                st.html(f"""
                <span class="match-badge">
                    {similarity:.1f}% Match
                </span>
                """)

                st.caption(
                    row["genre_text"]
                )

                if st.button(
                    "View Details",
                    key=f"details_{movie_id}",
                    use_container_width=True
                ):

                    st.session_state.detail_movie = (
                        movie_title
                    )

                    st.rerun()


    # Movie details

    if st.session_state.detail_movie:

        detail_title = (
            st.session_state.detail_movie
        )

        rows = movies[
            movies["title"] == detail_title
        ]

        if not rows.empty:

            movie = rows.iloc[0]

            omdb_movie = search_movie(
                detail_title
            )

            st.divider()

            st.subheader(
                "Movie Details"
            )

            col1, col2 = st.columns(
                [1, 2]
            )

            with col1:

                poster_url = get_poster_url(
                    omdb_movie
                )

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No poster available"
                    )

            with col2:

                st.header(
                    detail_title
                )

                st.write(
                    f"⭐ Rating: "
                    f"{movie['vote_average']:.1f}/10"
                )

                st.write(
                    f"Release Year: "
                    f"{str(movie['release_date'])[:4]}"
                )

                st.write(
                    f"Genres: "
                    f"{movie['genre_text']}"
                )

                st.subheader(
                    "Overview"
                )

                st.write(
                    movie["overview"]
                    if movie["overview"]
                    else "No overview available."
                )

                movie_id = int(
                    movie["id"]
                )

                st.divider()

                if is_favorite(
                    st.session_state.user_id,
                    movie_id
                ):

                    if st.button(
                        "Remove from Favorites",
                        key="remove_favorite"
                    ):

                        remove_favorite(
                            st.session_state.user_id,
                            movie_id
                        )

                        st.session_state.recommendations = None

                        st.success(
                            "Removed from favorites."
                        )

                        st.rerun()

                else:

                    if st.button(
                        "Add to Favorites",
                        key="add_favorite"
                    ):

                        add_favorite(
                            st.session_state.user_id,
                            movie_id,
                            movie["title"]
                        )

                        st.session_state.recommendations = None

                        st.success(
                            "Added to favorites."
                        )

                        st.rerun()

                if st.button(
                    "Mark as Watched",
                    key="mark_watched"
                ):

                    add_history(
                        st.session_state.user_id,
                        movie_id,
                        movie["title"]
                    )

                    st.session_state.recommendations = None

                    st.success(
                        "Added to watch history."
                    )

                    st.rerun()

                if (
                    omdb_movie
                    and "imdbID" in omdb_movie
                ):

                    imdb_id = omdb_movie["imdbID"]

                    st.link_button(
                        "View on IMDb",
                        f"https://www.imdb.com/title/{imdb_id}/"
                    )


    # Similarity chart

    if (
        st.session_state.recommendations
        is not None
        and not st.session_state.recommendations.empty
    ):

        st.divider()

        st.subheader(
            "Similarity Score"
        )

        chart_data = (
            st.session_state.recommendations[
                [
                    "title",
                    "similarity"
                ]
            ]
            .copy()
        )

        chart_data["similarity"] = (
            chart_data["similarity"] * 100
        )

        chart_data = chart_data.set_index(
            "title"
        )

        st.bar_chart(
            chart_data
        )


# Favorites

elif st.session_state.page == "Favorites":

    st.title(
        "Your Favorites"
    )

    favorites = get_favorites(
        st.session_state.user_id
    )

    if not favorites:

        st.info(
            "You haven't added any favorite movies yet."
        )

    else:

        for movie_id, title, added_at in favorites:

            rows = movies[
                movies["id"] == movie_id
            ]

            if rows.empty:
                continue

            movie = rows.iloc[0]

            col1, col2 = st.columns(
                [1, 4]
            )

            with col1:

                omdb_movie = search_movie(
                    title
                )

                poster_url = get_poster_url(
                    omdb_movie
                )

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No poster available"
                    )

            with col2:

                st.subheader(
                    title
                )

                st.write(
                    f"⭐ "
                    f"{movie['vote_average']:.1f}/10"
                )

                st.write(
                    movie["genre_text"]
                )

                if st.button(
                    "Remove",
                    key=f"remove_{movie_id}"
                ):

                    remove_favorite(
                        st.session_state.user_id,
                        movie_id
                    )

                    st.session_state.recommendations = None

                    st.rerun()

            st.divider()


# History

elif st.session_state.page == "History":

    st.title(
        "Your Watch History"
    )

    history = get_history(
        st.session_state.user_id,
        limit=30
    )

    if not history:

        st.info(
            "Your watch history is empty."
        )

    else:

        for movie_id, title, viewed_at in history:

            rows = movies[
                movies["id"] == movie_id
            ]

            if rows.empty:
                continue

            movie = rows.iloc[0]

            col1, col2 = st.columns(
                [1, 5]
            )

            with col1:

                omdb_movie = search_movie(
                    title
                )

                poster_url = get_poster_url(
                    omdb_movie
                )

                if poster_url:

                    st.image(
                        poster_url,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No poster available"
                    )

            with col2:

                st.subheader(
                    title
                )

                st.caption(
                    f"Watched: {viewed_at}"
                )

                st.write(
                    f"⭐ "
                    f"{movie['vote_average']:.1f}/10"
                )

                st.write(
                    movie["genre_text"]
                )

            st.divider()


# Analytics

elif st.session_state.page == "Analytics":

    st.title(
        "Analytics"
    )

    watched_count, favorite_count = (
        get_user_stats(
            st.session_state.user_id
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Movies",
            f"{len(movies):,}"
        )

    with col2:

        st.metric(
            "Movies Watched",
            watched_count
        )

    with col3:

        st.metric(
            "Favorites",
            favorite_count
        )

    with col4:

        st.metric(
            "Average Rating",
            f"{movies['vote_average'].mean():.1f}"
        )

    st.divider()

    st.subheader(
        "Movies by Genre"
    )

    genre_counter = {}

    for genre_string in movies["genre_text"]:

        if genre_string:

            for genre in genre_string.split(", "):

                genre_counter[genre] = (
                    genre_counter.get(
                        genre,
                        0
                    ) + 1
                )

    genre_data = pd.DataFrame(
        list(
            genre_counter.items()
        ),
        columns=[
            "Genre",
            "Movies"
        ]
    )

    genre_data = genre_data.sort_values(
        "Movies",
        ascending=False
    )

    st.bar_chart(
        genre_data.set_index(
            "Genre"
        )
    )

    st.divider()

    st.subheader(
        "Rating Distribution"
    )

    rating_bins = pd.cut(
        movies["vote_average"],
        bins=[
            0,
            2,
            4,
            6,
            8,
            10
        ],
        labels=[
            "0-2",
            "2-4",
            "4-6",
            "6-8",
            "8-10"
        ],
        include_lowest=True
    )

    rating_counts = (
        rating_bins
        .value_counts()
        .sort_index()
    )

    st.bar_chart(
        rating_counts
    )


# How It Works

elif st.session_state.page == "How It Works":

    st.title(
        "How It Works"
    )

    st.subheader(
        "1. User Profile"
    )

    st.write(
        "The user creates an account using a name and email. "
        "The email identifies the user in SQLite."
    )

    st.subheader(
        "2. Movie Selection"
    )

    st.write(
        "The user searches for and selects a movie "
        "that they are interested in."
    )

    st.subheader(
        "3. Movie Features"
    )

    st.write(
        "Genres and movie descriptions are combined "
        "to create movie features."
    )

    st.subheader(
        "4. TF-IDF"
    )

    st.write(
        "TF-IDF converts the movie text into "
        "numerical vectors."
    )

    st.subheader(
        "5. Cosine Similarity"
    )

    st.write(
        "Cosine similarity measures how similar "
        "movies are to each other."
    )

    st.subheader(
        "6. Personalization"
    )

    st.write(
        "The recommendation engine considers the "
        "currently selected movie, the user's watch "
        "history and the user's favorite movies."
    )

    st.subheader(
        "7. Weighted Recommendation"
    )

    st.write(
        "The current movie contributes 50%, watch "
        "history contributes 30% and favorites "
        "contribute 20%."
    )

    st.subheader(
        "8. Final Ranking"
    )

    st.write(
        "Already watched movies are removed. The "
        "remaining movies are ranked and the top "
        "five are displayed."
    )

    st.divider()

    st.info(
        "New user: Selected movie → Similar movies\n\n"
        "Returning user: Selected movie + History + "
        "Favorites → Personalized movies"
    )