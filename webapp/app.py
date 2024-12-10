import streamlit as st
import pandas as pd
import requests
import os

port = int(os.environ.get("PORT", 8501))  # Default port for Streamlit is 8501


# Function to fetch the poster and movie URL
def fetch_poster_and_url(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4dba8e5601303fa9cabfedfda01a11b0")
    data = response.json()
    poster_url = "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    movie_url = data.get('homepage', '#')  # Fallback to "#" if homepage is not available
    return poster_url, movie_url

# Function to get recommendations
def recommend(movie_name):
    # Get the index of the movie in the dataframe
    movie_index = movies[movies['title'] == movie_name].index[0]
    # get a singular row out of the similarity matrix 
    movie_similarities = similarity_matrix[movie_index]
    top5_movies = sorted(list(enumerate(movie_similarities)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_urls = []

    for i in top5_movies:        
        # Return movie id using index number 
        movie_id = movies.iloc[i[0]]['movie_id']
        poster_url, movie_url = fetch_poster_and_url(movie_id)
        recommended_movies_posters.append(poster_url)
        recommended_movies_urls.append(movie_url)
        # get the title of the movie
        # reason for i[0] is that i is a tuple and the first element is the index of the movie
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters, recommended_movies_urls

# Custom CSS for styling
st.markdown("""
    <style>
        /* Background styling */
        .stApp {
            background-color: #1a1a1a;
        }

        /* Header styling */
        .header {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #ff4b4b;
            margin-bottom: 20px;
        }

        /* Recommendation title */
        .recommendation-title {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin: 20px 0;
        }

        /* Movie poster hover effect */
        .movie-poster:hover {
            transform: scale(1.05);
            transition: transform 0.2s ease-in-out;
            border: 2px solid #ff4b4b;
        }

        /* Footer styling */
        .footer {
            text-align: center;
            font-size: 14px;
            color: #ff4b4b;
            margin-top: 40px;
        }
        .footer a {
            color: #ff4b4b;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown("<div class='header'>🎬 Movie Recommender</div>", unsafe_allow_html=True)

# Read parquet files
similarity_matrix = pd.read_parquet("similarity_matrix.parquet")
movies = pd.read_parquet("movies.parquet")

# Movie selection dropdown
selected_movie_name = st.selectbox(
    "Enter the movie you would like to get recommendations for:",
    movies["title"].values,
)

if st.button("Get Recommendations"):

    with st.spinner("Fetching recommendations..."):
        movies_5, posters_5, urls_5 = recommend(selected_movie_name)

    st.markdown("<div class='recommendation-title'>You might also enjoy:</div>", unsafe_allow_html=True)

    # Display movies in a horizontal layout
    cols = st.columns(len(movies_5))
    for col, movie, poster, url in zip(cols, movies_5, posters_5, urls_5):
        with col:
            st.markdown(
                f"<a href='{url}' target='_blank'><img class='movie-poster' src='{poster}' style='width:100%; border-radius:10px;'></a>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<a href='{url}' target='_blank' style='text-decoration:none; color:#ff4b4b; text-align:center; display:block;'>{movie}</a>",
                unsafe_allow_html=True,
            )

# Footer
st.markdown("""
    <div class="footer">
        Developed by <a href="https://github.com/raghavahuja2801" target="_blank">Raghav Ahuja</a> & 
         <a href="https://github.com/Ozayzay" target="_blank">Ozafa Mahmood</a> 
    </div>
""", unsafe_allow_html=True)
