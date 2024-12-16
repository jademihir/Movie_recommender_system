import pandas as pd
import streamlit as st
import pickle
import requests
import os

# Dummy credentials storage
USER_CREDENTIALS = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}

# Function to fetch movie poster and other details
def fetch_movie_details(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=47dd52ce23ec8410d38508076dbb5d8a&language=en-US')
        data = response.json()
        movie_details = {
            "title": data.get("title", "Unknown Title"),
            "plot": data.get("overview", "No description available."),
            "release_date": data.get("release_date", "N/A"),
            "rating": data.get("vote_average", "N/A"),
            "poster": f"https://image.tmdb.org/t/p/w500/{data['poster_path']}" if 'poster_path' in data else "https://via.placeholder.com/500x750?text=No+Image+Available",
            "url": f"https://www.themoviedb.org/movie/{movie_id}"  # Movie details URL
        }
        return movie_details
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movie details: {e}")
        return {
            "title": "Unknown Title",
            "plot": "No description available.",
            "release_date": "N/A",
            "rating": "N/A",
            "poster": "https://via.placeholder.com/500x750?text=Image+Unavailable",
            "url": "#"
        }

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ids = []  # To store movie IDs for fetching details
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_movie_details(movie_id)['poster'])
        recommended_movies_ids.append(movie_id)
    return recommended_movies, recommended_movies_posters, recommended_movies_ids

# Load movie data and similarity matrix
if not os.path.exists('movie_dict.pkl') or not os.path.exists('similarity.pkl'):
    st.error("Required files are missing!")
else:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    # Function for login
    def login(username, password):
        return USER_CREDENTIALS.get(username) == password

    # Function to register a new user
    def register(username, password):
        if username in USER_CREDENTIALS:
            return False
        else:
            USER_CREDENTIALS[username] = password
            return True

    # Streamlit app UI customization
    st.markdown("""
        <style>
        body {
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        .title {
            font-size: 48px;
            font-weight: bold;
            color: #FF6347;
            text-align: center;
            margin-top: 20px;
        }
        .subheader {
            font-size: 24px;
            font-weight: bold;
            color: #1E90FF;
            text-align: center;
            margin-top: 10px;
        }
        .logout-button {
            margin-top: 20px;
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #FF6347;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .logout-button:hover {
            background-color: #e55347;
        }
        </style>
    """, unsafe_allow_html=True)

    # Streamlit app flow
    if 'page' not in st.session_state:
        st.session_state.page = 'login'

    if st.session_state.page == 'login':
        st.markdown("<h1 class='title'>Login to Movie Recommender System</h1>", unsafe_allow_html=True)

        with st.container():
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

            if st.button("Login"):
                if login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.page = 'movie_recommendation'
                    st.success(f"Welcome, {username}!")
                else:
                    st.error("Invalid credentials.")

            if st.button("Register a new account"):
                st.session_state.page = 'register'

    elif st.session_state.page == 'register':
        st.title("Register New Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if password != confirm_password:
            st.error("Passwords do not match!")

        if username and password:
            if register(username, password):
                st.session_state.page = 'login'
                st.success(f"Account created successfully for {username}!")
            else:
                st.error("Username already exists. Please choose another one.")

    elif st.session_state.page == 'movie_recommendation':
        st.markdown("<h1 class='title'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

        selected_movie_name = st.selectbox('Select a movie to get recommendations: 🎥', movies['title'].values)

        if st.button('Recommend 🔍'):
            st.markdown("<h2 class='subheader'>Recommendations for: " + selected_movie_name + " 🎬", unsafe_allow_html=True)

            names, posters, movie_ids = recommend(selected_movie_name)

            # Create columns for the recommended movies
            cols = st.columns(5)  # 5 columns for 5 recommended movies
            for i, col in enumerate(cols):
                with col:
                    st.image(posters[i], width=150)
                    st.write(names[i])  # Display movie name
                    movie_details = fetch_movie_details(movie_ids[i])
                    # Create a "More Info" link that opens in a new tab
                    st.markdown(f'<a href="{movie_details["url"]}" target="_blank"><button style="background-color:#FF6347; color:white; padding:10px 20px; border:none; border-radius:5px;">More Info</button></a>', unsafe_allow_html=True)

        # Logout button
        if st.button('Logout'):
            st.session_state.logged_in = False
            st.session_state.page = 'login'
            st.experimental_rerun()
