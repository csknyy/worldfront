import pandas as pd
import streamlit as st
import datetime
#import matplotlib.pyplot as plt

st.set_page_config(page_title="Orders List summary tool", layout="wide")

pd.set_option('display.float_format', '{:.2f}'.format)

file = st.file_uploader("Drag and drop a file")

try:
    data = pd.read_csv(file)

    cols = data.columns.to_list()

    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")

    data.columns = cols

    data['Order_Status'] = [i.replace("Canceled", "Cancelled") for i in data['Order_Status']]

    data['Date'] = [datetime.datetime.strptime(i,'%d/%m/%Y %H:%M:%S') for i in data['Date_Purchased']]
    data['Date'] = [i.normalize() for i in data['Date']]

    data = data.fillna("NaN")
    try:
        del data["Image"]
    except:
        pass

    cols = data.columns.to_list()

    group_by = st.sidebar.multiselect("Group by",options = ['Date','Barcode','Category','Country','Channel','Supplier','Priced_At_supplier','Order_Status'], default = ['Date'])
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")

    status_opt = [str(i) for i in data["Order_Status"].unique()]
    status_opt.sort()
    status = st.sidebar.multiselect("Order Status",options = status_opt)
    channel_opt = [str(i) for i in data["Channel"].unique()]
    channel_opt.sort()
    channel = st.sidebar.multiselect("Channel",options = channel_opt)
    supplier_opt = [str(i) for i in data["Supplier"].unique()]
    supplier_opt.sort()
    supplier = st.sidebar.multiselect("Supplier",options = supplier_opt)
    pri_supplier_opt = [str(i) for i in data["Priced_At_supplier"].unique()]
    pri_supplier_opt.sort()
    pri_supplier = st.sidebar.multiselect("Priced at supplier",options = pri_supplier_opt)
    barcode_opt = [i for i in data["Barcode"].unique()]
    barcode_opt.sort()
    barcode = st.sidebar.multiselect("Barcode",options = barcode_opt)
    country_opt = [i for i in data["Country"].unique()]
    country_opt.sort()
    country = st.sidebar.multiselect("Country",options = country_opt)
    #columns_opt = [str(i) for i in data.columns.unique()]
    #columns_opt.sort()
    columns = st.sidebar.multiselect("Columns", options = cols, default = cols)

    if len(status) == 0:
        status = [i for i in data["Order_Status"].unique()]

    if len(channel) == 0:
        channel = [i for i in data["Channel"].unique()]

    if len(supplier) == 0:
        supplier = [i for i in data["Supplier"].unique()]

    if len(pri_supplier) == 0:
        pri_supplier = [i for i in data["Priced_At_supplier"].unique()]

    if len(barcode) == 0:
        barcode = [i for i in data["Barcode"].unique()]

    if len(country) == 0:
        country = [i for i in data["Country"].unique()]

    if len(columns) == 0:
        columns = [i for i in cols]

    data_selection = data.query("Order_Status == @status & Channel == @channel & Supplier == @supplier & Priced_At_supplier == @pri_supplier & Barcode == @barcode & Country == @country")
    data_selection = data_selection[columns]

    data_temp1 = data.groupby(by=group_by).sum()[['Qty', 'Total_USD']].sort_values(by='Qty', ascending=False)
    data_temp1 = data_temp1.rename(columns={'Qty': 'Total Qty', 'Total_USD': 'Total Revenue (USD)'})
    data_temp2 = data_selection.groupby(by=group_by).sum()[['Qty','Total_USD']]
    data_temp2 = data_temp2.rename(columns={'Qty': 'Qty', 'Total_USD': 'Revenue (USD)'})
    data_temp2['All status Total Sold Qty'] = data_temp1['Total Qty']
    data_temp2['All status Total Revenue (USD)'] = data_temp1['Total Revenue (USD)']
    data_temp2 = data_temp2.reset_index().sort_values(by='Qty',ascending=False)

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
        with right_column:
            pass

    except:
        st.subheader('Select an option from the "Group by" drop list')

    #st.markdown("---")

    #st.subheader("Reports by filters")

    st.markdown("---")

    st.subheader('Grouped by filters')

    st.subheader("Daily revenue (USD)")

    date_bar = data_selection.groupby(by='Date').sum()['Total_USD']

    st.bar_chart(date_bar)

    #st.markdown("---")

    #channel_group = data_selection.groupby(by='Channel').sum()['Qty']
    #ax = channel_group.plot.barh()
    #st.set_option('deprecation.showPyplotGlobalUse', False)
    #st.pyplot()

    channel_group = data_selection.groupby(by='Channel').sum()[['Qty','Total_USD']]
    channel_group = channel_group.sort_values(by='Qty',ascending=False)

    category_group = data_selection.groupby(by='Category').sum()[['Qty','Total_USD']]
    category_group = category_group.sort_values(by='Qty',ascending=False)

    barcode_group = data_selection.groupby(by='Barcode').sum()[['Qty','Total_USD']]
    barcode_group = barcode_group.sort_values(by='Qty',ascending=False)

    supplier_group = data_selection.groupby(by='Supplier').sum()[['Qty','Total_USD']]
    supplier_group = supplier_group.sort_values(by='Qty',ascending=False)

    pri_supplier_group = data_selection.groupby(by='Priced_At_supplier').sum()[['Qty','Total_USD']]
    pri_supplier_group = pri_supplier_group.sort_values(by='Qty',ascending=False)

    #channel_group.plot(kind = 'barh')

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Channel")
        st.dataframe(channel_group)
    with middle_column:
        st.subheader("Category")
        st.dataframe(category_group)
    with right_column:
        st.subheader("Barcode")
        st.dataframe(barcode_group)

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Supplier")
        st.dataframe(supplier_group)
        st.markdown("Keep in mind that the supplier is NaN because the order hasn't been supplied.")
    with middle_column:
        st.subheader("Priced at supplier")
        st.dataframe(pri_supplier_group)

    st.markdown("---")

    st.subheader(f"Filtered - Ungrouped")

    st.dataframe(data_selection)

except:
    st.subheader("Upload a file")
    st.subheader("Don't forget to add the 'Priced At Supplier' column before downloading the report")