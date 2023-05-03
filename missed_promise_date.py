import pandas as pd
import streamlit as st
import time

st.set_page_config(page_title="Missed Promise Date", layout="wide")

st.subheader("Only shipped orders are in the report")
st.text("'WF Stock, Fulfillment by Amazon' suppliers are not included")
st.subheader(
    "Don't forget to add the 'Priced At Supplier', 'Shipped Date' and 'Delivery Date' columns before downloading the report")

st.sidebar.subheader(" ")

st.markdown('---')

file = st.file_uploader("")

data_raw = pd.DataFrame()

try:
    data_raw = pd.read_csv(file)


    ##############################################
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    ##############################################

except:
    pass
    # if option == '':
    # st.header("Upload a file")
    # else:
    #    file = f'https://raw.githubusercontent.com/csknyy/worldfront/main/All_{option[:3]}_2022_orders.csv'
    #    data_raw = pd.read_csv(file)

#####

st.markdown('---')

freeze = st.sidebar.radio("Freeze?",("No","Yes"))
while freeze == "Yes":
    time.sleep(3)

###########

#try:
data = data_raw[~(data_raw["Supplier"] == "WF Stock, Fulfillment by Amazon")].copy()
# del data_raw
data = data[data['Order Status'] == 'Shipped']
data = data[data['Item Status'] == 'Shipped']
data = data[~(data['Supplier'] == 'Sell Yours Seller')]
data = data.reset_index()
del data['index']

cols = data.columns.to_list()
for i in range(len(cols)):
    cols[i] = cols[i].replace(" ", "_")
data.columns = cols

data = data.rename(columns={"Priced_At_supplier": "Priced_at_supplier"})
data['Supplier'] = data['Supplier'].fillna("NaN")
data['Supplier'] = [i.replace("Do Not Use - ", "") for i in data['Supplier']]

#data = data[~(data['Channel'].str.contains("Fishpond"))]

data['Channel'] = [i.replace('Ebay', 'eBay') for i in data['Channel']]

data['Priced_at_supplier'] = data['Priced_at_supplier'].fillna("NaN")
data['Priced_at_supplier'] = [i.replace("Do Not Use - ", "") for i in data['Priced_at_supplier']]

data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M:%S")
data["Promise_Date"] = pd.to_datetime(data["Promise_Date"], format="%d/%m/%Y")
data["Shipped_Date"] = pd.to_datetime(data["Shipped_Date"], format="%d/%m/%Y")
data["Delivery_Date"] = pd.to_datetime(data["Delivery_Date"], format="%d/%m/%Y")
data["Priced_at_supplier_fc"] = [i[:3] for i in data["Priced_at_supplier"]]
data["Supplier_fc"] = [i[:3] for i in data["Supplier"]]

# data['Date_Purchased'] = data['Date_Purchased'].dt.date
data['Promise_Date'] = data['Promise_Date'].dt.date
data['Shipped_Date'] = data['Shipped_Date'].dt.date
data['Delivery_Date'] = data['Delivery_Date'].dt.date

#####################
st.sidebar.header("Filters")

remove_fishpond = st.sidebar.radio("Remove Fishpond orders?",("No","Yes"))
if remove_fishpond == "Yes":
    data = data[~(data['Channel'].str.contains("Fishpond"))]

start_date = st.sidebar.text_input("Start date", "dd/mm/yyyy")
try:
    start_date = pd.to_datetime(start_date, format="%d/%m/%Y")
except:
    pass
if start_date == "dd/mm/yyyy" or start_date == "":
    pass
else:
    data = data.query("Date_Purchased > @start_date")

end_date = st.sidebar.text_input("End date", "dd/mm/yyyy")
try:
    end_date = pd.to_datetime(end_date, format="%d/%m/%Y")
except:
    pass
if end_date == "dd/mm/yyyy" or end_date == "":
    pass
else:
    data = data.query("Date_Purchased < @end_date")

count_filter = st.sidebar.text_input("Count", "+ for higher, - for lower")

# group_by = st.sidebar.multiselect("Group by",options = ['Date','Barcode','Category','Country','Channel','Supplier','Priced_at_supplier','Order_Status'], default = ['Priced_at_supplier'])

