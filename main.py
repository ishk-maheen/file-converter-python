import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload CSV and Excel files, clean data, and convert formats.")

files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        file_name = file.name
        ext = file_name.split(".")[-1]
        
        # File reading with correct conditions
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file, engine="openpyxl")  # Explicitly define engine for Excel

        # Show preview of the uploaded file
        st.subheader(f"Preview of {file_name}")
        st.dataframe(df.head())

        # Remove Duplicates
        if st.checkbox(f"Remove Duplicates - {file_name}"):
            df = df.drop_duplicates()
            st.success("Duplicates removed")
            st.dataframe(df.head())

        # Fill Missing Values
        if st.checkbox(f"Fill Missing Values - {file_name}"):
            df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
            st.success("Missing values filled with column means")
            st.dataframe(df.head())

        # Select Columns
        selected_columns = st.multiselect(f"Select Columns to Keep - {file_name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart only if numeric columns exist
        if not df.select_dtypes(include="number").empty:
            if st.checkbox(f"Show Chart - {file_name}"):
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # File conversion options
        format_choice = st.radio(f"Convert {file_name} to:", ["csv", "Excel"], key=file_name)

        if st.button(f"Download {file_name} as {format_choice}"):
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file_name.replace(ext, "csv")
            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file_name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download File", file_name=new_name, data=output, mime=mime)

        st.success(f"Processing Complete for {file_name}!")

