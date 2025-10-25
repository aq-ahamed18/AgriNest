import streamlit as st
import functions
import after_login
import base64

# ------------------- Background Setup -------------------
# Set background image from local file
def set_bg_from_local(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Use local background image
set_bg_from_local("background2.png")

# Initialize session state variables
if 'loggeduser' not in st.session_state:
    st.session_state.loggeduser = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

# ------------------- Sidebar Navigation -------------------
with st.sidebar:
    st.title("🌿 AgriNest")
    st.markdown("---")
    
    # Navigation menu
    menu_options = ["Home", "Login", "Sign Up", "About Us", "Our Team"]
    selected_menu = st.radio(
        "Navigate to:",
        menu_options,
        index=menu_options.index(st.session_state.current_page) if st.session_state.current_page in menu_options else 0
    )
    
    # Display logout button only if user is logged in
    if st.session_state.loggeduser is not None:
        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True, type="primary"):
            st.session_state.loggeduser = None
            st.session_state.current_page = "Home"
            st.rerun()
    
    st.markdown("---")
    st.caption("Use the menu above to navigate through the application")

# Update current page based on sidebar selection
if selected_menu != st.session_state.current_page:
    st.session_state.current_page = selected_menu
    st.rerun()

# ------------------- Page Routing -------------------
if st.session_state.current_page == "About Us":
    functions.about_us()
    
elif st.session_state.current_page == "Our Team":
    functions.our_team()
    
elif st.session_state.current_page == "Login" and st.session_state.loggeduser is None:
    functions.login_page()
    
elif st.session_state.current_page == "Sign Up" and st.session_state.loggeduser is None:
    functions.signup_page()
    
else:  # Home page or any other case
    # ------------------- Main App Content (Home Page) -------------------
    st.title("🌿 AgriNest")
    st.subheader("💡 Your friendly helper for all farming needs")

    st.write("""
    This project is a **Streamlit-based Python web application** that helps users 
    explore information about **plants, their related diseases, and suitable fertilizers**.  

    ### 🔍 Key Features:
    - View plant, disease, and fertilizer data  
    - Search for diseases associated with a plant  
    - Find fertilizers recommended for a specific plant or disease
    """)

    # Only show login/signup buttons if user is not logged in
    if st.session_state.loggeduser is None:
        # Keep the original two-column login/signup buttons
        col1, col2 = st.columns(2)
        with col1:
            st.write("Already a registered user?")
            if st.button("Login", key="main_login", use_container_width=True):
                st.session_state.current_page = "Login"
                st.rerun()
        with col2:
            st.write("Not yet registered?")
            if st.button("Sign-up", key="main_signup", use_container_width=True):
                st.session_state.current_page = "Sign Up"
                st.rerun()
    else:
        # ------------------- Post-Login Actions -------------------
        user = st.session_state.loggeduser

        st.markdown("---")
        # Display banner reflecting Free or Premium accurately
        if user["userType"] == "User":
            if user.get("accountType") == "Free":
                st.warning("⚠️ You are a Free user. Upgrade to Premium to unlock all features.")
            elif user.get("accountType") == "Premium":
                st.success("✅ You are a Premium user. All features unlocked!")
        elif user["userType"] == "Admin":
            st.info("🛠️ Logged in as Admin. You can manage plants, diseases, fertilizers, and connections.")

        st.markdown("---")
        after_login.after_login()