channel_opt = [str(i) for i in data["Channel"].unique()]
channel_opt.sort()
channel = st.sidebar.multiselect("Channel", options=channel_opt)

country_opt = [str(i) for i in data["Country"].unique()]
country_opt.sort()
country = st.sidebar.multiselect("Country", options=country_opt)

priced_at_supplier_fc_opt = [i[:3] for i in data["Priced_at_supplier_fc"].unique()]
priced_at_supplier_fc = st.sidebar.multiselect("Priced at supplier - warehouse", options=priced_at_supplier_fc_opt,
                                               default=priced_at_supplier_fc_opt)

supplier_fc_opt = [i[:3] for i in data["Supplier_fc"].unique()]
supplier_fc = st.sidebar.multiselect("Supplier - warehouse", options=supplier_fc_opt, default=supplier_fc_opt)

pri_supplier_opt = [i for i in data["Priced_at_supplier"].unique()]
pri_supplier_opt.sort()
pri_supplier = st.sidebar.multiselect("Priced at supplier", options=pri_supplier_opt)

supplier_opt = [i for i in data["Supplier"].unique()]
supplier_opt.sort()
supplier = st.sidebar.multiselect("Supplier", options=supplier_opt)

# if len(columns) == 0:
#    columns = [i for i in data.columns]

if count_filter == '+ for higher, - for lower' or count_filter == "":
    count_filter = 0

if len(channel) == 0:
    channel = channel_opt

if len(country) == 0:
    country = country_opt

if len(priced_at_supplier_fc) == 0:
    priced_at_supplier_fc = priced_at_supplier_fc_opt

if len(supplier_fc) == 0:
    supplier_fc = supplier_fc_opt

if len(pri_supplier) == 0:
    pri_supplier = pri_supplier_opt

if len(supplier) == 0:
    supplier = supplier_opt

try:
    data = data.query(
        "Country == @country & Channel == @channel & Priced_at_supplier_fc == @priced_at_supplier_fc & Supplier_fc == @supplier_fc & Priced_at_supplier == @pri_supplier & Supplier == @supplier")
except:
    st.header("Error with query. Try again.")

#####################

tracked = len(data[data['Delivery_Date'].isna()])
# untracked = len(data[~(data['Delivery_Date'].isna())])
# total = tracked + untracked
total = len(data)
untracked = total - tracked

data1 = pd.DataFrame({'Count': [tracked, untracked, total]}, index=['Tracked', 'Untracked', 'Total'])
data1['%'] = [100 * i / total for i in data1['Count']]

data2_1 = data[data['Delivery_Date'].isna()].groupby(by="Priced_at_supplier").count()['Barcode']
data2_1 = pd.DataFrame(data2_1)
data2_1 = data2_1.sort_values(by='Barcode', ascending=False).reset_index()

data2_2 = data[~(data['Delivery_Date'].isna())].groupby(by="Priced_at_supplier").count()['Barcode']
data2_2 = pd.DataFrame(data2_2)
data2_2 = data2_2.sort_values(by='Barcode', ascending=False).reset_index()

data2_1 = data2_1.rename(columns={"Barcode": "Untracked"})
data2_2 = data2_2.rename(columns={"Barcode": "Tracked"})
data2 = pd.merge(data2_1, data2_2, how='outer').fillna(0).astype(int, errors='ignore')

data3_1 = data[data['Delivery_Date'].isna()].groupby(by="Supplier").count()['Barcode']
data3_1 = pd.DataFrame(data3_1)
data3_1 = data3_1.sort_values(by='Barcode', ascending=False).reset_index()

data3_2 = data[~(data['Delivery_Date'].isna())].groupby(by="Supplier").count()['Barcode']
data3_2 = pd.DataFrame(data3_2)
data3_2 = data3_2.sort_values(by='Barcode', ascending=False).reset_index()

data3_1 = data3_1.rename(columns={"Barcode": "Untracked"})
data3_2 = data3_2.rename(columns={"Barcode": "Tracked"})
data3 = pd.merge(data3_1, data3_2, how='outer').fillna(0).astype(int, errors='ignore')

# def right_align(s, props='text-align: right;'):
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

