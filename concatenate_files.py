import pandas as pd
import streamlit as st

st.set_page_config(page_title="Concatenate files", layout="wide")

def convert_df(df):
    return df.to_csv().encode('utf-8')

uploaded_files = st.file_uploader("Choose the CSV files", accept_multiple_files=True)
file_count = len(uploaded_files)

files = [f"file{i}" for i in range(int(file_count))]

i=0
for uploaded_file,file in zip(uploaded_files,files):
    file = pd.read_csv(uploaded_file)
    files[i] = file
    st.write("Uploaded:", uploaded_file.name)
    i = i+1

st.header("Concatenated dataframes")
result = pd.concat(files)

result = result.iloc[:, 1:]

st.dataframe(result)

csv = convert_df(result)

st.download_button(label="Download data as CSV", data=csv,file_name='Concatenated_files.csv', mime='text/csv')
