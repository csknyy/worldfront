import pandas as pd
import streamlit as st
import datetime
import time

#import matplotlib.pyplot as plt

st.set_page_config(page_title="Orders List summary tool", layout="wide")

pd.set_option('display.float_format', '{:.2f}'.format)

file = st.file_uploader("Drag and drop a file")

freeze = st.sidebar.radio("Freeze?",("No","Yes"))

while freeze == "Yes":
    time.sleep(3)


try:
    data = pd.read_csv(file)

    cols = data.columns.to_list()

    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")

    data.columns = cols

    data['Channel'] = [i.replace('Ebay','eBay') for i in data['Channel']]
    data['Order_Status'] = [i.replace("Canceled", "Cancelled") for i in data['Order_Status']]
    try:
        data['Date'] = [datetime.datetime.strptime(i,'%d/%m/%Y %H:%M:%S') for i in data['Date_Purchased']]
        data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M:%S")
    except:
        data['Date'] = [datetime.datetime.strptime(i, '%d/%m/%Y %H:%M') for i in data['Date_Purchased']]
        data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M")
    data['Barcode'] = data['Barcode'].astype('str')
    data['Date'] = data['Date'].dt.date

    data["Supplier_fc"] = [str(i)[:3] for i in data["Supplier"]]
    data["Priced_at_supplier_fc"] = [str(i)[:3] for i in data["Priced_At_supplier"]]

    data = data.fillna("NaN")

    for i in ["Image","Total","Order_Item_ID","Promise_Date","Shipped_Date","Delivery_Date"]:
        try:
            del data[i]
        except:
            pass

    cols = data.columns.to_list()

    start_date = st.sidebar.text_input("Start date","dd/mm/yyyy")
    try:
        start_date = pd.to_datetime(start_date, format="%d/%m/%Y")
    except:
        pass
    if start_date == "dd/mm/yyyy" or start_date == "":
        pass
    else:
        data = data.query("Date_Purchased > @start_date")

    end_date = st.sidebar.text_input("End date","dd/mm/yyyy")
    try:
        end_date = pd.to_datetime(end_date, format="%d/%m/%Y")
    except:
        pass
    if end_date == "dd/mm/yyyy" or end_date == "":
        pass
    else:
        data = data.query("Date_Purchased < @end_date")

    group_by = st.sidebar.multiselect("Group by",options = ['Date','Barcode','Category','Country','Channel','Supplier','Priced_At_supplier','Order_Status','Item_Status'], default = ['Date'])
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")

    status_opt = [str(i) for i in data["Order_Status"].unique()]
    status_opt.sort()
    status = st.sidebar.multiselect("Order Status",options = status_opt,default=status_opt)
    #status = st.sidebar.multiselect("Order Status",options = status_opt)

    item_status_opt = [str(i) for i in data["Item_Status"].unique()]
    item_status_opt.sort()
    item_status = st.sidebar.multiselect("Item Status", options=item_status_opt, default=item_status_opt)

    channel_opt = [str(i) for i in data["Channel"].unique()]
    channel_opt.sort()
    channel = st.sidebar.multiselect("Channel",options = channel_opt)
    category_opt = [str(i) for i in data["Category"].unique()]
    category_opt.sort()
    category = st.sidebar.multiselect("Category", options=category_opt)
    supplier_opt = [str(i) for i in data["Supplier"].unique()]
    supplier_opt.sort()
    supplier = st.sidebar.multiselect("Supplier",options = supplier_opt)
    supplier_fc_opt = [str(i) for i in data["Supplier_fc"].unique()]
    supplier_fc_opt.sort()
    supplier_fc = st.sidebar.multiselect("Supplier FC", options=supplier_fc_opt)
    pri_supplier_opt = [str(i) for i in data["Priced_At_supplier"].unique()]
    pri_supplier_opt.sort()
    pri_supplier = st.sidebar.multiselect("Priced at supplier",options = pri_supplier_opt)
    priced_at_fc_opt = [str(i) for i in data["Priced_at_supplier_fc"].unique()]
    priced_at_fc_opt.sort()
    priced_at_fc = st.sidebar.multiselect("Priced at FC", options=priced_at_fc_opt)
    barcode_opt = [i for i in data["Barcode"].unique()]
    barcode_opt.sort()
    barcode = st.sidebar.multiselect("Barcode",options = barcode_opt)
    exl_barcode = st.sidebar.multiselect("Exclude barcodes", options=barcode_opt)
    country_opt = [i for i in data["Country"].unique()]
    country_opt.sort()
    country = st.sidebar.multiselect("Country",options = country_opt)
    #columns_opt = [str(i) for i in data.columns.unique()]
    #columns_opt.sort()
    columns = st.sidebar.multiselect("Columns", options = cols, default = cols)

    if len(status) == 0:
        status = [i for i in data["Order_Status"].unique()]

    if len(item_status) == 0:
        item_status = [i for i in data["Item_Status"].unique()]

    if len(channel) == 0:
        channel = [i for i in data["Channel"].unique()]

    if len(category) == 0:
        category = [i for i in data["Category"].unique()]

    if len(supplier) == 0:
        supplier = [i for i in data["Supplier"].unique()]

    if len(supplier_fc) == 0:
        supplier_fc = [i for i in data["Supplier_fc"].unique()]

    if len(pri_supplier) == 0:
        pri_supplier = [i for i in data["Priced_At_supplier"].unique()]

    if len(priced_at_fc) == 0:
        priced_at_fc = [i for i in data["Priced_at_supplier_fc"].unique()]

    if len(barcode) == 0:
        barcode = [i for i in data["Barcode"].unique()]

    #if len(exl_barcode) == 0:
    #    exl_barcode = [i for i in data["Barcode"].unique()]

    if len(country) == 0:
        country = [i for i in data["Country"].unique()]

    if len(columns) == 0:
        columns = [i for i in cols]

    data = data[~data['Barcode'].isin(exl_barcode)]
    data_selection = data.query("Supplier_fc == @supplier_fc & Priced_at_supplier_fc == @priced_at_fc & Order_Status == @status & Item_Status == @item_status & Channel == @channel & Category == @category & Supplier == @supplier & Priced_At_supplier == @pri_supplier & Barcode == @barcode & Country == @country")

    del data

    data_selection = data_selection[columns]

    date_column = data_selection['Date_Purchased']

    try:
        del data_selection['Date_Purchased']
    except:
        pass

    #data_temp1 = data.groupby(by=group_by).sum()[['Qty', 'Total_USD']].sort_values(by='Qty', ascending=False)
    #data_temp1 = data_temp1.rename(columns={'Qty': 'Total Qty', 'Total_USD': 'Total Revenue (USD)'})

    data_selection['Qty'] = data_selection['Qty'].astype(int)
    data_selection['Total_USD'] = data_selection['Total_USD'].astype(float)

    data_groupby = data_selection.groupby(by=group_by).sum()[['Qty','Total_USD']]
    data_groupby = data_groupby.rename(columns={'Qty': 'Qty', 'Total_USD': 'Revenue (USD)'})
    data_groupby['Rev per Qty'] = data_groupby['Revenue (USD)'] / data_groupby['Qty']
    data_groupby = data_groupby.reset_index().sort_values(by='Qty',ascending=False)

    #if len(status) == 5:
    #    pass
    #else:
    #    data_groupby['All status Total Sold Qty'] = data_temp1['Total Qty']
    #    data_groupby['All status Total Revenue (USD)'] = data_temp1['Total Revenue (USD)']
    #    data_groupby['Rev per Qty (All)'] = data_groupby['All status Total Revenue (USD)'] / data_groupby['All status Total Sold Qty']
    #    data_groupby = data_groupby.reset_index().sort_values(by='Qty',ascending=False)

    st.markdown("---")

    try:
        st.subheader(f"Grouped by {group_by}")
        st.write(data_groupby)

        date_groupby_bar = data_groupby.groupby(by='Date').sum()['Revenue (USD)']
        #st.bar_chart(date_groupby_bar, width = len(date_groupby_bar) * 50, use_container_width = False)
        st.bar_chart(date_groupby_bar)
        del date_groupby_bar

        #total_revenue = data_selection["Total_USD"].sum()
        #total_revenue = int(total_revenue * 100) / 100
        #total_qty = data_selection["Qty"].sum()
        #average = total_revenue / total_qty
        #average = int(average * 100) / 100

        #left_column, middle_column, right_column = st.columns(3)
        #with left_column:
        #    st.subheader("Total quantity")
        #    st.subheader(f"{total_qty:,}")
        #with middle_column:
        #    st.subheader("Total revenue")
        #    st.subheader(f"{total_revenue:,} USD")
        #with right_column:
        #    pass

    except:
        st.text("Choose 'Date' for a specific bar chart")

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

    del data_selection['Date']

    channel_group = data_selection.groupby(by='Channel').sum()[['Qty','Total_USD']].copy()
    #channel_group['Qty %'] = [i*100/sum(channel_group['Qty']) for i in channel_group['Qty']]
    #channel_group['Total_USD %'] = [i*100/sum(channel_group['Total_USD']) for i in channel_group['Total_USD']]
    #channel_group = channel_group[['Qty','Qty %','Total_USD','Total_USD %']]
    channel_group = channel_group.sort_values(by='Qty',ascending=False)

    category_group = data_selection.groupby(by='Category').sum()[['Qty','Total_USD']].copy()
    #category_group['Qty %'] = [int(i * 10000 / sum(category_group['Qty'])) / 100 for i in category_group['Qty']]
    #category_group['Total_USD %'] = [int(i * 10000 / sum(category_group['Total_USD'])) / 100 for i in category_group['Total_USD']]
    #category_group = category_group[['Qty', 'Qty %', 'Total_USD', 'Total_USD %']]
    category_group = category_group.sort_values(by='Qty',ascending=False)

    barcode_group = data_selection.groupby(by='Barcode').sum()[['Qty','Total_USD']].copy()
    #barcode_group['Qty %'] = [int(i * 10000 / sum(barcode_group['Qty'])) / 100 for i in barcode_group['Qty']]
    #barcode_group['Total_USD %'] = [int(i * 10000 / sum(barcode_group['Total_USD'])) / 100 for i in barcode_group['Total_USD']]
    #barcode_group = barcode_group[['Qty', 'Qty %', 'Total_USD', 'Total_USD %']]
    barcode_group = barcode_group.sort_values(by='Qty',ascending=False)

    supplier_group = data_selection.groupby(by='Supplier').sum()[['Qty','Total_USD']].copy()
    #supplier_group['Qty %'] = [int(i * 10000 / sum(supplier_group['Qty'])) / 100 for i in supplier_group['Qty']]
    #supplier_group['Total_USD %'] = [int(i * 10000 / sum(supplier_group['Total_USD'])) / 100 for i in supplier_group['Total_USD']]
    #supplier_group = supplier_group[['Qty', 'Qty %', 'Total_USD', 'Total_USD %']]
    supplier_group = supplier_group.sort_values(by='Qty',ascending=False)

    pri_supplier_group = data_selection.groupby(by='Priced_At_supplier').sum()[['Qty','Total_USD']].copy()
    #pri_supplier_group['Qty %'] = [int(i * 10000 / sum(pri_supplier_group['Qty'])) / 100 for i in pri_supplier_group['Qty']]
    #pri_supplier_group['Total_USD %'] = [int(i * 10000 / sum(pri_supplier_group['Total_USD'])) / 100 for i in pri_supplier_group['Total_USD']]
    #pri_supplier_group = pri_supplier_group[['Qty', 'Qty %', 'Total_USD', 'Total_USD %']]
    pri_supplier_group = pri_supplier_group.sort_values(by='Qty',ascending=False)

    #channel_group.plot(kind = 'barh')

    st.subheader("Channel")
    st.dataframe(channel_group)

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Category")
        st.dataframe(category_group)
    with right_column:
        st.subheader("Barcode")
        st.dataframe(barcode_group)

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader("Supplier")
        st.dataframe(supplier_group)
        st.markdown("Keep in mind that the supplier is NaN because the order hasn't been supplied.")
    with right_column:
        st.subheader("Priced at supplier")
        st.dataframe(pri_supplier_group)

    st.markdown("---")

    st.subheader(f"Filtered - Ungrouped")

    data_selection.insert(0, 'Date_Purchased', date_column)

    st.dataframe(data_selection)

    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(data_selection)

    st.download_button(label="Download data as CSV",data=csv,file_name='Filtered - Ungrouped.csv',mime='text/csv')

    st.stop()

except:
    st.subheader("Upload a file - Don't forget to add the 'Priced At Supplier' column before downloading the report")
    st.subheader("Or select an option from the Group by drop list")