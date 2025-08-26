import streamlit as st

# ---------- Page Config ----------
st.set_page_config(
    page_title="🏘️ Gurgaon Property Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Enhanced Custom CSS ----------
st.markdown("""
    <style>
        /* Main theme */
        .main {
            background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 50%, #0f1419 100%);
            color: white;
        }
        
        /* Hero Section */
        .hero-container {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #1e40af 100%);
            padding: 60px 40px;
            border-radius: 20px;
            margin: 20px 0 50px 0;
            text-align: center;
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.3);
            position: relative;
            overflow: hidden;
        }
        
        .hero-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="25" cy="25" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="50" cy="10" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="10" cy="70" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="90" cy="30" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(5deg); }
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: white;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 20px;
            position: relative;
            z-index: 1;
        }
        
        .hero-subtitle {
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 30px;
            position: relative;
            z-index: 1;
            line-height: 1.6;
        }
        
        .cta-button {
            background: linear-gradient(45deg, #f59e0b, #fbbf24);
            color: #1f2937;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            font-size: 1.1rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
            box-shadow: 0 8px 16px rgba(245, 158, 11, 0.3);
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 20px rgba(245, 158, 11, 0.4);
        }
        
        /* Feature Cards */
        .feature-card {
            margin: 20px 0;
        }
        
        .feature-card {
            background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
            padding: 30px;
            border-radius: 15px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(59, 130, 246, 0.2);
            border-color: rgba(59, 130, 246, 0.4);
        }
        
        .feature-card:hover::before {
            transform: scaleX(1);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            display: block;
        }
        
        .feature-title {
            font-size: 1.4rem;
            color: #60a5fa;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .feature-text {
            font-size: 1rem;
            color: #d1d5db;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .feature-badge {
            display: inline-block;
            background: linear-gradient(45deg, #10b981, #059669);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        /* Stats Section */
        .stats-container {
            background: linear-gradient(135deg, #111827, #1f2937);
            padding: 40px;
            border-radius: 15px;
            margin: 40px 0;
            text-align: center;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }
        
        .stat-item {
            padding: 20px;
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 800;
            color: #3b82f6;
            display: block;
        }
        
        .stat-label {
            font-size: 1rem;
            color: #9ca3af;
            margin-top: 5px;
        }
        
        /* Footer */
        .footer {
            background: linear-gradient(135deg, #111827, #1f2937);
            padding: 40px;
            border-radius: 15px;
            margin: 50px 0 20px 0;
            text-align: center;
            border-top: 2px solid rgba(59, 130, 246, 0.2);
        }
        
        .footer-text {
            color: #9ca3af;
            font-size: 1rem;
            margin-bottom: 20px;
        }
        
        .tech-badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .tech-badge {
            background: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .hero-title {
                font-size: 2.5rem;
            }
            .hero-subtitle {
                font-size: 1.1rem;
            }
            .features-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Hero Section ----------
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🏠 Gurgaon Property Assistant</div>
        <div class="hero-subtitle">
            Discover, analyze, and predict the perfect apartments in Gurgaon with AI-powered insights.<br>
            Your intelligent companion for smart real estate decisions.
        </div>
        <a href="#features" class="cta-button">Explore Features</a>
    </div>
""", unsafe_allow_html=True)

# ---------- Stats Section ----------
st.markdown("""
    <div class="stats-container">
        <h2 style="color: #60a5fa; font-size: 2rem; margin-bottom: 10px;">Platform Statistics</h2>
        <p style="color: #9ca3af; font-size: 1.1rem;">Trusted by property seekers across Gurgaon</p>
        <div class="stats-grid">
            <div class="stat-item">
                <span class="stat-number">10,000+</span>
                <div class="stat-label">Properties Analyzed</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">95%</span>
                <div class="stat-label">Prediction Accuracy</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">50+</span>
                <div class="stat-label">Localities Covered</div>
            </div>
            <div class="stat-item">
                <span class="stat-number">24/7</span>
                <div class="stat-label">AI Assistance</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ---------- Enhanced Feature Cards ----------
st.markdown('<div id="features"></div>', unsafe_allow_html=True)

# Create feature cards using Streamlit columns for better compatibility
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📍</span>
            <div class="feature-title">Smart Location Search</div>
            <div class="feature-text">
                Discover apartments within any radius of Gurgaon landmarks. Our intelligent search considers metro connectivity, traffic patterns, and local amenities for optimal location matching.
            </div>
            <span class="feature-badge">AI-Powered</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💰</span>
            <div class="feature-title">Price Predictor Pro</div>
            <div class="feature-text">
                Get accurate price estimates using our trained neural network model. Input property details and get instant valuations based on current market conditions.
            </div>
            <span class="feature-badge">95% Accurate</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🏢</span>
            <div class="feature-title">Similarity Engine</div>
            <div class="feature-text">
                Advanced machine learning algorithms analyze 50+ property features to recommend apartments that match your preferences. Find your perfect home based on similar properties you love.
            </div>
            <span class="feature-badge">ML-Based</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">Personalized Recommendations</div>
            <div class="feature-text">
                Our AI learns from your preferences and search patterns to provide tailored property suggestions that match your lifestyle and budget requirements.
            </div>
            <span class="feature-badge">Personalized</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📈</span>
            <div class="feature-title">Market Intelligence</div>
            <div class="feature-text">
                Interactive dashboards reveal price trends, locality growth patterns, and investment opportunities. Make data-driven decisions with real-time market insights.
            </div>
            <span class="feature-badge">Real-time</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📊</span>
            <div class="feature-title">Investment Analytics</div>
            <div class="feature-text">
                Comprehensive ROI analysis, rental yield predictions, and future appreciation forecasts help you make smart investment decisions in Gurgaon's dynamic market.
            </div>
            <span class="feature-badge">Pro Analytics</span>
        </div>
    """, unsafe_allow_html=True)

# ---------- Enhanced Footer ----------
st.markdown("""
    <div class="footer">
        <div class="footer-text">
            Empowering smarter real estate decisions with cutting-edge AI technology<br>
            Built with passion for the Gurgaon property market
        </div>
        <div class="tech-badges">
            <span class="tech-badge">🐍 Python</span>
            <span class="tech-badge">🚀 Streamlit</span>
            <span class="tech-badge">🤖 Machine Learning</span>
            <span class="tech-badge">📊 Data Science</span>
            <span class="tech-badge">🔮 AI/ML</span>
            <span class="tech-badge">📈 Analytics</span>
        </div>
        <p style="color: #6b7280; font-size: 0.9rem; margin-top: 30px;">
            © 2024 Gurgaon Property Assistant | Made with ❤️ for smart property decisions
        </p>
    </div>
""", unsafe_allow_html=True)