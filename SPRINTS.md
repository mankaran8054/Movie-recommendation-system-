
---

# `SPRINTS.md`

For your sprint file, I recommend documenting what was **planned, implemented, and completed** rather than making it sound like you're still developing the project.

```markdown
# Movie Recommendation System - Sprint Plan

## Project Overview

The Movie Recommendation System is a content-based movie recommendation application developed using Python and Streamlit.

The system uses TF-IDF and Cosine Similarity to recommend movies and uses user history and favorite movies to provide personalized recommendations.

The project also integrates the OMDb API to retrieve movie posters.

---

## Sprint 1 - Project Setup and Dataset

### Objectives

- Set up the Python project
- Select and prepare the movie dataset
- Install required libraries
- Create the basic project structure

### Tasks

- Create the project directory
- Add the movie dataset
- Install Python dependencies
- Set up Streamlit
- Create the initial application files
- Load the movie dataset using Pandas

### Status

Completed

---

## Sprint 2 - Movie Data Processing

### Objectives

- Prepare movie data for recommendation
- Extract useful movie features

### Tasks

- Load movie data
- Clean movie information
- Process movie genres
- Process movie descriptions
- Combine relevant movie features
- Prepare data for machine learning

### Status

Completed

---

## Sprint 3 - Recommendation Engine

### Objectives

- Build the content-based recommendation system

### Tasks

- Implement TF-IDF vectorization
- Convert movie features into numerical vectors
- Calculate Cosine Similarity
- Find similar movies
- Rank movies according to similarity
- Return the top recommended movies

### Status

Completed

---

## Sprint 4 - Personalization

### Objectives

- Make recommendations specific to individual users

### Tasks

- Create user profiles
- Store user information
- Track watch history
- Track favorite movies
- Use watch history in recommendations
- Use favorite movies in recommendations
- Implement weighted personalization
- Remove already watched movies
- Display the top 5 personalized recommendations

### Recommendation Weights

- Selected movie: 50%
- Watch history: 30%
- Favorite movies: 20%

### Status

Completed

---

## Sprint 5 - Database Integration

### Objectives

- Store user-related information permanently

### Tasks

- Set up SQLite database
- Create user records
- Store movie watch history
- Store favorite movies
- Retrieve user history
- Retrieve favorite movies
- Remove favorite movies
- Calculate user statistics

### Status

Completed

---

## Sprint 6 - Web Interface

### Objectives

- Build an interactive user interface using Streamlit

### Tasks

- Create sidebar navigation
- Create user profile section
- Add movie search
- Add movie selection
- Add recommendation button
- Display recommended movies
- Add movie details section
- Add favorite controls
- Add watch history controls
- Add logout functionality

### Status

Completed

---

## Sprint 7 - Movie Poster API Integration

### Objectives

- Add movie posters to the application

### Initial Approach

The project initially used the TMDB API for movie posters.

The TMDB API could not be reliably accessed from the development environment, so an alternative API was selected.

### Final Approach

The OMDb API was integrated into the project.

### Tasks

- Obtain an OMDb API key
- Store the API key using Streamlit secrets
- Create the OMDb API module
- Search movies using their titles
- Retrieve poster URLs
- Display posters for recommended movies
- Display posters in movie details
- Display posters in Favorites
- Display posters in Watch History
- Add IMDb links

### Status

Completed

---

## Sprint 8 - Analytics

### Objectives

- Provide useful statistics about the movie dataset and user activity

### Tasks

- Display total number of movies
- Display movies watched
- Display favorite movies
- Calculate average movie rating
- Create movies-by-genre chart
- Create rating distribution chart
- Create recommendation similarity chart

### Status

Completed

---

## Sprint 9 - Security and Optimization

### Objectives

- Protect API credentials
- Improve application performance

### Tasks

- Store OMDb API key in Streamlit secrets
- Add secrets.toml to .gitignore
- Prevent API credentials from being committed to GitHub
- Implement Streamlit caching for OMDb requests
- Cache movie data
- Cache the recommendation model

### Status

Completed

---

## Sprint 10 - Testing and Final Integration

### Objectives

- Test the complete application
- Fix integration problems
- Prepare the final project

### Tasks

- Test user registration
- Test movie search
- Test movie selection
- Test recommendations
- Test poster retrieval
- Test movie details
- Test favorites
- Test watch history
- Test analytics
- Test logout
- Test API integration
- Verify API key protection
- Verify application startup

### Status

Completed

---

# Final Project Status

The Movie Recommendation System has been completed.

The final application provides:

- User profiles
- Movie search
- Content-based recommendations
- TF-IDF
- Cosine Similarity
- Personalized recommendations
- Watch history
- Favorites
- Movie details
- OMDb poster integration
- IMDb links
- Analytics
- SQLite database
- Streamlit interface
- API key protection
- Application caching

## Final Technology Stack

Python  
Streamlit  
Pandas  
Scikit-learn  
SQLite  
Requests  
OMDb API  
HTML/CSS

## Project Completion

All planned development sprints have been completed successfully.
