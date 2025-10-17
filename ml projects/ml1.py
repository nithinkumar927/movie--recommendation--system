import streamlit as st
import difflib
import pickle

with open('movies_df.pkl', 'rb') as f:
    A = pickle.load(f)

with open('similarity_matrix.pkl', 'rb') as f:
    similarity = pickle.load(f)


def recommend_movies(movie_title):
    list_of_titles = A['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_title, list_of_titles)

    if not find_close_match:
        return "No close match found for the movie title."

    close_match = find_close_match[0]
    index_of_movie = A[A.title == close_match]['index'].values[0]
    similarity_score = list(enumerate(similarity[index_of_movie]))
    sorted_similar_movies = sorted(
        similarity_score, key=lambda x: x[1], reverse=True)

    recommended_movies_list = []
    for i, (index, score) in enumerate(sorted_similar_movies):
        if (i < 20) and (A[A.index == index]['title'].values[0] != close_match):
            recommended_movies_list.append(
                A[A.index == index]['title'].values[0])

    return recommended_movies_list


st.title('Movie Recommendation System')

movie_name = st.text_input('Enter your favorite movie name:')

if movie_name:
    recommendations = recommend_movies(movie_name)
    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        st.write('Movies suggested for you:')
        for i, movie in enumerate(recommendations):
            st.write(f"{i+1}. {movie}")
