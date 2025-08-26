import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns



# Page config
st.set_page_config(page_title="Analytics", layout="wide")
st.title('🏙️ Sector Analytics Dashboard')

# Load GeoMap Data
@st.cache_data
def load_map_data():
    return pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl','rb'))



map_df = load_map_data()


# ------------------- 🗺️ GEOMAP --------------------
st.subheader("📍 Sector-wise Price Per Sqft Map")

group_df = map_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]
group_df['latitude'] = group_df['latitude'].astype(float)
group_df['longitude'] = group_df['longitude'].astype(float)
group_df = group_df.reset_index()

fig = px.scatter_mapbox(group_df,
                        lat="latitude",
                        lon="longitude",
                        color="price_per_sqft",
                        size='built_up_area',
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom=10,
                        mapbox_style="open-street-map",
                        width=1200,
                        height=700,
                        hover_name="sector",
                        text="sector")
fig.update_traces(textposition='top center')

st.plotly_chart(fig, use_container_width=True)

# ------------------- ☁️ WORD CLOUD --------------------

# Create the word cloud object
wordcloud = WordCloud(
    width=800, height=800,
    background_color='black',
    stopwords=set(['s']),  # Add any stopwords you want
    min_font_size=10
).generate(feature_text)

# Create the matplotlib figure
fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)

# Show in Streamlit
st.pyplot(fig)


st.header('Area Vs Price')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(map_df[map_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(map_df[map_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

sector_options = map_df['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig2 = px.pie(map_df, names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)
else:

    fig2 = px.pie(map_df[map_df['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(map_df[map_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.distplot(map_df[map_df['property_type'] == 'house']['price'],label='house')
sns.distplot(map_df[map_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig3)

import streamlit as st
import pandas as pd
import plotly.express as px

st.header(" Average Price vs Luxury Score")

# Dropdown for sector selection
sector_list = ['overall'] + sorted(map_df['sector'].dropna().unique().tolist())
selected_sector = st.selectbox("Select Sector", sector_list, key="luxury_sector")

# Prepare data
if selected_sector == 'overall':
    df_filtered = map_df.copy()
else:
    df_filtered = map_df[map_df['sector'] == selected_sector]

# Clean and group by luxury_score (optional: bin into intervals)
lux_price_df = df_filtered.groupby('luxury_score')['price'].mean().reset_index()

# Sort just in case
lux_price_df = lux_price_df.sort_values(by='luxury_score')

# Line plot
fig_lux = px.line(
    lux_price_df,
    x='luxury_score',
    y='price',
    markers=True,
    title=f"Average Price vs Luxury Score ({selected_sector})"
)

fig_lux.update_layout(xaxis_title="Luxury Score", yaxis_title="Average Price (CR)", height=500)

st.plotly_chart(fig_lux, use_container_width=True)
