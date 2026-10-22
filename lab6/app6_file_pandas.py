import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Analyzer", layout="wide")

st.title("Upload CSV and Analyze")

file = st.file_uploader("Upload a CSV file", type=["csv"])

if file is not None:
    df = pd.read_csv(file)

    st.subheader("Data Preview")
    st.dataframe(df)

    st.subheader("Statistics")
    st.write(df.describe())

    st.subheader("Filter by Column")
    col = st.selectbox("Choose column", df.columns)
    value = st.text_input("Filter value")

    if value:
        filtered = df[
            df[col].astype(str).str.contains(value, case=False, na=False)
        ]
        st.dataframe(filtered)

    st.subheader("Sort Data")
    sort_col = st.selectbox("Sort by", df.columns, key="sort")
    st.dataframe(df.sort_values(sort_col))

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    option = st.radio(
        "Handle missing values",
        ["Keep", "Drop", "Fill with 0"]
    )

    if option == "Drop":
        df = df.dropna()
    elif option == "Fill with 0":
        df = df.fillna(0)

    st.write("Processed Data")
    st.dataframe(df)

    st.subheader("Download Processed CSV")
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="processed.csv",
        mime="text/csv"
    )

    st.subheader("Group By and Aggregate")

    group_col = st.selectbox("Group by column", df.columns)
    num_cols = df.select_dtypes(include="number").columns

    if len(num_cols) > 0:
        agg = df.groupby(group_col)[num_cols].mean()
        st.dataframe(agg)
    else:
        st.write("No numeric columns available for aggregation.")
else:
    st.info("Please upload a CSV file to begin.")