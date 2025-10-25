import json
import os
import streamlit as st

# Admin users list
adminUser = [
    {"username": "aaqif", "password": "newproject", "userType": "Admin"},
    {"username": "kavindu", "password": "newprojects", "userType": "Admin"}
]

USER_FILE = "users.json"

# ------------------- Lookup Functions -------------------

def find_diseases_by_plant(plant_name, diseases):
    plant_name = plant_name.strip().lower()
    found_diseases = []
    for d in diseases:
        if plant_name in [p.lower() for p in d["Plants Affected"]]:
            found_diseases.append(d["Disease Name"])
    return found_diseases

def find_plants_by_disease(disease_name, diseases):
    disease_name = disease_name.strip().lower()
    for d in diseases:
        if d["Disease Name"].lower() == disease_name:
            return d["Plants Affected"]
    return []

def find_diseases_by_fertilizer(fertilizer_name, fertilizers):
    fertilizer_name = fertilizer_name.strip().lower()
    for f in fertilizers:
        if f["FertilizerName"].lower() == fertilizer_name:
            return f["Diseases Treated"]
    return []

def find_fertilizers_by_disease(disease_name, fertilizers):
    disease_name = disease_name.strip().lower()
    matched_fertilizers = []
    for f in fertilizers:
        if disease_name in [d.lower() for d in f["Diseases Treated"]]:
            matched_fertilizers.append(f["FertilizerName"])
    return matched_fertilizers

# ------------------- User Functions -------------------

def load_users():
    if os.path.exists(USER_FILE) and os.path.getsize(USER_FILE) > 0:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ------------------- Streamlit Pages -------------------

def login_page():
    st.subheader("🔑 Login Page")
    username = st.text_input("Enter Username")
    password = st.text_input("Enter Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enter", use_container_width=True, key="login_enter"):
            admin_found = next((admin for admin in adminUser if username == admin["username"] and password == admin["password"]), None)
            if admin_found:
                st.session_state.loggeduser = admin_found
                st.session_state.current_page = "Home"
                st.success(f"Successfully logged in as Admin ✅")
                st.rerun()
            else:
                users = load_users()
                user_found = next((user for user in users if user["username"] == username and user["password"] == password), None)
                if user_found:
                    st.session_state.loggeduser = user_found
                    if "accountType" not in user_found:
                        user_found["accountType"] = "Free"
                    st.session_state.loggeduser["accountType"] = user_found["accountType"]
                    st.session_state.current_page = "Home"
                    st.success(f"Successfully logged in as {user_found['username']} ({user_found['accountType']}) ✅")
                    st.rerun()
                else:
                    st.error("Invalid User Credentials, Try again.")
    
    with col2:
        if st.button("Back to Home", use_container_width=True, key="login_back"):
            st.session_state.current_page = "Home"
            st.rerun()

def signup_page():
    st.subheader("📝 Sign Up Page")
    new_username = st.text_input("Create a new username")
    new_password = st.text_input("Create a new password", type="password")
    mobile_no = st.text_input("Mobile Number")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register", use_container_width=True, key="signup_register"):
            users = load_users()
            if not new_username or not new_password or not mobile_no:
                st.error("Please fill in all fields ❌")
            elif len(new_username) < 5:
                st.error("Username must be at least 5 characters ❌")
            elif len(new_password) < 7:
                st.error("Password must be at least 7 characters ❌")
            elif any(user["username"] == new_username for user in users):
                st.error("Username already exists ❌")
            else:
                users.append({
                    "username": new_username,
                    "password": new_password,
                    "mobile": mobile_no,
                    "userType": "User",
                    "accountType": "Free"
                })
                save_users(users)
                st.success("Account created Successfully ✅ Please log in.")
                st.session_state.current_page = "Login"  # Redirect to login page
                st.rerun()
    
    with col2:
        if st.button("Back to Home", use_container_width=True, key="signup_back"):
            st.session_state.current_page = "Home"
            st.rerun()

