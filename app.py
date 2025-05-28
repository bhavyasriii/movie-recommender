import streamlit as st
import pandas as pd
import pickle
import requests
import os
import train_model
from dotenv import load_dotenv


#Full theme: animated background, dark overlay, glowing button
st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        color: white; !important
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* ⬛ Dark transparent overlay */
    .main > div {
        background-color: rgba(0, 0, 0, 0.5) !important;
        padding: 20px;
        border-radius: 12px;
    }

    /* 🔴 Glowing red recommend button */
    .stButton > button {
        background-color: #0d0d0d;
        color: white;
        border: 2px solid red;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 16px;
        transition: 0.3s ease;
        box-shadow: 0 0 10px red;
    }

    .stButton > button:hover {
        background-color: red;
        color: black;
        box-shadow: 0 0 20px red;
        cursor: pointer;
    }

    /* 🖼 Poster spacing */
    img {
        border-radius: 10px;
        box-shadow: 0 0 10px #00000066;
    }
    </style>
""", unsafe_allow_html=True)
# 💫 Animated card entry on recommendation
st.markdown("""
    <style>
    .recommendation-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 30px;
    }

    .recommendation-container img {
        transition: transform 0.5s ease, box-shadow 0.5s ease;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        animation: float-in 1s ease forwards;
    }

    .recommendation-container img:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(255, 0, 0, 0.6);
    }

    @keyframes float-in {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)




# ✅ Check and train if model files are missing
if not os.path.exists("movies.pkl") or not os.path.exists("similarity.pkl"):
    st.warning("🔄 Model files not found. Training the model...")
    train_model.train()  # This should generate movies.pkl and similarity.pkl
    st.success("✅ Model training complete.")

# Load similarity matrix and dataframe
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

load_dotenv()
API_KEY = os.environ.get("TMDB_API_KEY")



def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    return f"https://image.tmdb.org/t/p/w500{poster_path}"

def recommend(movie):
    movie = movie.lower()
    index = movies[movies['title'].str.lower() == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in distances:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# Streamlit UI
st.title("🎬 Movie Recommender")

st.markdown("<p style='color: white; font-weight: bold;'>Choose a movie to get recommendations</p>", unsafe_allow_html=True)
selected_movie = st.selectbox("", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    
    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(
                f"<p style='text-align: center; color: white; font-size: 14px; font-weight: bold;'>{names[i]}</p>",
                unsafe_allow_html=True
            ) 


