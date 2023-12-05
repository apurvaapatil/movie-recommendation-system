from urllib import response
import streamlit as st
import pickle
import requests

# load the steam file of dataframe created in Jupyter notebook
# The name of our dataframe is 'movies_data_frame'
movies_data_frame = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# after loading the .pkl file, 'movies_list' contains the actual dataframe, 
# hence we can access it in the same as we did in the Jupyter notebook.
movies_list = movies_data_frame['title'].values

# fetch posters
def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=67ef8a78540e253184ffafee99eb8532".format(movie_id))
    data = response.json()
    if(data['poster_path'] is None):
        return ("https://cdn1.vectorstock.com/i/thumb-large/50/20/no-photo-or-blank-image-icon-loading-images-vector-37375020.jpg")
    return ("https://image.tmdb.org/t/p/w500/" + data['poster_path'])

def recommend(movie):
    movie_index = movies_data_frame[movies_data_frame['title'] == movie].index[0]
    distances_array = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances_array)), reverse=True, key=lambda x:x[1])[1:6]
    
    titles = []
    movie_posters=[]
    for i in movies_list:
        titles.append(movies_data_frame.iloc[i[0]].title)
        # fetch posters from API
        poster = fetch_poster(movies_data_frame.iloc[i[0]].movie_id)
        movie_posters.append(poster)

    return titles, movie_posters

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
     'Please select a movie',
     movies_list)

if st.button('Recommend'):
    st.write("You might also like: ")
    Reclist, posters_list = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters_list[0])
        st.write(Reclist[0])

    with col2:
        st.image(posters_list[1])
        st.write(Reclist[1])

    with col3:
        st.image(posters_list[2])
        st.write(Reclist[2])
    
    with col4:
        st.image(posters_list[3])
        st.write(Reclist[3])

    with col5:
        st.image(posters_list[4])
        st.write(Reclist[4])