# ------------------- About Us Page -------------------

def about_us():
    st.title("🌿 AgriNest - About Us")
    
    # Short introduction
    st.subheader("💡 Empowering Farmers with Smart Agriculture")
    st.write("""
    Welcome to **AgriNest**, your friendly helper for all farming needs! 
    AgriNest is a **Streamlit-based Python web application** designed to provide farmers 
    and agriculture enthusiasts with detailed information about **plants, diseases, and fertilizers**.
    """)

    # Comprehensive description
    st.write("""
    Our application serves **three types of users**: Free users, Premium users, and Admins.
    """)

    # Free User Features
    st.markdown("### 🆓 Free User Features")
    st.write("""
    Free users have access to the basic functionality:
    - Search for diseases associated with a specific plant.
    - Search for plants affected by a specific disease.
    """)

    # Premium User Features
    st.markdown("### 💎 Premium User Features")
    st.write("""
    Premium users have **all the free user features**, plus additional benefits:
    - View detailed information about plants and their associated diseases.
    - Find fertilizers that can treat a particular disease.
    - Discover diseases that can be treated with a specific fertilizer.
    - Purchase fertilizers directly through the app.
    """)

    # Admin Features
    st.markdown("### 🛠️ Admin Features")
    st.write("""
    Admins have **complete control** over the application's data and functionalities:
    - Manage the **Plant Table** (add, edit, delete plants).
    - Manage the **Disease Table** (add, edit, delete diseases).
    - Manage the **Fertilizer Table** and catalog (add, edit, delete fertilizers).
    - Control premium and free user access and features.
    """)

    # Closing statement
    st.write("""
    AgriNest is designed to **simplify farming decisions**, empower users with accurate 
    agricultural knowledge, and make fertilizer management easier than ever.  
    Whether you're a casual user, a dedicated premium subscriber, or an admin managing the system, 
    AgriNest has the tools you need.
    """)

# ------------------- Our Team Page -------------------

def our_team():
    st.title("👥 Our Team")
    st.write("Meet the amazing team behind **AgriNest**!")

    # Team member details
    team_members = [
        {"name": "Aaqif Ahamed", "cpm": "26993", "image": None},
        {"name": "Miyuru Malshan", "cpm": "26992", "image": None},
        {"name": "Kavindu Theekshana", "cpm": "26991", "image": None},
        {"name": "Muhammad Saheeth", "cpm": "26987", "image": None},
        {"name": "V. Harithas", "cpm": "26985", "image": None},
    ]

    # Display team members one by one
    for member in team_members:
        col1, col2 = st.columns([1, 3])  # Image on left, text on right
        with col1:
            # Circular placeholder image with fixed 200x200 px size
            st.image(
                "https://via.placeholder.com/200",
                width=200,  # fixed width
                caption=None
            )
        with col2:
            st.subheader(member["name"])
            st.write(f"CPM: {member['cpm']}")
        st.markdown("---")  # Separator line between members

# ------------------- Upgrade to Premium -------------------

def upgrade_to_premium(user):
    st.markdown("### 💳 Upgrade to Premium")
    st.info("Premium users can access advanced features like portalization.")

    # Use session state to track if button clicked
    if 'show_ref_input' not in st.session_state:
        st.session_state.show_ref_input = False

    if st.button("Upgrade to Premium"):
        st.session_state.show_ref_input = True

    if st.session_state.show_ref_input:
        reference_code = st.text_input("Enter Reference Number to Unlock Premium Features", key="ref_code")
        if st.button("Submit Reference Number", key="submit_ref"):
            if reference_code == "AAQ2004":
                user["accountType"] = "Premium"
                all_users = load_users()
                for u in all_users:
                    if u["username"] == user["username"]:
                        u["accountType"] = "Premium"
                save_users(all_users)
                st.success("✅ Premium Features Unlocked! You now have full access.")
                st.rerun()
            else:
                st.error("❌ Invalid Reference Number. Please try again.")
