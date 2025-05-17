import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/390px-No-Image-Placeholder.svg.png"
    except:
        return "https://getodk.b-cdn.net/uploads/default/original/3X/4/7/4745ebbdfae5bd2e641b5c91070edd2174154772.png"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters, distances

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters, dist = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.text(f"Similarity score: { round((1 - round(dist[0],5))*100,3)}%")

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.text(f"Similarity score: { round((1 - round(dist[1],5))*100,3)}%")

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.text(f"Similarity score: { round((1 - round(dist[2],5))*100,3)}%")

    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.text(f"Similarity score: { round((1 - round(dist[3],5))*100,3)}%")

    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.text(f"Similarity score: { round((1 - round(dist[4],5))*100,3)}%")
