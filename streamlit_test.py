import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="Amazon orders", layout="wide")

data = pd.DataFrame

#url = "https://s84.etcserver.com/~coskunyay/worldfront/all_orders.csv"
url = "https://www.coskunyay.com/worldfront/all_orders.csv"

file = st.file_uploader("Drag and drop a file")

try:
    data = pd.read_csv(file)
except:
    data = pd.read_csv(url)

cols = data.columns.to_list()

for i in range(len(cols)):
    cols[i] = cols[i].replace(" ", "_")

data.columns = cols

data['Order_Status'] = [i.replace("Canceled", "Cancelled") for i in data['Order_Status']]

data['Date'] = [datetime.datetime.strptime(i,'%d/%m/%Y %H:%M:%S') for i in data['Date_Purchased']]
data['Date'] = [i.normalize() for i in data['Date']]

cols = data.columns.to_list()

#SIDEBAR

#st.sidebar.header("Filters")
group_by = st.sidebar.multiselect("Group by",options = ['Date','Barcode','Category','Country','Channel','Supplier','Priced_At_supplier','Order_Status'], default = ['Date'])
st.sidebar.markdown("---")
st.sidebar.header("Filters")
status = st.sidebar.multiselect("Order Status",options = data["Order_Status"].unique(), default = data["Order_Status"].unique())
columns = st.sidebar.multiselect("Columns",options = cols, default = cols)
channel = st.sidebar.multiselect("Channel",options = data["Channel"].unique(), default = data["Channel"].unique())
supplier = st.sidebar.multiselect("Supplier",options = data["Supplier"].unique(), default = data["Supplier"].unique())
pri_supplier = st.sidebar.multiselect("Priced at supplier",options = data["Priced_At_supplier"].unique(), default = data["Priced_At_supplier"].unique())

data_selection = data.query("Order_Status == @status & Channel == @channel & Supplier == @supplier & Priced_At_supplier == @pri_supplier")
data_selection = data_selection[columns]


data_temp1 = data.groupby(by=group_by).sum()[['Qty', 'Total_USD']].sort_values(by='Qty', ascending=False)
data_temp1 = data_temp1.rename(columns={'Qty': 'Total Qty', 'Total_USD': 'Total Revenue (USD)'})
data_temp2 = data_selection.groupby(by=group_by).sum()[['Qty','Total_USD']]
data_temp2 = data_temp2.rename(columns={'Qty': 'Qty', 'Total_USD': 'Revenue (USD)'})
data_temp2['Total Sold Qty'] = data_temp1['Total Qty']
data_temp2['Total Revenue (USD)'] = data_temp1['Total Revenue (USD)']
data_temp2 = data_temp2.reset_index().sort_values(by='Date',ascending=False)

st.markdown("---")

try:
    st.subheader(f"Grouped by {group_by}")

    st.write(data_temp2)

    total_revenue = data_selection["Total_USD"].sum()
    total_revenue = int(total_revenue * 100) / 100
    total_qty = data_selection["Qty"].sum()
    average = total_revenue / total_qty
    average = int(average * 100) / 100

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Total quantity")
        st.subheader(f"{total_qty:,}")
    with middle_column:
        st.subheader("Total revenue")
        st.subheader(f"{total_revenue:,} USD")
    #with right_column:
    #    st.subheader("Average")
    #    st.subheader(f"{average:,}")

except:
    st.subheader('Select an option from the "Group by" drop list')

st.markdown("---")

st.subheader(f"Ungrouped")

st.dataframe(data_selection)