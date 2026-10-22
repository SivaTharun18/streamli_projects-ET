import streamlit as st

st.title("Forms + Session State")

# Counter
if "count" not in st.session_state:
    st.session_state.count = 0

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Increment"):
        st.session_state.count += 1

with col2:
    if st.button("Add 5"):
        st.session_state.count += 5

with col3:
    if st.button("Reset Counter"):
        st.session_state.count = 0

st.write("Counter:", st.session_state.count)

st.divider()

# Login form
st.subheader("Login Form")

with st.form("login_form"):
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if user == "admin" and pwd == "1234":
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid credentials")

if st.session_state.get("logged_in", False):
    st.info("Welcome, admin! You are now logged in.")

st.divider()

# To-do list
if "todos" not in st.session_state:
    st.session_state.todos = []

st.subheader("To-Do List")

with st.form("todo_form", clear_on_submit=True):
    task = st.text_input("New Task")
    add = st.form_submit_button("Add Task")

if add and task.strip():
    st.session_state.todos.append(task.strip())

st.write("Your Tasks")

if st.session_state.todos:
    for i, t in enumerate(st.session_state.todos, start=1):
        st.write(f"{i}. {t}")
else:
    st.write("No tasks added yet.")

if st.button("Clear All"):
    st.session_state.todos = []