from urllib import response
import streamlit as st 
import pandas as pd
# to hit API
import requests

def fetch_poster_and_url(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4dba8e5601303fa9cabfedfda01a11b0")
    data = response.json()
    poster_url = "http://image.tmdb.org/t/p/w500/" + data['poster_path']
    movie_url = data.get('homepage', '#')  # Get the homepage URL or fallback to "#" if not available
    return poster_url, movie_url

# Function to get recommendations
def recommend(movie_name):
    movie_index = movies[movies['title'] == movie_name ].index[0]
    # get a singular row out of the similarity matrix 
    movie_similarities = similarity_matrix[movie_index]
    top5_movies = sorted(list(enumerate(movie_similarities)),reverse=True , key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_urls = []

    for i in top5_movies:
        # Return movie id using index number 
        movie_id = movies.iloc[i[0]]['movie_id']
        # fetch poster and urls 
        poster_url, movie_url = fetch_poster_and_url(movie_id)
        recommended_movies_posters.append(poster_url)
        recommended_movies_urls.append(movie_url)        # get the title of the movie
        # reason for i[0] is that i is a tuple and the first element is the index of the movie
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies , recommended_movies_posters, recommended_movies_urls

# App title
st.title("🎬 Movie Recommender")

# Read parquet files
similarity_matrix = pd.read_parquet("similarity_matrix.parquet")
movies = pd.read_parquet("movies.parquet")

# Movie selection dropdown 
selected_movie_name = st.selectbox(
    "Enter the movie you would like to get recommendations for:",
    (movies["title"].values),
)

if st.button("Get Recommendations"):

    with st.spinner("Fetching recommendations..."):
        movies_5, posters_5, urls_5 = recommend(selected_movie_name)
    st.success("Recommendations loaded!")

    st.markdown("### You might also enjoy:")


    # Display movies with fewer columns for larger posters
    cols = st.columns([1] * len(movies_5))  # Each column will take up equal space
    for col, movie, poster, url in zip(cols, movies_5, posters_5, urls_5):
        with col:
            # Make the poster clickable
            st.markdown(
                f"<a href='{url}' target='_blank'><img src='{poster}' style='width:90%; border-radius:10px;'></a>",
                unsafe_allow_html=True,
            )
            # Make the movie title clickable
            st.markdown(
                f"<a href='{url}' target='_blank' style='text-decoration:none; color:white; text-align:center; display:block;'>{movie}</a>",
                unsafe_allow_html=True,
            )

# Footer
st.markdown("---------")
st.markdown("""
    <div class="footer">
        Developed by <a href="https://github.com/raghavahuja2801" target="_blank">Raghav Ahuja</a> & 
         <a href="https://github.com/Ozayzay" target="_blank">Ozafa Mahmood</a> 
        
    </div>
""", unsafe_allow_html=True)