# Movie_recommender_system

This project is a **Movie Recommender System** that suggests movies based on their similarity in genres, cast, crew, and other features. It is built using **Python, Machine Learning,** and the **TMDB API** for fetching movie posters and additional movie details.

## Project Description

The Movie Recommender System provides personalized movie recommendations. Using a combination of **content-based filtering** and **vector similarity measures**, it delivers suggestions to users based on the selected movie. A user-friendly interface, built using **Streamlit**, enhances the user experience.

## Key Feature:

After a user hits the **Recommend** button, movie posters are displayed along with a **More Info** button. Clicking this button redirects the user to the movie’s page on the **TMDB website**, where they can view the movie's trailer, ratings, and detailed information.

## Features

- Content-Based Recommendations: Suggests movies similar to the selected movie based on genres, cast, crew, and tags.
- TMDB API Integration:
  - Fetches dynamic movie posters.
  - Provides links to detailed movie information, including trailers and ratings.
- Interactive User Interface: Built with Streamlit for seamless interaction.
- Data Cleaning and Preprocessing: Ensures data accuracy and usability by cleaning and transforming the movie datasets.

## Datasets

The following datasets are used:

1. **movies.csv:** Contains movie details such as title, genres, cast, and crew.


2. **credits.csv:** Provides information about the cast and crew members.

## Methodology

1. Data Preprocessing

  - Handled missing values and duplicates.

  - Converted complex columns (e.g., genres, cast) into a structured format.

  - Merged data from both datasets into a single DataFrame.


2. Feature Engineering

  - Combined features like genres, keywords, and cast into a single column (tags).

  - Used TF-IDF Vectorization to create numerical representations of tags.


3. Similarity Calculation

  - Applied cosine similarity to calculate similarities between movies.

4. API Integration

  - Connected the project to the TMDB API to fetch high-quality movie posters.

  - Added functionality to redirect users to the movie's TMDB page for trailers and ratings.


5. Interactive Interface

  - Built a responsive interface using Streamlit to allow users to input a movie and get recommendations in real time.


## Tools and Technologies

= **Python**: Core programming language.

- **Libraries**: NumPy, Pandas, Scikit-learn, Streamlit, Requests.

- **Jupyter Notebook**: Used for data cleaning, feature engineering, and model development.

- **TMDB API**: For fetching dynamic movie posters and movie details.



