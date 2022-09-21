import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Amazon orders", layout="wide")

file = st.file_uploader("Drag and drop a file")

try:
    data = pd.read_csv(file)
except:
    data = pd.read_csv('all_orders.csv')

#COLUMNS
cols = data.columns.to_list()

for i in range(len(cols)):
    cols[i] = cols[i].replace(" ", "_")

data.columns = cols

#SIDEBAR

st.sidebar.header("Filters")
status = st.sidebar.multiselect("Order status",options = data["Order_Status"].unique(), default = data["Order_Status"].unique())
columns = st.sidebar.multiselect("Columns",options = cols, default = cols)
channel = st.sidebar.multiselect("Channel",options = data["Channel"].unique(), default = data["Channel"].unique())
supplier = st.sidebar.multiselect("Supplier",options = data["Supplier"].unique(), default = data["Supplier"].unique())
pri_supplier = st.sidebar.multiselect("Priced at supplier",options = data["Priced_At_supplier"].unique(), default = data["Priced_At_supplier"].unique())

data_selection = data.query("Order_Status == @status & Channel == @channel & Supplier == @supplier & Priced_At_supplier == @pri_supplier")
data_selection = data_selection[columns]



data_groupby = data_selection.groupby(by=["Channel","Order_Status"]).sum()[['Qty','Total_USD']]

total_revenue = data_selection["Total_USD"].sum()
total_revenue = int(total_revenue*100)/100
total_qty = data_selection["Qty"].sum()
average = total_revenue/total_qty
average = int(average*100)/100

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total revenue")
    st.subheader(f"{total_revenue:,}")
with middle_column:
    st.subheader("Total quantity")
    st.subheader(f"{total_qty:,}")
with right_column:
    st.subheader("Average")
    st.subheader(f"{average:,}")

st.markdown("---")

st.dataframe(data_groupby)

st.dataframe(data_selection)