import streamlit as st
import pandas as pd

from db import (
    init_db,
    create_user,
    get_user_by_username,
    get_all_users,
    user_exists
)

from auth import (
    hash_password,
    verify_password,
    validate_username,
    validate_email,
    validate_password
)

st.set_page_config(page_title="Login Signup App", page_icon="🔐")

try:
    init_db()
except Exception as e:
    st.error("Could not connect to PostgreSQL.")
    st.info("Check your database settings in secrets.toml.")
    st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


def signup_page():
    st.title("Create Account")

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")

    if submit:
        username = username.strip()
        email = email.strip()

        ok, msg = validate_username(username)
        if not ok:
            st.error(msg)
            return

        ok, msg = validate_email(email)
        if not ok:
            st.error(msg)
            return

        ok, msg = validate_password(password)
        if not ok:
            st.error(msg)
            return

        if password != confirm:
            st.error("Passwords do not match.")
            return

        if user_exists(username=username):
            st.error("Username already exists.")
            return

        if user_exists(email=email):
            st.error("Email already registered.")
            return

        if create_user(username, email, hash_password(password)):
            st.success("Account created! Please log in.")
        else:
            st.error("Username or email already exists.")


def login_page():
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        user = get_user_by_username(username.strip())

        if user and verify_password(
            password, user["password_hash"]
        ):
            st.session_state.logged_in = True
            st.session_state.user = {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "created_at": user["created_at"]
            }
            st.rerun()
        else:
            st.error("Invalid username or password.")


def dashboard_page():
    user = st.session_state.user

    st.title(f"Welcome, {user['username']}!")

    col1, col2 = st.columns(2)
    col1.metric("User ID", user["id"])
    col2.metric("Username", user["username"])

    st.write("Email:", user["email"])
    st.write(
        "Joined:",
        user["created_at"].strftime("%Y-%m-%d %H:%M")
    )

    st.markdown("---")
    st.subheader("Registered Users")

    users = get_all_users()

    if users:
        df = pd.DataFrame(users)
        df["created_at"] = pd.to_datetime(
            df["created_at"]
        ).dt.strftime("%Y-%m-%d %H:%M")

        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users registered yet.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


if st.session_state.logged_in:
    dashboard_page()
else:
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        login_page()

    with tab2:
        signup_page()