import pandas as pd
import streamlit as st

st.set_page_config(page_title="Min Max", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file = st.file_uploader("Choose the .csv file")

data = pd.read_excel(uploaded_file, header=1)

list1 = []

for i in range(len(data)):
  if data['Average Weekly Sales'][i] == 0:
    list1.append(0)
  elif data['Department'][i] == "300 AUTO AND TOOL STORAGE":
    if (data['Average Weekly Sales'][i] * 5)//1 + 1 == (data['Average Weekly Sales'][i] * 5)/1 + 1:
      list1.append((data['Average Weekly Sales'][i] * 5)//1)
    else:
      list1.append((data['Average Weekly Sales'][i] * 5)//1 + 1)
  else:
    if (data['Average Weekly Sales'][i] * 4)//1 + 1 == (data['Average Weekly Sales'][i] * 4)/1 + 1:
      list1.append((data['Average Weekly Sales'][i] * 4)//1)
    else:
      list1.append((data['Average Weekly Sales'][i] * 4)//1 + 1)

data["Min for Upload Supplier Request1"] = list1

list1 = []

for i in range(len(data)):
  if data['Average Weekly Sales'][i] == 0:
    list1.append(0)
  elif data['Department'][i] == "300 AUTO AND TOOL STORAGE":
    if (data['Average Weekly Sales'][i] * 8)//1 + 1 == (data['Average Weekly Sales'][i] * 8)/1 + 1:
      list1.append((data['Average Weekly Sales'][i] * 8)//1)
    else:
      list1.append((data['Average Weekly Sales'][i] * 8)//1 + 1)
  elif data['Department'][i] == "300 PAINT":
    if (data['Average Weekly Sales'][i] * 5)//1 + 1 == (data['Average Weekly Sales'][i] * 5)/1 + 1:
      list1.append((data['Average Weekly Sales'][i] * 5)//1)
    else:
      list1.append((data['Average Weekly Sales'][i] * 5)//1 + 1)
  else:
    if (data['Average Weekly Sales'][i] * 6)//1 + 1 == (data['Average Weekly Sales'][i] * 6)/1 + 1:
      list1.append((data['Average Weekly Sales'][i] * 6)//1)
    else:
      list1.append((data['Average Weekly Sales'][i] * 6)//1 + 1)

data["Max for Upload Supplier Request1"] = list1

list1 = []
for i in range(len(data)):
  list1.append(max(data["Current Min"][i],data["Min for Upload Supplier Request1"][i]))

data["Min for Upload Supplier Request"] = list1

list1 = []
for i in range(len(data)):
  list1.append(max(data["Current Max"][i],data["Max for Upload Supplier Request1"][i]))

data["Max for Upload Supplier Request"] = list1

st.dataframe(data)

csv = convert_data(data)

st.download_button(label="Download data as CSV", data=csv,file_name='Min_Max_with_supplier_request.csv', mime='text/csv')
