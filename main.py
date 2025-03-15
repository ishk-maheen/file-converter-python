import streamlit as st
import pandas as pd 
from io import BytesIO

st.set_page_config(page_title="File Converter",layout="wide")
st.title("File Converter & Cleaner")
st.write("Upload csv and excel files, clean data and convert formats.")

files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files: 
    for file in files:
        file_name=file.name
        ext = file.name.split(".")[-1]
        
    if ext == "csv":
        df = pd.read_csv(file) 
        
    else: 
        df = pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Remove Duplicates - {file.name}"): 
            df=df.drop_duplicates()
            st.success("Duplicates removed")
            st.dataframe(df.head())

            if st.checkbox(f"File Missing values {file.name}"):
                df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.success("Missing values filled with mean")
                st.dataframe(df.head()) 

            selected_columns = st.multiselect(f"Selected columns - {file.name}", df.columns,default=df.columns)
            df= df[selected_columns]
            st.dataframe(df.head())

            if st.checkbox(f"Show chart - {file.name}") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            format_choice = st.radio(f"Convert {file.name} to:", ["csv" , "Excel"], key=file.name)

            if st.button(f"Download {file.name} as {format_choice}"):
                output = BytesIO()
                if format_choice == "csv":
                    df.to_csv(output, index=False)
                    mime = "text/csv"
                    new_name = file_name.replace(ext,"csv")
                
                else:
                    df.to_excel(output, index=False,engine="openpyxl")
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file_name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button("Download file",file_name= new_name, data=output, mime=mime)

            st.success("Processing Complete!")