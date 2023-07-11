import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import streamlit as st

from packages.search_song import search_song
from packages.run_recommender import get_feature_vector, show_similar_songs
# load data
dat = pd.read_csv('./data/processed/dat_for_recommender.csv')

song_features_normalized = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness']
song_features_not_normalized = ['duration_ms', 'key', 'loudness', 'mode', 'tempo']

all_features = song_features_normalized + song_features_not_normalized + ['decade', 'popularity']

# set app layout
st.set_page_config(layout="wide")


# set a good looking font
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



def main():
    st.markdown("# Your Customized Music Recommender")
    st.markdown("Welcome to this music recommender! \
                \n You can search for a song and get recommendations based on the song you searched for. \
                \n You can also customize the recommendations by selecting the features you care about. Enjoy!")

    # add selectbox for selecting the features
    st.sidebar.markdown("### Select Features")
    features = st.sidebar.multiselect('Select the features you care about', all_features, default=all_features)
    # add a slider for selecting the number of recommendations
    st.sidebar.markdown("### Number of Recommendations")
    num_recommendations = st.sidebar.slider('Select the number of recommendations', 10, 50, 10)

    # add a search box for searching the song by giving capital letters and year
    st.markdown("### Ready to get recommendations based on my song?")
    song_name = st.text_input('Enter the name of the song')
    if song_name != '':
        song_name = song_name.upper()
    year = st.text_input('Enter the year of the song (e.g. 2019). \
                         \nIf you are not sure if the song is in the database or not sure about the year, \
                         please leave the year blank and click the button below to search for the song.')
    if year != '':
        year = int(year)

    # exmaples of song name and year:
    # song_name = 'YOUR HAND IN MINE'
    # year = 2003

    # add a button for searching the song if the user does not know the year
    if st.button('Search for my song'):
        found_flag, found_song = search_song(song_name, dat)
        if found_flag:
            st.markdown("Perfect, this song is in the dataset:")
            # st.markdown(found_song)
            for i in range(len(found_song)):
                st.markdown("Song Name: " + found_song[i][0])
                st.markdown("Artist(s): " + found_song[i][1])
                st.markdown("Release Date: " + found_song[i][2])


        else:
            st.markdown("Sorry, this song is not in the dataset. Please try another song!")

    # add a button for getting recommendations
    if st.button('Get Recommendations'):
        if song_name == '':
            st.markdown("Please enter the name of the song!")
        elif year == '':
            st.markdown("Please enter the year of the song!")
        else:
            
            # show the most similar songs in wordcloud
            fig_cloud = show_similar_songs(song_name, year, dat, features, num_recommendations, plot_type='wordcloud')
            st.markdown(f"### Great! Here are your recommendation for \
                        \n#### {song_name} ({year})!")
            st.pyplot(fig_cloud)

            # show the most similar songs in bar chart
            fig_bar = show_similar_songs(song_name, year, dat, features, top_n=10, plot_type='bar')
            st.markdown("### Get a closer look at the top 10 recommendations for you!")
            st.pyplot(fig_bar)

if __name__ == "__main__":
    main()

    
    


