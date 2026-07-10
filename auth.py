import streamlit as st
import re
from database import db


# -----------------------------
# Session Initialization
# -----------------------------
def initialize_session():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "user" not in st.session_state:
        st.session_state.user = None


# -----------------------------
# Email Validation
# -----------------------------
def valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)


# -----------------------------
# Password Validation
# -----------------------------
def strong_password(password):

    if len(password) < 8:
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    return True


# -----------------------------
# Registration Page
# -----------------------------
def register():

    st.title("🚌 Smart Public Transport Assistant")

    st.subheader("Create Account")

    fullname = st.text_input("Full Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone Number")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register", use_container_width=True):

        if fullname == "" or email == "" or phone == "" or password == "":
            st.error("Please fill all fields.")
            return

        if not valid_email(email):
            st.error("Invalid Email Address")
            return

        if not strong_password(password):
            st.warning("""
Password must contain

• Minimum 8 characters

• One uppercase letter

• One lowercase letter

• One number
""")
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        success, message = db.register_user(
            fullname,
            email,
            phone,
            password
        )

        if success:
            st.success(message)
        else:
            st.error(message)


# -----------------------------
# Login Page
# -----------------------------
def login():

    st.title("🚌 Smart Public Transport Assistant")

    st.subheader("Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login", use_container_width=True):

        user = db.login_user(
            email,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.user = {
                "id": user[0],
                "fullname": user[1],
                "email": user[2],
                "phone": user[3],
                "created": user[5]
            }

            st.success("Login Successful")

            st.rerun()

        else:

            st.error("Invalid Email or Password")


# -----------------------------
# User Profile
# -----------------------------
def profile():

    user = st.session_state.user

    st.title("👤 User Profile")

    st.write("### Personal Information")

    st.write(f"**Name:** {user['fullname']}")

    st.write(f"**Email:** {user['email']}")

    st.write(f"**Phone:** {user['phone']}")

    st.write(f"**Joined:** {user['created']}")


# -----------------------------
# Logout
# -----------------------------
def logout():

    st.session_state.logged_in = False

    st.session_state.user = None

    st.success("Logged Out Successfully")

    st.rerun()