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
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with green theme
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #2d5016 0%, #16a085 100%);
        padding: 2rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #27ae60 0%, #2ecc71 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(46, 204, 113, 0.4);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        margin: 0;
        font-weight: 500;
    }
    
    /* Input section styling */
    .input-section {
        background: rgba(255, 255, 255, 0.98);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(46, 204, 113, 0.2);
        backdrop-filter: blur(8px);
        border: 2px solid rgba(46, 204, 113, 0.3);
    }
    
    .input-section h2 {
        color: #1e8449;
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(30, 132, 73, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #ffffff, #f8fff8);
        border: 2px solid #a9dfbf;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(46, 204, 113, 0.15);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #27ae60;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.25);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #27ae60;
        box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.2);
        transform: translateY(-2px);
    }
    
    /* Selectbox dropdown arrow styling */
    .stSelectbox svg {
        color: #27ae60 !important;
    }
    
    /* Number input styling */
    .stNumberInput > div > div {
        background: linear-gradient(145deg, #ffffff, #f8fff8);
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(46, 204, 113, 0.15);
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input {
        background: transparent !important;
        border: 2px solid #a9dfbf !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #1e8449 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput > div > div > input:hover {
        border-color: #27ae60 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.25) !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #27ae60 !important;
        box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.2) !important;
        transform: translateY(-2px);
        outline: none !important;
    }
    
    /* Number input buttons styling */
    .stNumberInput button {
        background: linear-gradient(145deg, #27ae60, #2ecc71) !important;
        border: none !important;
        border-radius: 8px !important;
        color: white !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.4) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        font-weight: 700;
        font-size: 1.2rem;
        padding: 1rem 3rem;
        border: none;
        border-radius: 30px;
        box-shadow: 0 6px 20px 0 rgba(46, 204, 113, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 1rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px 0 rgba(46, 204, 113, 0.5);
        background: linear-gradient(45deg, #2ecc71 0%, #58d68d 100%);
    }
    
    /* Result styling */
    .result-box {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 10px 40px 0 rgba(46, 204, 113, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .result-box h3 {
        color: white;
        font-size: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .price-range {
        background: rgba(255, 255, 255, 0.25);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        font-size: 1.5rem;
        font-weight: 800;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.3);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    /* Column styling */
    .input-column {
        padding: 0.5rem;
    }
    
    /* AGGRESSIVE TEXT VISIBILITY FIXES - Override all Streamlit defaults */
    
    /* Target all possible selectbox text elements */
    .stSelectbox div,
    .stSelectbox span,
    .stSelectbox p,
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-testid="stSelectbox"] div,
    .stSelectbox [data-testid="stSelectbox"] span,
    .stSelectbox > div > div div,
    .stSelectbox > div > div span {
        color: #000000 !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }
    
    /* Force selected value visibility */
    .stSelectbox [role="button"] div,
    .stSelectbox [role="button"] span,
    .stSelectbox [aria-expanded="false"] div,
    .stSelectbox [aria-expanded="false"] span {
        color: #000000 !important;
        font-weight: 700 !important;
        background-color: transparent !important;
    }
    
    /* Placeholder text - slightly lighter but still visible */
    .stSelectbox div:first-child {
        color: #333333 !important;
        font-style: italic !important;
        font-weight: 600 !important;
    }
    
    /* Number input text */
    .stNumberInput input {
        color: #000000 !important;
        font-weight: 700 !important;
    }
    
    /* Labels - keep them dark green */
    .stSelectbox label, 
    .stNumberInput label {
        color: #1e8449 !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 1px 1px 2px rgba(30, 132, 73, 0.1);
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
        border: 2px solid #e74c3c;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
    }
    
    .stAlert .stMarkdown {
        color: #c0392b !important;
        font-weight: 600 !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(145deg, #f0fff4, #d4edda);
        border: 2px solid #27ae60;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(39, 174, 96, 0.3);
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 600;
        font-size: 1rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* SUPER AGGRESSIVE DROPDOWN FIXES */
    .stSelectbox div[role="listbox"] {
        background: white !important;
        border: 2px solid #27ae60 !important;
        border-radius: 10px !important;
        box-shadow: 0 8px 25px rgba(39, 174, 96, 0.3) !important;
    }
    
    .stSelectbox div[role="listbox"] div,
    .stSelectbox div[role="listbox"] span,
    .stSelectbox [role="option"],
    .stSelectbox [role="option"] div,
    .stSelectbox [role="option"] span {
        color: #000000 !important;
        font-weight: 700 !important;
        background: white !important;
    }
    
    .stSelectbox div[role="listbox"] div:hover,
    .stSelectbox [role="option"]:hover {
        background: #f0fff4 !important;
        color: #000000 !important;
    }
    
    /* Nuclear option - force ALL text in selectbox to be black */
    .stSelectbox * {
        color: #000000 !important;
    }
    
    /* Selectbox container background to ensure contrast */
    .stSelectbox > div > div {
        background: white !important;
    }
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
            <p style="color: rgba(255,255,255,0.9); margin-top: 1rem; font-size: 1rem; font-weight: 500;">
                *Price estimate based on current market trends and property features
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>Built with ❤️ using Streamlit | Property Price Prediction ML Model</p>
</div>
""", unsafe_allow_html=True)