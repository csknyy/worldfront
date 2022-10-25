import pandas as pd
import streamlit as st

st.set_page_config(page_title="Check Promise Date", layout="wide")

st.subheader("Don't forget to add the 'Priced At Supplier' column before downloading the report")

st.sidebar.header("Filters")

st.markdown('---')

file = st.file_uploader("")

try:
    data = pd.read_csv(file)
except:
    pass

st.markdown('---')

try:
    cols = data.columns.to_list()
    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")
    data.columns = cols

    data = data.rename(columns={"Priced_At_supplier" : "Priced_at_supplier"})
    data['Supplier'] = data['Supplier'].fillna("NaN")
    data['Supplier'] = [i.replace("Do Not Use - ","") for i in data['Supplier']]

    data = data[~(data['Channel'].str.contains("Fishpond"))]
    data['Channel'] = [i.replace('Ebay','eBay') for i in data['Channel']]

    data['Priced_at_supplier'] = data['Priced_at_supplier'].fillna("NaN")
    data['Priced_at_supplier'] = [i.replace("Do Not Use - ","") for i in data['Priced_at_supplier']]

    data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M:%S")
    data["Promise_Date"] = pd.to_datetime(data["Promise_Date"], format="%d/%m/%Y")
    data["Priced_at_supplier_fc"] = [i[:3] for i in data["Priced_at_supplier"]]
    data["Supplier_fc"] = [i[:3] for i in data["Supplier"]]

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

    channel_opt = [str(i) for i in data["Channel"].unique()]
    channel_opt.sort()
    channel = st.sidebar.multiselect("Channel",options = channel_opt)

    country_opt = [str(i) for i in data["Country"].unique()]
    country_opt.sort()
    country = st.sidebar.multiselect("Country",options = country_opt)

    priced_at_supplier_fc_opt = [i[:3] for i in data["Priced_at_supplier_fc"].unique()]
    priced_at_supplier_fc = st.sidebar.multiselect("Priced at supplier - warehouse",options = priced_at_supplier_fc_opt , default = priced_at_supplier_fc_opt)

    supplier_fc_opt = [i[:3] for i in data["Supplier_fc"].unique()]
    supplier_fc = st.sidebar.multiselect("Supplier - warehouse",options = supplier_fc_opt , default = supplier_fc_opt)

    pri_supplier_opt = [i for i in data["Priced_at_supplier"].unique()]
    pri_supplier_opt.sort()
    pri_supplier = st.sidebar.multiselect("Priced at supplier",options = pri_supplier_opt)

    supplier_opt = [i for i in data["Supplier"].unique()]
    supplier_opt.sort()
    supplier = st.sidebar.multiselect("Supplier",options = supplier_opt)

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
        data = data.query("Country == @country & Channel == @channel & Priced_at_supplier_fc == @priced_at_supplier_fc & Supplier_fc == @supplier_fc & Priced_at_supplier == @pri_supplier & Supplier == @supplier")
    except:
        st.header("Error with query. Try again.")

    data_boxscore = data[~data['Promise_Date'].isna()][['Date_Purchased', 'Promise_Date', 'Channel', 'Priced_at_supplier','Supplier']]
    data_boxscore['Count'] = 1

    data_boxscore['Promised_days'] = data_boxscore['Promise_Date'].subtract(data_boxscore['Date_Purchased'])
    data_boxscore['Promised_days'] = [int(100 * i.total_seconds() / (24 * 60 * 60)) / 100 for i in data_boxscore['Promised_days']]

    data_boxscore = data_boxscore.groupby(by='Supplier').sum()

    data_boxscore.loc['Total',:] = [sum(data_boxscore['Count']), sum(data_boxscore['Promised_days'])]

    data_boxscore['Avg_Promised_days'] = (data_boxscore['Promised_days'] / data_boxscore['Count']).round(2)

    data_boxscore = data_boxscore[['Count', 'Avg_Promised_days']]

    data_boxscore['Count'] = [int(i) for i in data_boxscore['Count']]

    try:
        count_filter = int(count_filter)
        if count_filter < -0.00001:
            count_filter = count_filter * (-1)
            data_boxscore = data_boxscore.query("Count < @count_filter")
        else:
            data_boxscore = data_boxscore.query("Count > @count_filter")
    except:
        pass

    data['Promise_Date'] = data['Promise_Date'].dt.date

    st.dataframe(data_boxscore.sort_values(by='Count', ascending=False).reset_index())

    st.markdown('---')

    st.dataframe(data)

except:
    st.header('Please upload a file')