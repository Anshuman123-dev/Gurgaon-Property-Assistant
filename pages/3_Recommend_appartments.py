import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ---------- Page Config ----------
st.set_page_config(page_title="Recommend Apartments", layout="wide")
st.title("🏠 Apartment Recommender System")

# ---------- Load Data ----------
location_df = pickle.load(open('datasets/location_distances.pkl', 'rb'))
cosine_sim1 = pickle.load(open('datasets/cosine_sim1.pkl', 'rb'))
cosine_sim2 = pickle.load(open('datasets/cosine_sim2.pkl', 'rb'))
cosine_sim3 = pickle.load(open('datasets/cosine_sim3.pkl', 'rb'))

# ---------- Recommender Function ----------
def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1.0 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    top_properties = location_df.index[top_indices].tolist()
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })
    return recommendations_df

# ---------- 🔍 Radius-Based Location Filter ----------
st.subheader("📍 Filter Apartments by Radius")

location_options = ['Select a location'] + sorted(location_df.columns.to_list())
selected_location = st.selectbox('📌 Choose a location', location_options)

radius = st.number_input('📏 Radius in Kms (enter a value)', min_value=0.0, value=0.0, step=0.5, format="%.2f")

if st.button('Search Nearby Apartments'):
    if selected_location == 'Select a location':
        st.warning("Please choose a valid location.")
    elif radius == 0.0:
        st.warning("Please enter a valid radius greater than 0.")
    else:
        result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
        if result_ser.empty:
            st.warning("No apartments found within this radius.")
        else:
            st.success(f"Apartments within {radius} km of {selected_location}:")
            for key, value in result_ser.items():
                st.text(f"{key} - {round(value / 1000, 2)} km")

# ---------- 🤝 Similar Apartment Recommender ----------
st.subheader("🏙️ Recommend Similar Apartments")

apartment_options = ['Select an apartment'] + sorted(location_df.index.to_list())
selected_apartment = st.selectbox('🏢 Select an apartment', apartment_options)

if st.button('Recommend', key='recommend_btn'):
    if selected_apartment == 'Select an apartment':
        st.warning("Please choose a valid apartment.")
    else:
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        if recommendation_df.empty:
            st.warning("No recommendations found.")
        else:
            st.success(f"Top Recommendations similar to '{selected_apartment}':")
            st.dataframe(recommendation_df)