# st.write(data2.astype(str).style.applymap(right_align))

st.markdown('---')

st.header('Box Score - Priced at supplier and Supplier are same (shipped orders)')

data_boxscore0 = data[~(data['Shipped_Date'].isna())][
    ['Date_Purchased', 'Promise_Date', 'Shipped_Date', 'Channel', 'Priced_at_supplier', 'Supplier']].copy()
data_boxscore0 = data_boxscore0[~(data['Promise_Date'].isna())]
data_boxscore0 = data_boxscore0[data_boxscore0["Priced_at_supplier"] == data_boxscore0['Supplier']]

for i in data_boxscore0.columns[:3]:
    data_boxscore0[i] = pd.to_datetime(data_boxscore0[i])

data_boxscore0['Count'] = 1

data_boxscore0['Shipped_days'] = data_boxscore0['Shipped_Date'] - data_boxscore0['Date_Purchased']
data_boxscore0['Shipped_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                  data_boxscore0['Shipped_days']]

data_boxscore0['Promised_days'] = data_boxscore0['Promise_Date'] - data_boxscore0['Date_Purchased']
data_boxscore0['Promised_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                   data_boxscore0['Promised_days']]

data_boxscore0['Promise_Shipped'] = data_boxscore0['Promise_Date'] - data_boxscore0['Shipped_Date']
data_boxscore0['Promise_Shipped'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                     data_boxscore0['Promise_Shipped']]

data_boxscore0_2 = data_boxscore0.iloc[:,3:].groupby(by='Priced_at_supplier').sum()

st.dataframe(data_boxscore0_2)

data_boxscore0_2.loc['Total', :] = [sum(data_boxscore0['Count']), sum(data_boxscore0['Shipped_days']), sum(data_boxscore0['Promised_days']), sum(data_boxscore0['Promise_Shipped'])]

data_boxscore0_2['Count'] = [int(i) for i in data_boxscore0_2['Count']]

data_boxscore0_2['Avg_Shipped_days'] = (data_boxscore0_2['Shipped_days'] / data_boxscore0_2['Count']).round(2)
data_boxscore0_2['Avg_Promised_days'] = (data_boxscore0_2['Promised_days'] / data_boxscore0_2['Count']).round(2)
data_boxscore0_2['Promise - Shipped'] = (data_boxscore0_2['Promise_Shipped'] / data_boxscore0_2['Count']).round(2)

data_boxscore0_2 = data_boxscore0_2[['Count', 'Avg_Shipped_days', 'Avg_Promised_days', 'Promise - Shipped']]

try:
    count_filter = int(count_filter)
    if count_filter < -0.00001:
        count_filter = count_filter * (-1)
        data_boxscore0_2 = data_boxscore0_2.query("Count < @count_filter")
    else:
        data_boxscore0_2 = data_boxscore0_2.query("Count > @count_filter")
except:
    pass

report1 = data_boxscore0_2.sort_values(by='Count', ascending=False).reset_index()
st.dataframe(report1)

csv = convert_df(report1)

st.download_button(label="Download data as CSV", data=csv,
                   file_name='Priced at supplier and Supplier are same (shipped orders).csv', mime='text/csv')

#################################################################################################################

st.markdown('---')

st.header('Box Score - Priced at supplier and Supplier are same (delivered orders)')

data_boxscore = data[~(data['Delivery_Date'].isna())][
    ['Date_Purchased', 'Promise_Date', 'Shipped_Date', 'Delivery_Date', 'Channel', 'Priced_at_supplier',
     'Supplier']]

data_boxscore = data_boxscore.reset_index()
del data_boxscore['index']

data_boxscore = data_boxscore[~(data['Promise_Date'].isna())]
data_boxscore = data_boxscore[data_boxscore["Priced_at_supplier"] == data_boxscore['Supplier']]

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

data_boxscore_2.loc['Total', :] = [sum(data_boxscore['Count']), sum(data_boxscore['Shipped_days']),
                                   sum(data_boxscore['Delivered_days']), sum(data_boxscore['Promised_days']),
                                   sum(data_boxscore['Promise_Delivery'])]

data_boxscore_2['Count'] = [int(i) for i in data_boxscore_2['Count']]

data_boxscore_2['Avg_Shipped_days'] = (data_boxscore_2['Shipped_days'] / data_boxscore_2['Count']).round(2)
data_boxscore_2['Avg_Delivered_days'] = (data_boxscore_2['Delivered_days'] / data_boxscore_2['Count']).round(2)
data_boxscore_2['Avg_Promised_days'] = (data_boxscore_2['Promised_days'] / data_boxscore_2['Count']).round(2)
data_boxscore_2['Promise - Delivery'] = (data_boxscore_2['Promise_Delivery'] / data_boxscore_2['Count']).round(2)

data_boxscore_2 = data_boxscore_2[
    ['Count', 'Avg_Shipped_days', 'Avg_Delivered_days', 'Avg_Promised_days', 'Promise - Delivery']]

try:
    count_filter = int(count_filter)
    if count_filter < -0.00001:
        count_filter = count_filter * (-1)
        data_boxscore_2 = data_boxscore_2.query("Count < @count_filter")
    else:
        data_boxscore_2 = data_boxscore_2.query("Count > @count_filter")
except:
    pass

report2 = data_boxscore_2.sort_values(by='Count', ascending=False).reset_index()
st.dataframe(report2)

csv = convert_df(report2)

st.download_button(label="Download data as CSV", data=csv,
                   file_name='Priced at supplier and Supplier are same (delivered orders).csv', mime='text/csv')

#################################################################################################################

st.markdown('---')

st.header('Box Score - Priced at supplier')

data_boxscore1 = data[~(data['Delivery_Date'].isna())][
    ['Date_Purchased', 'Promise_Date', 'Shipped_Date', 'Delivery_Date', 'Channel', 'Priced_at_supplier']]
data_boxscore1 = data_boxscore1[~(data['Promise_Date'].isna())]

for i in data_boxscore1.columns[:4]:
    data_boxscore1[i] = pd.to_datetime(data_boxscore1[i])

data_boxscore1['Count'] = 1

data_boxscore1['Shipped_days'] = data_boxscore1['Shipped_Date'] - data_boxscore1['Date_Purchased']
data_boxscore1['Shipped_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                  data_boxscore1['Shipped_days']]

data_boxscore1['Delivered_days'] = data_boxscore1['Delivery_Date'] - data_boxscore1['Date_Purchased']

data_boxscore1['Delivered_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                    data_boxscore1['Delivered_days']]

data_boxscore1['Promised_days'] = data_boxscore1['Promise_Date'] - data_boxscore1['Date_Purchased']
data_boxscore1['Promised_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                   data_boxscore1['Promised_days']]

data_boxscore1['Promise_Delivery'] = data_boxscore1['Promise_Date'] - data_boxscore1['Delivery_Date']
data_boxscore1['Promise_Delivery'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                      data_boxscore1['Promise_Delivery']]

data_boxscore1_2 = data_boxscore1.groupby(by='Priced_at_supplier').sum()

data_boxscore1_2.loc['Total', :] = [sum(data_boxscore1['Count']), sum(data_boxscore1['Shipped_days']),
                                    sum(data_boxscore1['Delivered_days']), sum(data_boxscore1['Promised_days']),
                                    sum(data_boxscore1['Promise_Delivery'])]

data_boxscore1_2['Count'] = [int(i) for i in data_boxscore1_2['Count']]

data_boxscore1_2['Avg_Shipped_days'] = (data_boxscore1_2['Shipped_days'] / data_boxscore1_2['Count']).round(2)
data_boxscore1_2['Avg_Delivered_days'] = (data_boxscore1_2['Delivered_days'] / data_boxscore1_2['Count']).round(2)
data_boxscore1_2['Avg_Promised_days'] = (data_boxscore1_2['Promised_days'] / data_boxscore1_2['Count']).round(2)
data_boxscore1_2['Promise - Delivery'] = (data_boxscore1_2['Promise_Delivery'] / data_boxscore1_2['Count']).round(2)

data_boxscore1_2 = data_boxscore1_2[
    ['Count', 'Avg_Shipped_days', 'Avg_Delivered_days', 'Avg_Promised_days', 'Promise - Delivery']]

# try:
count_filter = int(count_filter)
if count_filter < -0.00001:
    count_filter = count_filter * (-1)
    data_boxscore1_2 = data_boxscore1_2.query("Count < @count_filter")
else:
    data_boxscore1_2 = data_boxscore1_2.query("Count > @count_filter")
# except:
#    pass

report3 = data_boxscore1_2.sort_values(by='Count', ascending=False).reset_index()
st.dataframe(report3)

csv = convert_df(report3)

st.download_button(label="Download data as CSV", data=csv, file_name='Box Score - Priced at supplier.csv',
                   mime='text/csv')

#################################################################################################################

st.markdown('---')

st.header('Box Score - Supplier')

data_boxscore2 = data[~(data['Delivery_Date'].isna())][
    ['Date_Purchased', 'Promise_Date', 'Shipped_Date', 'Delivery_Date', 'Channel', 'Supplier']]
data_boxscore2 = data_boxscore2[~(data['Promise_Date'].isna())]

for i in data_boxscore2.columns[:4]:
    data_boxscore2[i] = pd.to_datetime(data_boxscore2[i])

data_boxscore2['Count'] = 1

data_boxscore2['Shipped_days'] = data_boxscore2['Shipped_Date'] - data_boxscore2['Date_Purchased']
data_boxscore2['Shipped_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                  data_boxscore2['Shipped_days']]

data_boxscore2['Delivered_days'] = data_boxscore2['Delivery_Date'] - data_boxscore2['Date_Purchased']
data_boxscore2['Delivered_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                    data_boxscore2['Delivered_days']]

data_boxscore2['Promised_days'] = data_boxscore2['Promise_Date'] - data_boxscore2['Date_Purchased']
data_boxscore2['Promised_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                   data_boxscore2['Promised_days']]

data_boxscore2['Promise_Delivery'] = data_boxscore2['Promise_Date'] - data_boxscore2['Delivery_Date']
data_boxscore2['Promise_Delivery'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in
                                      data_boxscore2['Promise_Delivery']]

data_boxscore2_2 = data_boxscore2.groupby(by='Supplier').sum()

data_boxscore2_2.loc['Total', :] = [sum(data_boxscore2['Count']), sum(data_boxscore2['Shipped_days']),
                                    sum(data_boxscore2['Delivered_days']), sum(data_boxscore2['Promised_days']),
                                    sum(data_boxscore2['Promise_Delivery'])]

data_boxscore2_2['Avg_Shipped_days'] = (data_boxscore2_2['Shipped_days'] / data_boxscore2_2['Count']).round(2)
data_boxscore2_2['Avg_Delivered_days'] = (data_boxscore2_2['Delivered_days'] / data_boxscore2_2['Count']).round(2)
data_boxscore2_2['Avg_Promised_days'] = (data_boxscore2_2['Promised_days'] / data_boxscore2_2['Count']).round(2)
data_boxscore2_2['Promise - Delivery'] = (data_boxscore2_2['Promise_Delivery'] / data_boxscore2_2['Count']).round(2)

data_boxscore2_2 = data_boxscore2_2[
    ['Count', 'Avg_Shipped_days', 'Avg_Delivered_days', 'Avg_Promised_days', 'Promise - Delivery']]

data_boxscore2_2['Count'] = [int(i) for i in data_boxscore2_2['Count']]

try:
    count_filter = int(count_filter)
    if count_filter < -0.00001:
        count_filter = count_filter * (-1)
        data_boxscore2_2 = data_boxscore2_2.query("Count < @count_filter")
    else:
        data_boxscore2_2 = data_boxscore2_2.query("Count > @count_filter")
except:
    pass

report4 = data_boxscore2_2.sort_values(by='Count', ascending=False).reset_index()
st.dataframe(report4)

csv = convert_df(report4)

st.download_button(label="Download data as CSV", data=csv, file_name='Box Score - Supplier.csv', mime='text/csv')

st.markdown('---')

#################################################################################################################

st.header("Raw data")
st.write(data.astype(str))

csv = convert_df(data)

st.download_button(label="Download data as CSV", data=csv, file_name='Raw data.csv', mime='text/csv')

#except:
#    pass
