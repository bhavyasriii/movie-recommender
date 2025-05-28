Movie Recommender App

A personalized Movie Recommender web app built with **Python**, **Streamlit**, and **TMDB API**.

 Features:

- Suggests 5 similar movies based on your selected title
- Animated UI with glowing effects and floating posters
- Uses content-based filtering via movie metadata and similarity matrix
- Live movie posters fetched via TMDB API

📸 Demo

![Demo Screenshot](link-to-screenshot-if-any)

Try it live: [Streamlit App](https://your-app-url.streamlit.app)

---

 How It Works:

- Movie metadata and similarity matrix loaded from `.pkl` files
- `recommend()` function finds closest movies using cosine similarity
- TMDB API used to fetch posters
- Streamlit handles interactive UI

File Structure:
.
├── app.py
├── movies.pkl
├── similarity.pkl
├── requirements.txt
├── README.md

Author: Bhavyasri Mudireddy
