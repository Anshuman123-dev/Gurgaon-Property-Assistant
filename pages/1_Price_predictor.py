import streamlit as st
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Page configuration with custom theme
st.set_page_config(
    page_title="Property Price Predictor",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Input section styling */
    .input-section {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .input-section h2 {
        color: #2c3e50;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 600;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        border: 2px solid #d1d9e6;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4facfe;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.2);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #4facfe;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.15);
        transform: translateY(-1px);
    }
    
    /* Selectbox dropdown arrow styling */
    .stSelectbox svg {
        color: #667eea !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div {
        background: linear-gradient(145deg, #ffffff, #f0f2f6);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input {
        background: transparent !important;
        border: 2px solid #d1d9e6 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #2c3e50 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #4facfe !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.2) !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #4facfe !important;
        box-shadow: 0 0 0 3px rgba(79, 172, 254, 0.15) !important;
        transform: translateY(-1px);
        outline: none !important;
    }
    
    /* Number input buttons styling */
    .stNumberInput button {
        background: linear-gradient(145deg, #667eea, #764ba2) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 2px 8px rgba(116, 75, 162, 0.3) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 25px;
        box-shadow: 0 4px 15px 0 rgba(116, 75, 162, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(116, 75, 162, 0.4);
    }
    
    /* Result styling */
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .result-box h3 {
        color: white;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .price-range {
        background: rgba(255, 255, 255, 0.2);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        font-size: 1.3rem;
        font-weight: 700;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Column styling */
    .input-column {
        padding: 0.5rem;
    }
    
    /* Label styling */
    .stSelectbox label, .stNumberInput label {
        color: #2c3e50 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input field text styling */
    .stSelectbox div[data-baseweb="select"] > div {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #2c3e50 !important;
        padding: 0.75rem 1rem !important;
    }
    
    /* Placeholder text styling */
    .stSelectbox div[data-baseweb="select"] > div:first-child {
        color: #6c757d !important;
    }
    
    /* Input container styling */
    .input-column .stSelectbox, .input-column .stNumberInput {
        margin-bottom: 1.5rem;
    }
    
    /* Custom focus ring for all inputs */
    .stSelectbox:focus-within,
    .stNumberInput:focus-within {
        outline: none;
    }
    
    /* Error message styling */
    .stAlert {
        background: linear-gradient(145deg, #fff5f5, #fed7d7);
        border: 2px solid #fc8181;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(252, 129, 129, 0.2);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Load data
data_dir = Path(__file__).parent
with open(data_dir / 'df.pkl', 'rb') as file:
    df = pickle.load(file)

with open(data_dir / 'pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏠 Property Price Predictor</h1>
    <p>Get accurate property price estimates with our advanced ML model</p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h2>📝 Property Details</h2>', unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="input-column">', unsafe_allow_html=True)
    property_type = st.selectbox('🏢 Property Type', ['Select Property Type', 'flat', 'house'])
    sector = st.selectbox('📍 Sector', ['Select Sector'] + sorted(df['sector'].unique().tolist()))
    bedroom_opt = ['Select Bedrooms'] + sorted(df['bedRoom'].unique().tolist())
    bedroom = st.selectbox('🛏️ Number of Bedrooms', bedroom_opt)
    bathroom_opt = ['Select Bathrooms'] + sorted(df['bathroom'].unique().tolist())
    bathroom = st.selectbox('🚿 Number of Bathrooms', bathroom_opt)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="input-column">', unsafe_allow_html=True)
    balcony_opt = ['Select Balconies'] + sorted(df['balcony'].unique().tolist())
    balcony = st.selectbox('🏞️ Balconies', balcony_opt)
    property_age = st.selectbox('📅 Property Age', ['Select Property Age'] + sorted(df['agePossession'].unique().tolist()))
    built_up_area = st.number_input('📐 Built Up Area (sq ft)', min_value=0.0, step=1.0)
    servant_room = st.selectbox('👥 Servant Room', ['Select Option', 0.0, 1.0])
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="input-column">', unsafe_allow_html=True)
    store_room = st.selectbox('📦 Store Room', ['Select Option', 0.0, 1.0])
    furnishing_type = st.selectbox('🪑 Furnishing Type', ['Select Furnishing Type'] + sorted(df['furnishing_type'].unique().tolist()))
    luxury_category = st.selectbox('✨ Luxury Category', ['Select Luxury Category'] + sorted(df['luxury_category'].unique().tolist()))
    floor_category = st.selectbox('🏗️ Floor Category', ['Select Floor Category'] + sorted(df['floor_category'].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Center the predict button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_button = st.button('🔮 Predict Property Price')

if predict_button:
    # Validation
    required_fields = [
        (property_type, 'Property Type'),
        (sector, 'Sector'),
        (bedroom, 'Number of Bedrooms'),
        (bathroom, 'Number of Bathrooms'),
        (balcony, 'Balconies'),
        (property_age, 'Property Age'),
        (servant_room, 'Servant Room'),
        (store_room, 'Store Room'),
        (furnishing_type, 'Furnishing Type'),
        (luxury_category, 'Luxury Category'),
        (floor_category, 'Floor Category')
    ]
    
    missing_fields = [field for value, field in required_fields if str(value).startswith('Select')]
    
    if missing_fields or built_up_area <= 0:
        st.error(f"⚠️ Please fill in all required fields: {', '.join(missing_fields)}")
        if built_up_area <= 0:
            st.error("⚠️ Please enter a valid Built Up Area")
    else:
        # Form DataFrame
        data = [[property_type, sector, bedroom, bathroom, balcony, property_age, 
                built_up_area, servant_room, store_room, furnishing_type, 
                luxury_category, floor_category]]
        
        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                   'agePossession', 'built_up_area', 'servant room', 'store room',
                   'furnishing_type', 'luxury_category', 'floor_category']
        
        one_df = pd.DataFrame(data, columns=columns)
        
        # Predict
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22
        
        # Display result
        st.markdown(f"""
        <div class="result-box">
            <h3>💰 Estimated Property Price</h3>
            <div class="price-range">
                ₹ {round(low, 2)} Cr - ₹ {round(high, 2)} Cr
            </div>
            <p style="color: rgba(255,255,255,0.8); margin-top: 1rem; font-size: 0.9rem;">
                *Price estimate based on current market trends and property features
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7);">
    <p>Built with ❤️ using Streamlit | Property Price Prediction ML Model</p>
</div>
""", unsafe_allow_html=True)