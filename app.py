import streamlit as st
import pandas as pd

st.set_page_config(page_title="Excise Dashboard", layout="wide")

st.title("📊 Excise Data Dashboard")

uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file:

    # ---- Load Data ----
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, on_bad_lines="skip")
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Data Loaded Successfully")

    # ---- Sidebar ----
    st.sidebar.header("🔎 Filters")

    filter_column = st.sidebar.selectbox("Select Column", df.columns)

    unique_vals = df[filter_column].dropna().unique()
    selected_vals = st.sidebar.multiselect(
        "Select Values",
        unique_vals,
        default=unique_vals[:5]
    )

    filtered_df = df[df[filter_column].isin(selected_vals)]

    # ---- KPIs ----
    st.write("## 📌 Key Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(filtered_df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Unique Categories", filtered_df[filter_column].nunique())

    st.divider()

    # ---- Charts Section ----
    st.write("## 📈 Visual Analysis")

    numeric_cols = filtered_df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        chart_column = st.selectbox("Select Numeric Column", numeric_cols)

        chart_data = (
            filtered_df
            .groupby(filter_column)[chart_column]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(chart_data)

        st.line_chart(chart_data)

    else:
        st.warning("⚠ No numeric columns detected for visualization")

    st.divider()

    # ---- Data Table ----
    st.write("## 🗂 Filtered Data View")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info("⬆ Upload a file to start dashboard")
