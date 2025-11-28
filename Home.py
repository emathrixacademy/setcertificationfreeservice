"""
SET Certification Platform - Home Page
Main entry point with login, registration, and landing page
"""

import streamlit as st
from utils.auth import (
    init_session, login_user, register_user, logout_user,
    verify_email_token, is_authenticated
)
from utils.helpers import show_success, show_error, show_info
import hashlib


# Page configuration
st.set_page_config(
    page_title="SET Certification Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session
init_session()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)


def show_landing_page():
    """Display landing page for non-authenticated users"""
    
    # Hero section
    st.markdown("""
    <div class="main-header">
        <h1>🎓 SET Certification Platform</h1>
        <h3>FREE EDUCATION • FREE TOOLS • FREE FUTURE</h3>
        <p>Your complete resource for Special Education Teacher certification preparation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("## 🌟 Platform Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Digital Library</h3>
            <p>Free downloadable books and comprehensive study materials for SET exam preparation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🛠️ AI Tools</h3>
            <p>15+ educational AI assistants for lesson planning, assessment creation, and more.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📝 Practice Exams</h3>
            <p>Timed mock tests with detailed explanations to track your progress.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎥 Video Tutorials</h3>
            <p>Curated educational video content covering key SET concepts.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🎮 Interactive Games</h3>
            <p>Learn through engaging gamified experiences and challenges.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🏆 Gamification</h3>
            <p>Earn points, unlock badges, and climb the leaderboard!</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("---")
    st.markdown("### 🚀 Ready to Start Your Journey?")
    st.info("👉 **Create a free account** using the sidebar or **login** to continue your learning!")


def show_dashboard():
    """Display dashboard for authenticated users"""
    
    user = st.session_state
    
    # Welcome header
    st.markdown(f"""
    <div class="main-header">
        <h1>Welcome back, {user['username']}! 👋</h1>
        <h3>Level {user['current_level']} • {user['total_points']:,} Points</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Points", f"{user['total_points']:,}")
    
    with col2:
        st.metric("Current Level", user['current_level'])
    
    with col3:
        st.metric("Login Streak", f"{user['current_streak']} days")
    
    with col4:
        if user['is_verified']:
            st.success("✅ Verified")
        else:
            st.warning("⚠️ Not Verified")
    
    st.markdown("---")
    
    # Quick links
    st.markdown("### 🎯 Quick Access")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Browse Books", use_container_width=True):
            st.switch_page("pages/1_📚_Books.py")
    
    with col2:
        if st.button("🛠️ AI Tools", use_container_width=True):
            st.switch_page("pages/2_🛠️_AI_Tools.py")
    
    with col3:
        if st.button("📝 Practice Exams", use_container_width=True):
            st.switch_page("pages/3_📝_Practice_Exams.py")
    
    # Recent activity
    st.markdown("### 📊 Your Progress")
    st.info("Complete activities to earn points and level up! Check the sidebar for navigation.")


def show_auth_sidebar():
    """Display authentication forms in sidebar"""
    
    if is_authenticated():
        # Logged in user menu
        with st.sidebar:
            st.markdown(f"### 👤 {st.session_state['username']}")
            st.markdown(f"**Level {st.session_state['current_level']}**")
            st.progress(st.session_state['current_level'] / 10)
            st.markdown(f"🏆 {st.session_state['total_points']:,} points")
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()
                st.rerun()
    
    else:
        # Login/Register forms
        with st.sidebar:
            st.markdown("### 🔐 Account Access")
            
            tab1, tab2 = st.tabs(["Login", "Register"])
            
            with tab1:
                with st.form("login_form"):
                    email = st.text_input("Email", placeholder="your@email.com")
                    password = st.text_input("Password", type="password")
                    submit = st.form_submit_button("Login", use_container_width=True)
                    
                    if submit:
                        if not email or not password:
                            show_error("Please fill in all fields")
                        else:
                            success, message, user_data = login_user(email, password)
                            if success:
                                show_success(message)
                                st.rerun()
                            else:
                                show_error(message)
            
            with tab2:
                with st.form("register_form"):
                    username = st.text_input("Username", placeholder="Choose a username")
                    email = st.text_input("Email", placeholder="your@email.com")
                    password = st.text_input("Password", type="password")
                    password_confirm = st.text_input("Confirm Password", type="password")
                    referral_code = st.text_input("Referral Code (optional)", placeholder="Enter if you have one")
                    
                    submit = st.form_submit_button("Create Account", use_container_width=True)
                    
                    if submit:
                        if not username or not email or not password:
                            show_error("Please fill in all required fields")
                        elif password != password_confirm:
                            show_error("Passwords do not match")
                        else:
                            ref_code = referral_code.strip() if referral_code else None
                            success, message = register_user(username, email, password, ref_code)
                            if success:
                                show_success(message)
                            else:
                                show_error(message)


def main():
    """Main application logic"""
    
    # Show authentication sidebar
    show_auth_sidebar()
    
    # Check for verification token in URL
    query_params = st.query_params
    
    if 'verify' in query_params:
        token = query_params['verify']
        success, message = verify_email_token(token)
        
        if success:
            show_success(message)
            st.balloons()
        else:
            show_error(message)
        
        # Clear the token from URL
        st.query_params.clear()
    
    # Show appropriate page
    if is_authenticated():
        show_dashboard()
    else:
        show_landing_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem 0;">
        <p><strong>SET Certification Platform</strong></p>
        <p>FREE EDUCATION • FREE TOOLS • FREE FUTURE</p>
        <p>© 2025 All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
