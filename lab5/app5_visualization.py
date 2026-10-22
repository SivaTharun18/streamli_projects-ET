import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Data Visualization")

# Sample Data
df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Math", "Science", "English"]
)

st.subheader("Sample Data")
st.dataframe(df)

# Average Math Score
st.subheader("Average Score")
st.metric("Average Math Score", f"{df['Math'].mean():.2f}")

# Built-in Charts
st.header("Built-in Charts")

st.subheader("Line Chart")
st.line_chart(df)

st.subheader("Bar Chart")
st.bar_chart(df)

st.subheader("Area Chart")
st.area_chart(df)

# Matplotlib Chart
st.header("Matplotlib Visualization")
st.subheader("Math Score Distribution")

fig, ax = plt.subplots()
ax.hist(df["Math"], bins=10, color="skyblue", edgecolor="black")
ax.set_title("Math Score Distribution")
ax.set_xlabel("Math Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)
plt.close(fig)

# Plotly Chart
st.header("Plotly Visualization")
st.subheader("Math Distribution")

fig = px.histogram(
    df,
    x="Math",
    nbins=10,
    title="Math Distribution"
)
st.plotly_chart(fig, use_container_width=True)

# Scatter Plot
st.header("Relationship Between Subjects")
st.subheader("Math vs Science")

st.scatter_chart(df, x="Math", y="Science")