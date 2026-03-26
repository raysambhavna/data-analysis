import streamlit as st
import pandas as pd
import numpy as np
import io
import pickle

from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score

# ------------------------------
# PAGE CONFIG
# ------------------------------ 
st.set_page_config(
    page_title="Smart Dataset Analyzer",
    layout="wide"
)

st.title("📊 Smart Dataset Analyzer & Auto-ML Assistant")
st.write("Upload any dataset → Analyze → Train ML models → Compare results")


# ------------------------------
# FILE UPLOAD
# ------------------------------
uploaded_file = st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

df = None

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        st.write("value error")

    st.subheader("🔍 Dataset Preview")
    st.dataframe(df.head())
    st.write("Shape:", df.shape)

if df is not None:
    if st.checkbox("Generate EDA Report (Slow)"):
        profile = ProfileReport(df, minimal=True)
        st.write("Report generated")

    st.subheader("📈 Automated EDA (YData Profiling)")

    if "profile_html" not in st.session_state:
        st.session_state.profile_html = None

    if st.button("Generate Profiling Report"):
        with st.spinner("Generating report..."):
            profile = ProfileReport(df, explorative=True)
            st.session_state.profile_html = profile.to_html()

    if st.session_state.profile_html:
        with st.expander("View Profiling Report", expanded=False):
            html(st.session_state.profile_html, height=700, scrolling=True)

    st.subheader("🎯 Select Target Column")
    target_col = st.selectbox("Choose target column", df.columns)

    X = df.drop(columns=[target_col])
    y = df[target_col]

    if y.dtype == "object" or y.nunique() < 10:
        problem_type = "Classification"
    else:
        problem_type = "Regression"

    st.success(f"Detected Problem Type: {problem_type}")

    categorical_cols = X.select_dtypes(include=["object"]).columns
    numeric_cols = X.select_dtypes(include=np.number).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    st.subheader("🤖 Train Machine Learning Models")

    if st.button("Train Model"):
        if problem_type == "Classification":
            model = RandomForestClassifier(random_state=42)
            pipeline = Pipeline([
                ("preprocess", preprocessor),
                ("model", model)
            ])

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            acc = accuracy_score(y_test, preds)
            f1 = f1_score(y_test, preds, average="weighted")

            st.success("Model trained successfully")
            st.write(f"Accuracy: {acc:.3f}")
            st.write(f"F1 Score: {f1:.3f}")
        else:
            model = RandomForestRegressor(random_state=42)
            pipeline = Pipeline([
                ("preprocess", preprocessor),
                ("model", model)
            ])

            pipeline.fit(X_train, y_train)
            preds = pipeline.predict(X_test)

            rmse = np.sqrt(mean_squared_error(y_test, preds))
            r2 = r2_score(y_test, preds)

            st.success("Model trained successfully")
            st.write(f"RMSE: {rmse:.3f}")
            st.write(f"R² Score: {r2:.3f}")

        model_buffer = io.BytesIO()
        pickle.dump(pipeline, model_buffer)
        model_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Trained Model",
            data=model_buffer,
            file_name="trained_model.pkl",
            mime="application/octet-stream"
        )

        st.success("Training completed successfully!")