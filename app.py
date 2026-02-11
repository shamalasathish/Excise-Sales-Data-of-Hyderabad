{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww33400\viewh18060\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
\
st.set_page_config(page_title="Excise Dashboard", layout="wide")\
\
st.title("\uc0\u55357 \u56522  Excise Data Dashboard")\
\
# ---- File Upload ----\
uploaded_file = st.file_uploader("Upload your data file", type=["csv", "xlsx"])\
\
@st.cache_data\
def load_data(file):\
    if file.name.endswith(".csv"):\
        return pd.read_csv(file, on_bad_lines="skip")  # Handles inconsistent rows\
    else:\
        return pd.read_excel(file)\
\
if uploaded_file:\
    df = load_data(uploaded_file)\
\
    st.success("Data Loaded Successfully")\
\
    st.write("### Data Preview")\
    st.dataframe(df.head())\
\
    # ---- Sidebar Filters ----\
    st.sidebar.header("Filters")\
\
    column_list = df.columns.tolist()\
    selected_column = st.sidebar.selectbox("Select column to filter", column_list)\
\
    unique_values = df[selected_column].dropna().unique()\
    selected_values = st.sidebar.multiselect(\
        "Select values", unique_values, default=unique_values[:5]\
    )\
\
    filtered_df = df[df[selected_column].isin(selected_values)]\
\
    st.write("### Filtered Data")\
    st.dataframe(filtered_df)\
\
    # ---- Basic Metrics ----\
    st.write("### Key Metrics")\
    col1, col2, col3 = st.columns(3)\
\
    col1.metric("Total Records", len(filtered_df))\
    col2.metric("Columns", len(df.columns))\
    col3.metric("Unique Values", filtered_df[selected_column].nunique())\
\
    # ---- Charts ----\
    st.write("### Visualization")\
\
    numeric_cols = df.select_dtypes(include="number").columns.tolist()\
\
    if numeric_cols:\
        chart_col = st.selectbox("Select numeric column", numeric_cols)\
\
        chart_data = filtered_df.groupby(selected_column)[chart_col].sum()\
\
        st.bar_chart(chart_data)\
\
else:\
    st.info("Please upload a CSV or Excel file to begin.")\
}