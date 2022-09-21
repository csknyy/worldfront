import pandas as pd
import streamlit as st

st.set_page_config(page_title="Amazon orders", layout="wide")

data = pd.DataFrame(columns=['A'], index=[0])

file = st.file_uploader("Drag and drop a file")

st.dataframe(data)
