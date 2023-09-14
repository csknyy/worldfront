import pandas as pd
import streamlit as st

st.set_page_config(page_title="Min Max", layout="wide")

def convert_df(df):
    return df.to_csv().encode('utf-8')

uploaded_file = st.file_uploader("Choose the .csv file")

dataframe = pd.read_csv(uploaded_file, header=1)

list1 = []

for i in range(len(dataframe)):
  if dataframe['Average Weekly Sales'][i] == 0:
    list1.append(0)
  elif dataframe['Department'][i] == "300 AUTO AND TOOL STORAGE":
    if (dataframe['Average Weekly Sales'][i] * 5)//1 + 1 == (dataframe['Average Weekly Sales'][i] * 5)/1 + 1:
      list1.append((dataframe['Average Weekly Sales'][i] * 5)//1)
    else:
      list1.append((dataframe['Average Weekly Sales'][i] * 5)//1 + 1)
  else:
    if (dataframe['Average Weekly Sales'][i] * 4)//1 + 1 == (dataframe['Average Weekly Sales'][i] * 4)/1 + 1:
      list1.append((dataframe['Average Weekly Sales'][i] * 4)//1)
    else:
      list1.append((dataframe['Average Weekly Sales'][i] * 4)//1 + 1)

dataframe["Min for Upload Supplier Request1"] = list1

list1 = []

for i in range(len(dataframe)):
  if dataframe['Average Weekly Sales'][i] == 0:
    list1.append(0)
  elif dataframe['Department'][i] == "300 AUTO AND TOOL STORAGE":
    if (dataframe['Average Weekly Sales'][i] * 8)//1 + 1 == (dataframe['Average Weekly Sales'][i] * 8)/1 + 1:
      list1.append((dataframe['Average Weekly Sales'][i] * 8)//1)
    else:
      list1.append((dataframe['Average Weekly Sales'][i] * 8)//1 + 1)
  elif dataframe['Department'][i] == "300 PAINT":
    if (dataframe['Average Weekly Sales'][i] * 5)//1 + 1 == (dataframe['Average Weekly Sales'][i] * 5)/1 + 1:
      list1.append((dataframe['Average Weekly Sales'][i] * 5)//1)
    else:
      list1.append((dataframe['Average Weekly Sales'][i] * 5)//1 + 1)
  else:
    if (dataframe['Average Weekly Sales'][i] * 6)//1 + 1 == (dataframe['Average Weekly Sales'][i] * 6)/1 + 1:
      list1.append((dataframe['Average Weekly Sales'][i] * 6)//1)
    else:
      list1.append((dataframe['Average Weekly Sales'][i] * 6)//1 + 1)

dataframe["Max for Upload Supplier Request1"] = list1

list1 = []
for i in range(len(dataframe)):
  list1.append(max(dataframe["Current Min"][i],dataframe["Min for Upload Supplier Request1"][i]))

dataframe["Min for Upload Supplier Request"] = list1

list1 = []
for i in range(len(dataframe)):
  list1.append(max(dataframe["Current Max"][i],dataframe["Max for Upload Supplier Request1"][i]))

dataframe["Max for Upload Supplier Request"] = list1

st.dataframe(result)

csv = convert_df(result)

st.download_button(label="Download data as CSV", data=csv,file_name='Concatenated_files.csv', mime='text/csv')
