import streamlit as st
from datetime import date

st.title("Widgets Playground")

# Basic Widgets
name = st.text_input("Name")
age = st.number_input("Age", min_value=1, max_value=100, value=20)
marks = st.slider("Marks", 0, 100, 75)
city = st.selectbox("City", ["Chennai", "Mumbai", "Delhi"])
skills = st.multiselect("Skills", ["Python", "ML", "SQL", "Streamlit"])
gender = st.radio("Gender", ["Male", "Female", "Other"])
agree = st.checkbox("I agree to terms")
dob = st.date_input("Date of Birth", date(2000, 1, 1))
file = st.file_uploader("Upload a file")

# Exercise 1: Color Picker
color = st.color_picker("Pick a color", "#00FF00")
st.write("Selected color:", color)

# Exercise 2: Select Slider
marks_range = st.select_slider(
    "Select a range of marks",
    options=list(range(0, 101)),
    value=(40, 80)
)
st.write("Range:", marks_range)

# Submit Button
if st.button("Submit"):
    st.write("Name:", name)
    st.write("Age:", age)
    st.write("Marks:", marks)
    st.write("City:", city)
    st.write("Skills:", skills)
    st.write("Gender:", gender)
    st.write("Agreed:", agree)
    st.write("DOB:", dob)

    if file is not None:
        st.write("File uploaded:", file.name)

# Exercise 3: Widget Value Types
st.subheader("Widget Value Types")

st.write("Name type:", type(name).__name__)
st.write("Age type:", type(age).__name__)
st.write("Marks type:", type(marks).__name__)
st.write("City type:", type(city).__name__)
st.write("Skills type:", type(skills).__name__)
st.write("Gender type:", type(gender).__name__)
st.write("Agree type:", type(agree).__name__)
st.write("DOB type:", type(dob).__name__)

if file is not None:
    st.write("File type:", type(file).__name__)