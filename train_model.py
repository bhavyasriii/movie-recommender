import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def train():
    # Load the data
    movies = pd.read_csv("tmdb_5000_movies.csv")
    credits = pd.read_csv("tmdb_5000_credits.csv")

    # Preprocess and merge
    movies = movies[['title', 'overview', 'genres', 'keywords', 'id']]
    credits = credits.rename(columns={"movie_id": "id"})
    movies = movies.merge(credits[['id', 'cast', 'crew']], on='id')

    # Helper functions
    def convert(text):
        try:
            return [i['name'] for i in ast.literal_eval(text)]
        except:
            return []

    def get_top_cast(text):
        try:
            return [i['name'] for i in ast.literal_eval(text)][:4]
        except:
            return []

    def get_director(text):
        try:
            for i in ast.literal_eval(text):
                if i['job'] == 'Director':
                    return [i['name']]
            return []
        except:
            return []

    # Apply cleaning
    movies['genres'] = movies['genres'].apply(convert)
    movies['keywords'] = movies['keywords'].apply(convert)
    movies['cast'] = movies['cast'].apply(get_top_cast)
    movies['crew'] = movies['crew'].apply(get_director)
    movies['overview'] = movies['overview'].apply(lambda x: x.split() if isinstance(x, str) else [])

    # Combine into 'tags'
    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    new_df = movies[['id', 'title', 'tags']]
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())

    # Vectorization
    tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
    vectors = tfidf.fit_transform(new_df['tags']).toarray()

    # Similarity matrix
    similarity = cosine_similarity(vectors)

    # Rename id to movie_id for consistency
    new_df.rename(columns={'id': 'movie_id'}, inplace=True)

    # Save the model files
    pickle.dump(new_df, open("movies.pkl", "wb"))
    pickle.dump(similarity, open("similarity.pkl", "wb"))

    print("✅ Model training complete. Files saved as 'movies.pkl' and 'similarity.pkl'")


# Optional: allows manual testing of this script
if __name__ == "__main__":
    train()

