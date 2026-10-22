import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Iris Flower Prediction")
st.title("Iris Flower Prediction")

model = joblib.load("model.pkl")
classes = ["Setosa", "Versicolor", "Virginica"]

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("prediction_form"):
    sl = st.slider("Sepal Length", 4.0, 8.0, 5.1)
    sw = st.slider("Sepal Width", 2.0, 4.5, 3.5)
    pl = st.slider("Petal Length", 1.0, 7.0, 1.4)
    pw = st.slider("Petal Width", 0.1, 2.5, 0.2)

    submit = st.form_submit_button("Predict")

if submit:
    features = np.array([[sl, sw, pl, pw]])

    pred = model.predict(features)[0]
    proba = model.predict_proba(features)[0]

    st.success(f"Prediction: {classes[pred]}")
    st.metric("Confidence", f"{max(proba) * 100:.1f}%")

    st.subheader("Class Probabilities")
    probability_df = pd.DataFrame({
        "Class": classes,
        "Probability": proba
    })
    st.bar_chart(probability_df.set_index("Class"))

    st.session_state.history.append({
        "Sepal Length": sl,
        "Sepal Width": sw,
        "Petal Length": pl,
        "Petal Width": pw,
        "Prediction": classes[pred]
    })

st.subheader("Prediction History")

if st.session_state.history:
    st.dataframe(
        pd.DataFrame(st.session_state.history),
        use_container_width=True
    )
else:
    st.info("No predictions yet.")

st.subheader("Model Comparison")

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

lr_model = LogisticRegression(max_iter=200)
lr_model.fit(X_train, y_train)

rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test))
lr_accuracy = accuracy_score(y_test, lr_model.predict(X_test))

comparison = pd.DataFrame({
    "Model": ["Random Forest", "Logistic Regression"],
    "Accuracy": [rf_accuracy, lr_accuracy]
})

st.dataframe(comparison, use_container_width=True)
st.bar_chart(comparison.set_index("Model"))