import pandas as pd
import streamlit as st

st.set_page_config(page_title="Min Max", layout="wide")

def convert_df(df):
    return df.to_csv().encode('utf-8')

uploaded_file = st.file_uploader("Choose the .csv file")

df = pd.read_csv(uploaded_file, header=1)

list1 = []

for i in range(len(df)):
  if df['Average Weekly Sales'][i] == 0:
    list1.append(0)
  elif df['Department'][i] == "300 AUTO AND TOOL STORAGE":
    if (df['Average Weekly Sales'][i] * 5)//1 + 1 == (df['Average Weekly Sales'][i] * 5)/1 + 1:
      list1.append((df['Average Weekly Sales'][i] * 5)//1)
    else:
      list1.append((df['Average Weekly Sales'][i] * 5)//1 + 1)
  else:
    if (df['Average Weekly Sales'][i] * 4)//1 + 1 == (df['Average Weekly Sales'][i] * 4)/1 + 1:
      list1.append((df['Average Weekly Sales'][i] * 4)//1)
    else:
      list1.append((df['Average Weekly Sales'][i] * 4)//1 + 1)

df["Min for Upload Supplier Request1"] = list1

list1 = []

for i in range(len(df)):
  if df['Average Weekly Sales'][i] == 0:
    list1.append(0)
  elif df['Department'][i] == "300 AUTO AND TOOL STORAGE":
    if (df['Average Weekly Sales'][i] * 8)//1 + 1 == (df['Average Weekly Sales'][i] * 8)/1 + 1:
      list1.append((df['Average Weekly Sales'][i] * 8)//1)
    else:
      list1.append((df['Average Weekly Sales'][i] * 8)//1 + 1)
  elif df['Department'][i] == "300 PAINT":
    if (df['Average Weekly Sales'][i] * 5)//1 + 1 == (df['Average Weekly Sales'][i] * 5)/1 + 1:
      list1.append((df['Average Weekly Sales'][i] * 5)//1)
    else:
      list1.append((df['Average Weekly Sales'][i] * 5)//1 + 1)
  else:
    if (df['Average Weekly Sales'][i] * 6)//1 + 1 == (df['Average Weekly Sales'][i] * 6)/1 + 1:
      list1.append((df['Average Weekly Sales'][i] * 6)//1)
    else:
      list1.append((df['Average Weekly Sales'][i] * 6)//1 + 1)

df["Max for Upload Supplier Request1"] = list1

list1 = []
for i in range(len(df)):
  list1.append(max(df["Current Min"][i],df["Min for Upload Supplier Request1"][i]))

df["Min for Upload Supplier Request"] = list1

list1 = []
for i in range(len(df)):
  list1.append(max(df["Current Max"][i],df["Max for Upload Supplier Request1"][i]))

df["Max for Upload Supplier Request"] = list1

st.dataframe(df)

csv = convert_df(df)

st.download_button(label="Download data as CSV", data=csv,file_name='Concatenated_files.csv', mime='text/csv')
