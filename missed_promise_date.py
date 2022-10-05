import pandas as pd
import streamlit as st

st.set_page_config(page_title="Missed Promise Date", layout="wide")

#data_raw = pd.read_csv("https://raw.githubusercontent.com/csknyy/worldfront/main/missed_orderdefects.csv")

try:
    file = st.file_uploader("Drag and drop a file")
    data_raw = pd.read_csv(file)

except:
    data_raw = pd.read_csv("https://raw.githubusercontent.com/csknyy/worldfront/main/missed_orderdefects.csv")

try:
    data = data_raw[~(data_raw['Supplier'] == "WF Stock, Fulfillment by Amazon")].copy()
    data = data.reset_index()
    del data['index']

    cols = data.columns.to_list()
    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")
    data.columns = cols

    data = data.rename(columns={"Priced_At_supplier" : "Priced_at_supplier"})

    data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M:%S")
    data["Promise_Date"] = pd.to_datetime(data["Promise_Date"], format="%d/%m/%Y")
    data["Shipped_Date"] = pd.to_datetime(data["Shipped_Date"], format="%d/%m/%Y")
    data["Delivery_Date"] = pd.to_datetime(data["Delivery_Date"], format="%d/%m/%Y")
    data["Handover_to_Carrier"] = pd.to_datetime(data["Handover_to_Carrier"], format="%d/%m/%Y")

    data = data.replace({pd.NaT: pd.to_datetime('11/07/1987', format="%d/%m/%Y")})

    data['Date_Purchased'] = data['Date_Purchased'].dt.date
    data['Promise_Date'] = data['Promise_Date'].dt.date
    data['Shipped_Date'] = data['Shipped_Date'].dt.date
    data['Delivery_Date'] = data['Delivery_Date'].dt.date
    data['Handover_to_Carrier'] = data['Handover_to_Carrier'].dt.date

    st.header(f"{type(data['Date_Purchased'][0])}")
    st.header(f"{type(data['Promise_Date'][0])}")
    st.header(f"{type(data['Shipped_Date'][0])}")
    st.header(f"{type(data['Delivery_Date'][0])}")

    st.dataframe(data)

    data = data.replace(pd.to_datetime('11/07/1987', format="%d/%m/%Y"), "")

    #####################

    st.sidebar.header("")

    #group_by = st.sidebar.multiselect("Group by",options = ['Date','Barcode','Category','Country','Channel','Supplier','Priced_at_supplier','Order_Status'], default = ['Priced_at_supplier'])

    st.sidebar.markdown("---")

    columns_opt = [i for i in data.columns]
    columns_opt.sort()
    columns = st.sidebar.multiselect("Columns",options = columns_opt , default = [i for i in data.columns])

    #if len(columns) == 0:
    #    columns = [i for i in data.columns]

    data_selection = data[columns]

    #####################

    tracked = len(data[~(data['Delivery_Date'] == '')])
    untracked = len(data[data['Delivery_Date'] == ''])
    total = tracked + untracked

    data1 = pd.DataFrame({'Count':[tracked, untracked, total]}, index=['Tracked','Untracked','Total'])
    data1['%'] = [100*i/total for i in data1['Count']]

    data2_1 = data[data['Delivery_Date'] == ''].groupby(by="Priced_at_supplier").count()['Barcode']
    data2_1 = pd.DataFrame(data2_1)
    data2_1 = data2_1.sort_values(by='Barcode',ascending=False).reset_index()

    data2_2 = data[~(data['Delivery_Date'] == '')].groupby(by="Priced_at_supplier").count()['Barcode']
    data2_2 = pd.DataFrame(data2_2)
    data2_2 = data2_2.sort_values(by='Barcode',ascending=False).reset_index()

    data2_1 = data2_1.rename(columns={"Barcode" : "Untracked"})
    data2_2 = data2_2.rename(columns={"Barcode" : "Tracked"})
    data2 = pd.merge(data2_1,data2_2,how='outer').fillna(0).astype(int , errors='ignore')


    data3_1 = data[data['Delivery_Date'] == ''].groupby(by="Supplier").count()['Barcode']
    data3_1 = pd.DataFrame(data3_1)
    data3_1 = data3_1.sort_values(by='Barcode',ascending=False).reset_index()

    data3_2 = data[~(data['Delivery_Date'] == '')].groupby(by="Supplier").count()['Barcode']
    data3_2 = pd.DataFrame(data3_2)
    data3_2 = data3_2.sort_values(by='Barcode',ascending=False).reset_index()

    data3_1 = data3_1.rename(columns={"Barcode" : "Untracked"})
    data3_2 = data3_2.rename(columns={"Barcode" : "Tracked"})
    data3 = pd.merge(data3_1,data3_2,how='outer').fillna(0).astype(int , errors='ignore')

    #def right_align(s, props='text-align: right;'):
    #    return props

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Count")
        st.dataframe(data1)
    with middle_column:
        st.subheader("Priced at supplier")
        st.dataframe(data2)
    with right_column:
        st.subheader("Supplier")
        st.dataframe(data3)

    #st.write(data2.astype(str).style.applymap(right_align))

    st.markdown('---')

    st.header('Box Score - Priced at supplier')

    data_boxscore = data[~(data['Delivery_Date'] == "")][['Date_Purchased', 'Promise_Date', 'Shipped_Date', 'Delivery_Date', 'Channel', 'Priced_at_supplier']]

    for i in data_boxscore.columns[:4]:
        data_boxscore[i] = pd.to_datetime(data_boxscore[i])

    data_boxscore['Count'] = 1

    data_boxscore['Shipped_days'] = data_boxscore['Shipped_Date'] - data_boxscore['Date_Purchased']
    data_boxscore['Shipped_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                     data_boxscore['Shipped_days']]

    data_boxscore['Delivered_days'] = data_boxscore['Delivery_Date'] - data_boxscore['Date_Purchased']
    data_boxscore['Delivered_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                       data_boxscore['Delivered_days']]

    data_boxscore['Promised_days'] = data_boxscore['Promise_Date'] - data_boxscore['Date_Purchased']
    data_boxscore['Promised_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                      data_boxscore['Promised_days']]

    data_boxscore['Promise_Delivery'] = data_boxscore['Promise_Date'] - data_boxscore['Delivery_Date']
    data_boxscore['Promise_Delivery'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                         data_boxscore['Promise_Delivery']]

    data_boxscore_2 = data_boxscore.groupby(by='Priced_at_supplier').sum()

    data_boxscore_2.loc['Total',:] = [sum(data_boxscore['Count']),sum(data_boxscore['Shipped_days']),sum(data_boxscore['Delivered_days']),sum(data_boxscore['Promised_days']),sum(data_boxscore['Promise_Delivery'])]

    data_boxscore_2['Count'] = [int(i) for i in data_boxscore_2['Count']]

    data_boxscore_2['Avg_Shipped_days'] = (data_boxscore_2['Shipped_days'] / data_boxscore_2['Count']).round(2)
    data_boxscore_2['Avg_Delivered_days'] = (data_boxscore_2['Delivered_days'] / data_boxscore_2['Count']).round(2)
    data_boxscore_2['Avg_Promised_days'] = (data_boxscore_2['Promised_days'] / data_boxscore_2['Count']).round(2)
    data_boxscore_2['Avg_Promise_Delivery'] = (data_boxscore_2['Promise_Delivery'] / data_boxscore_2['Count']).round(2)

    data_boxscore_2 = data_boxscore_2[['Count', 'Avg_Shipped_days', 'Avg_Delivered_days', 'Avg_Promised_days', 'Avg_Promise_Delivery']]

    st.dataframe(data_boxscore_2.sort_values(by='Avg_Promise_Delivery', ascending=True).reset_index())

    ##################################

    st.markdown('---')

    st.header('Box Score - Supplier')

    data_boxscore1 = data[~(data['Delivery_Date'] == "")][['Date_Purchased', 'Promise_Date', 'Shipped_Date', 'Delivery_Date', 'Channel', 'Supplier']]

    for i in data_boxscore1.columns[:4]:
        data_boxscore1[i] = pd.to_datetime(data_boxscore[i])

    data_boxscore1['Count'] = 1

    data_boxscore1['Shipped_days'] = data_boxscore1['Shipped_Date'] - data_boxscore1['Date_Purchased']
    data_boxscore1['Shipped_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in data_boxscore1['Shipped_days']]

    data_boxscore1['Delivered_days'] = data_boxscore1['Delivery_Date'] - data_boxscore1['Date_Purchased']
    data_boxscore1['Delivered_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in data_boxscore1['Delivered_days']]

    data_boxscore1['Promised_days'] = data_boxscore1['Promise_Date'] - data_boxscore1['Date_Purchased']
    data_boxscore1['Promised_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in data_boxscore1['Promised_days']]

    data_boxscore1['Promise_Delivery'] = data_boxscore1['Promise_Date'] - data_boxscore1['Delivery_Date']
    data_boxscore1['Promise_Delivery'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in data_boxscore1['Promise_Delivery']]

    data_boxscore1_2 = data_boxscore1.groupby(by='Supplier').sum()

    data_boxscore1_2.loc['Total',:] = [sum(data_boxscore1['Count']),sum(data_boxscore1['Shipped_days']),sum(data_boxscore1['Delivered_days']),sum(data_boxscore1['Promised_days']),sum(data_boxscore1['Promise_Delivery'])]

    data_boxscore1_2['Avg_Shipped_days'] = (data_boxscore1_2['Shipped_days'] / data_boxscore1_2['Count']).round(2)
    data_boxscore1_2['Avg_Delivered_days'] = (data_boxscore1_2['Delivered_days'] / data_boxscore1_2['Count']).round(2)
    data_boxscore1_2['Avg_Promised_days'] = (data_boxscore1_2['Promised_days'] / data_boxscore1_2['Count']).round(2)
    data_boxscore1_2['Avg_Promise_Delivery'] = (data_boxscore1_2['Promise_Delivery'] / data_boxscore1_2['Count']).round(2)

    data_boxscore1_2 = data_boxscore1_2[['Count', 'Avg_Shipped_days', 'Avg_Delivered_days', 'Avg_Promised_days', 'Avg_Promise_Delivery']]

    data_boxscore1_2['Count'] = [int(i) for i in data_boxscore1_2['Count']]

    st.dataframe(data_boxscore1_2.sort_values(by='Avg_Promise_Delivery', ascending=True).reset_index())

    st.markdown('---')

    st.write(data_selection.astype(str))

except:
    st.subheader(
        "Don't forget to add the 'Priced At Supplier', 'Shipped Date' and 'Delivery Date' columns before downloading the report")

    st.markdown('---')