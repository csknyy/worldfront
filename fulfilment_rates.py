import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="Cancellation and fulfilment rates", layout="wide")

st.header(f"Cancellation and fulfilment rates")

file = st.file_uploader("Drag and drop a file")

try:
    data = pd.read_csv(file)

    cols = data.columns.to_list()

    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")

    data.columns = cols

    data['Channel'] = [i.replace('Ebay', 'eBay') for i in data['Channel']]
    data['Order_Status'] = [i.replace("Canceled", "Cancelled") for i in data['Order_Status']]

    data = data.fillna("NaN")

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

    #group_by = st.sidebar.multiselect("Group by",options = ['Date','Barcode','Category','Country','Channel','Supplier','Priced_At_supplier','Order_Status','Item_Status'], default = ['Date'])
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")

    count_filter = st.sidebar.text_input("Total count", "+ for higher, - for lower")

    status_opt = [str(i) for i in data["Order_Status"].unique()]
    status_opt.sort()
    status = st.sidebar.multiselect("Order Status",options = status_opt)
    #status = st.sidebar.multiselect("Order Status",options = status_opt)

    item_status_opt = [str(i) for i in data["Item_Status"].unique()]
    item_status_opt.sort()
    item_status = st.sidebar.multiselect("Item Status", options=item_status_opt)

    channel_opt = [str(i) for i in data["Channel"].unique()]
    channel_opt.sort()
    channel = st.sidebar.multiselect("Channel",options = channel_opt)
    category_opt = [str(i) for i in data["Category"].unique()]
    category_opt.sort()
    category = st.sidebar.multiselect("Category", options=category_opt)
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
    columns = st.sidebar.multiselect("Columns", options = cols)

    if count_filter == '+ for higher, - for lower' or count_filter == "":
        count_filter = 0

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

    if len(pri_supplier) == 0:
        pri_supplier = [i for i in data["Priced_At_supplier"].unique()]

    if len(barcode) == 0:
        barcode = [i for i in data["Barcode"].unique()]

    if len(country) == 0:
        country = [i for i in data["Country"].unique()]

    if len(columns) == 0:
        columns = [i for i in cols]

    data_selection = data.query("Order_Status == @status & Item_Status == @item_status & Channel == @channel & Category == @category & Supplier == @supplier & Priced_At_supplier == @pri_supplier & Barcode == @barcode & Country == @country")

    del data

    data_selection = data_selection[columns]

    data_selection['Is_same'] = data_selection['Priced_At_supplier'] == data_selection['Supplier']

    sup_count = data_selection.groupby(by="Priced_At_supplier").count()['Qty']
    sup_count = pd.DataFrame(sup_count).sort_values(by=["Qty"], ascending=False).reset_index()
    sup_count.rename(columns={"Qty": "Total"},inplace= True)

    count_list = []
    for i in status:
        count_list.append(f"{i}_count")

        count_list[-1] = data_selection[data_selection['Order_Status'] == i].groupby(by="Priced_At_supplier").count()['Qty'].reset_index()
        count_list[-1] = pd.merge(sup_count, count_list[-1], on='Priced_At_supplier',how='outer')
        count_list[-1].fillna(0,inplace=True)
        count_list[-1].rename(columns={"Qty": i},inplace= True)
        count_list[-1][f'{i}_%'] = count_list[-1][i] * 100 / count_list[-1]['Total']
        count_list[-1][i] = [int(j) for j in count_list[-1][i]]
        count_list[-1] = count_list[-1].sort_values(by = i, ascending=False)

    is_same = data_selection.groupby(by="Priced_At_supplier").sum()['Is_same']
    is_same = pd.DataFrame(is_same).sort_values(by=["Is_same"], ascending=False).reset_index()
    is_same["Is_same"] = [int(i) for i in is_same["Is_same"]]

    report0 = pd.merge(sup_count,is_same,on='Priced_At_supplier')
    report0['Is_same_%'] = report0['Is_same'] * 100 / report0['Total']

    for i in count_list:
        temp = i.iloc[:,[0,2,3]]
        report0 = pd.merge(report0, temp, on='Priced_At_supplier',how='outer')

    report0.fillna(0,inplace=True)

    report0.rename(columns={"Priced_At_supplier": "Priced at supplier"},inplace= True)

    try:
        count_filter = int(count_filter)
        if count_filter < -0.00001:
            count_filter = count_filter * (-1)
            report0 = report0.query("Total < @count_filter")
        else:
            report0 = report0.query("Total > @count_filter")
    except:
        pass

    st.subheader('All statuses based on Priced at supplier')
    st.dataframe(report0)

    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(report0)
    st.download_button(label="Download all statuses as .csv", data=csv, file_name='All statuses based on Priced at supplier.csv', mime='text/csv')
    st.markdown("---")


    st.subheader(f"Filtered - Ungrouped")
    st.dataframe(data_selection)

    csv = convert_df(data_selection)
    st.download_button(label="Download Filtered - Ungrouped as .csv", data=csv, file_name='AFiltered - Ungrouped.csv', mime='text/csv')

except:
    st.subheader("Upload a file - Don't forget to add the 'Priced At Supplier' column before downloading the report")