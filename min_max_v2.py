import pandas as pd
import streamlit as st

st.set_page_config(page_title="Min Max v2.0", layout="wide")

def convert_data(data):
    return data.to_csv(index=False).encode('utf-8')

uploaded_file = st.file_uploader("Choose the .csv file")

data = pd.read_excel(uploaded_file, header=1)

def rounding_check(number):
  return number // 1 == number

def round_number_up(min_max, aws, dep):
  min_week = {"auto":5,"else":4}
  max_week = {"auto":8,"paint":5,"else":6}
  if min_max == 'min':
    if aws == 0: return 0
    elif dep == "300 AUTO AND TOOL STORAGE":
      if rounding_check(aws): return (aws * min_week['auto'])
      else: return (aws * min_week['auto']) // 1 + 1
    else:
      if rounding_check(aws): return (aws * min_week['else'])
      else: return (aws * min_week['else']) // 1 + 1
  elif min_max == 'max':
    if aws == 0: return 0
    elif dep == "300 AUTO AND TOOL STORAGE":
      if rounding_check(aws): return (aws * max_week['auto'])
      else: return (aws * max_week['auto']) // 1 + 1
    elif dep == "300 PAINT":
      if rounding_check(aws): return (aws * max_week['paint'])
      else: return (aws * max_week['paint']) // 1 + 1
    else:
      if rounding_check(aws): return (aws * max_week['else'])
      else: return (aws * max_week['else']) // 1 + 1
  else:
    return 'Invalid'

list1 = []

for i in range(len(dataframe)):
  department = dataframe['Department'][i]
  average_weekly_sales = dataframe['Average Weekly Sales'][i]
  number = round_number_up('min',average_weekly_sales, department)
  list1.append(max(dataframe["Current Min"][i],number))

dataframe["Min for Upload Supplier Request"] = list1
dataframe["Min for Upload Supplier Request1"] = list1

list1 = []

for i in range(len(dataframe)):
  department = dataframe['Department'][i]
  average_weekly_sales = dataframe['Average Weekly Sales'][i]
  number = round_number_up('max',average_weekly_sales, department)
  list1.append(max(dataframe["Current Max"][i],number))

dataframe["Max for Upload Supplier Request"] = list1
dataframe["Max for Upload Supplier Request1"] = list1

for i in range(len(dataframe)):
  if dataframe['Current Min'][i] == dataframe['Min for Upload Supplier Request'][i] and dataframe['Current Max'][i] == dataframe['Max for Upload Supplier Request'][i]:
    dataframe['Min for Upload Supplier Request'][i] = ""
    dataframe['Max for Upload Supplier Request'][i] = ""

data["Max for Upload Supplier Request"] = list1

st.dataframe(data)

csv = convert_data(data)

st.download_button(label="Download data as CSV", data=csv,file_name='Min_Max_with_supplier_request.csv', mime='text/csv')
