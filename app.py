import re
import random
import string
import streamlit as st

# List of common weak passwords
COMMON_PASSWORDS = {"rehmat", "123456", "1234567890", "0987654321", "12345", "hello", "xyz12345", "abc123", "abc12345"}

def evaluate_password_strength(password: str) -> tuple:
    score = 0
    feedback = []
    color = "#5d1049"  # Default color to avoid UnboundLocalError
    
    if password.lower() in COMMON_PASSWORDS:
        return "Very Weak", ["This password is too common and easily guessable. Choose a different one."], "#c0392b"  

    weights = {
        "length": 2 if len(password) >= 12 else 1,
        "uppercase": 1,
        "lowercase": 1,
        "digit": 1,
        "special": 2
    }
    
    if len(password) >= 8:
        score += weights["length"]
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    if re.search(r"[A-Z]", password):
        score += weights["uppercase"]
    else:
        feedback.append("Add at least one uppercase letter.")
    
    if re.search(r"[a-z]", password):
        score += weights["lowercase"]
    else:
        feedback.append("Add at least one lowercase letter.")
    
    if re.search(r"\d", password):
        score += weights["digit"]
    else:
        feedback.append("Include at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += weights["special"]
    else:
        feedback.append("Use at least one special character (!@#$%^&*).")
    
    if score <= 2:
        strength = "Weak"
        color = "#e30425"  # Red
    elif score <= 4:
        strength = "Moderate"
        color = "#FF9F0D"  # Orange
    elif score <= 6:
        strength = "Strong"
        color = "#4edd3a"  # Green
    else:
        strength = "Very Strong"
        color = "#720d5d"  # Dark Purple
        feedback = ["Your password is very strong!"]
    
    return strength, feedback, color


def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))


# Updated Styling
st.markdown(
    """
    <style>
    html, body, .stApp {
        color: black !important;
        background-color: #FFB6C1 !important; /* Light Pink */
    }

    .stTextInput input {
        font-size: 18px !important;
        padding: 12px !important;
        border-radius: 10px !important;
        border: 2px solid #5d1049 !important;
        background-color: white !important;
        color: black !important;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(93, 16, 73, 0.3);
    }

    .stButton button {
        font-size: 18px !important;
        padding: 12px !important;
        border-radius: 10px !important;
        background: linear-gradient(to right, #720d5d, #5d1049);
        color: white !important;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        box-shadow: 0px 5px 15px rgba(114, 13, 93, 0.6);
    }

    .stButton button:hover {
        background: linear-gradient(to right, #5d1049, #720d5d);
        transform: scale(1.05);
        box-shadow: 0px 5px 20px rgba(114, 13, 93, 0.6);
    }

    .navbar {
        background: linear-gradient(to right, #720d5d, #5d1049);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: white !important;
        margin-bottom: 30px;
        box-shadow: 0px 5px 15px rgba(114, 13, 93, 0.5);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #FFB6C1 !important;
        color: black !important;
        border-right: 2px solid #5d1049;
    }

    h3 {
        color: #5d1049 !important;
    }

    .stMarkdown h3 {
        font-weight: bold !important;
        font-size: 22px !important;
    }
</style>

    """,
    unsafe_allow_html=True
)

# Navbar
st.markdown('<div class="navbar">🔐 Secure Password Analyzer</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["Password Strength Checker", "Password Generator"])


# 🔒 Password Strength Checker Page
def password_strength_page():
    st.title("🔒 Password Strength Meter")
    password = st.text_input("Enter a password:", type="password")

    if password.strip():  # Ensure password is not empty
        strength, feedback, color = evaluate_password_strength(password)
        st.markdown(f'<h3 style="color:{color};">Password Strength: {strength}</h3>', unsafe_allow_html=True)
        for msg in feedback:
            st.warning(msg)
        
        if strength == "Weak" or strength == "Very Weak":
            st.write("💡 Suggested Strong Password:", generate_strong_password())
    else:
        st.warning("Please enter a password to check its strength.")


# 🔑 Password Generator Page
def password_generator_page():
    st.title("🔑 Generate a Strong Password")
    length = st.slider("Select password length:", 8, 20, 12)
    if st.button("Generate Password"):
        password = generate_strong_password(length)
        st.success(f"Generated Password: `{password}`")


# Handle Navigation
if page == "Password Strength Checker":
    password_strength_page()
elif page == "Password Generator":
    password_generator_page()

