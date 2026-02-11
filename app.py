import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excise Dashboard", layout="wide")

st.title("Excise Dashboard")
st.write("Upload your file")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, on_bad_lines="skip")
    else:
        df = pd.read_excel(uploaded_file)

    st.dataframe(df.head())
