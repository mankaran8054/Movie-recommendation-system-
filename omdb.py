import requests
import streamlit as st


try:
    API_KEY = st.secrets["OMDB_API_KEY"]

except Exception:
    API_KEY = ""


BASE_URL = "https://www.omdbapi.com/"


@st.cache_data(ttl=3600)
def search_movie(title):
    """
    Search OMDb for a movie by title.
    """

    if not API_KEY:
        return {
            "error": "OMDb API key not found."
        }

    try:

        response = requests.get(
            BASE_URL,
            params={
                "apikey": API_KEY,
                "t": title
            },
            timeout=10
        )

        if response.status_code != 200:

            return {
                "error": (
                    f"OMDb API error: "
                    f"{response.status_code}"
                )
            }

        data = response.json()

        if data.get("Response") != "True":

            return {
                "error": (
                    f"No OMDb result found for "
                    f"'{title}'."
                )
            }

        return data

    except requests.exceptions.RequestException as error:

        return {
            "error": f"OMDb connection error: {error}"
        }


def get_poster_url(movie):
    """
    Get the poster URL from an OMDb movie result.
    """

    if not movie:
        return None

    poster_url = movie.get("Poster")

    if not poster_url or poster_url == "N/A":
        return None

    return poster_url