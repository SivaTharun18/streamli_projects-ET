import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Layouts Demo", layout="wide")

st.title("Layouts Demo")

# Sidebar
st.sidebar.header("Settings")
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"])
font_size = st.sidebar.slider("Font Size", 10, 30, 15)

st.sidebar.write("Selected Theme:", theme)
st.sidebar.write("Font Size:", font_size)

# Two columns
col1, col2 = st.columns(2)

with col1:
    st.metric("Total Sales", "25 Lakh")

with col2:
    st.metric("Customers", "1,200")

# Three columns with different widths
c1, c2, c3 = st.columns([1, 2, 1])

with c1:
    st.write("Left (narrow)")

with c2:
    st.write("Center (wide)")

with c3:
    st.write("Right (narrow)")

# Data for charts
df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

# Tabs with charts
tab1, tab2, tab3 = st.tabs(["Overview", "Analysis", "About"])

with tab1:
    st.subheader("Overview")
    st.write("Overview content here")
    st.line_chart(df)

with tab2:
    st.subheader("Analysis")
    st.write("Analysis content here")
    st.bar_chart(df)

with tab3:
    st.subheader("About")
    st.write("About this app")
    st.write("This app demonstrates Streamlit layouts.")

# Container
with st.container():
    st.subheader("Grouped Section")
    st.write("All these elements are inside one container.")

# Expander
with st.expander("Details"):
    st.write("This content is hidden until expanded.")
    st.write("You can put anything here.")