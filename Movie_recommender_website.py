import requests
import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies=[]
    movie_id_list=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        movie_link=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=5e35f74847d12bda931cc537c8010df6".format(movie_id))
        data=movie_link.json()
        release_date=data['release_date']
        movie_id_list.append(release_date)
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies,movie_id_list

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'How would you like to be contacted ?',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations,recommendations_id=recommend(selected_movie_name)
    c=0
    for i in recommendations:
        st.write(i,recommendations_id[c]) 
        c+=1