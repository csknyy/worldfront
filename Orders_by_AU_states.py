import pandas as pd
import streamlit as st
import datetime

st.set_page_config(page_title="Orders by state", layout="wide")

pd.set_option('display.float_format', '{:.2f}'.format)

file = st.file_uploader("Drag and drop a file")

try:
    data = pd.read_csv(file)

    ##############################################
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    ##############################################

    cols = data.columns.to_list()

    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")

    data.columns = cols

    data['Channel'] = [i.replace('Ebay','eBay') for i in data['Channel']]
    data['Order_Status'] = [i.replace("Canceled", "Cancelled") for i in data['Order_Status']]

    channel_group = [i.split(" [")[0] for i in data['Channel']]

    for i in range(len(channel_group)):
        if "Fishpond" in channel_group[i]:
            channel_group[i] = "Fishpond"
        elif "eBay" in channel_group[i]:
            channel_group[i] = "eBay"
        elif "Amazon" in channel_group[i]:
            channel_group[i] = "Amazon"
        elif "Catch" in channel_group[i]:
            channel_group[i] = "Catch"

    data['Channel_Grouped'] = channel_group

    try:
        data['Date'] = [datetime.datetime.strptime(i,'%d/%m/%Y %H:%M:%S') for i in data['Date_Purchased']]
        data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M:%S")
    except:
        data['Date'] = [datetime.datetime.strptime(i, '%d/%m/%Y %H:%M') for i in data['Date_Purchased']]
        data["Date_Purchased"] = pd.to_datetime(data["Date_Purchased"], format="%d/%m/%Y %H:%M")
    data['Barcode'] = data['Barcode'].astype('str')
    data['Date'] = data['Date'].dt.date
    #data['Date'] = [datetime.datetime.combine(i,datetime.datetime.min.time()) for i in data['Date'].dt.date]

    data = data.fillna("NaN")

    channel_groups = [i for i in data["Channel_Grouped"].unique()]

    data_state = data.groupby(by=['Channel_Grouped','Delivery_State','Date']).sum()[['Qty','Total_USD']].reset_index()

    state_count = data_state.groupby(by="Delivery_State").sum().sort_values(by='Qty',ascending=False).reset_index()

    #states = [i for i in state_count['Delivery_State'][:8]]
    states = ['NSW','VIC','QLD','WA','SA','TAS','ACT','NT']


    ################
    #All channels grouped
    ################

    all_channels = data_state.groupby(by=['Date','Delivery_State']).sum().reset_index()

    temp = data.groupby(by=['Date']).sum().reset_index()[['Date','Qty','Total_USD']]

    temp_cols = [f"All States - {col}" for col in temp.columns]
    temp_cols[0] = 'Date'
    temp.columns = temp_cols

    temp0 = all_channels[all_channels['Delivery_State'] == states[0]].copy()[['Date','Qty','Total_USD']]

    temp0_cols = [f"{states[0]} - {col}" for col in temp0.columns]
    temp0_cols[0] = 'Date'
    temp0.columns = temp0_cols

    temp0 = pd.merge(temp, temp0, how="outer", on="Date")
    temp0[f"{states[0]} - Qty %"] = temp0[f"{states[0]} - Qty"] / temp0["All States - Qty"]


    for k in states[1:]:
        temp1 = all_channels[all_channels['Delivery_State'] == k].copy()[['Date', 'Qty', 'Total_USD']]
        temp1_cols = [f"{k} - {col}" for col in temp1.columns]
        temp1_cols[0] = 'Date'
        temp1.columns = temp1_cols
        temp0 = pd.merge(temp0, temp1, how="outer", on="Date")
        temp0[f"{k} - Qty %"] = temp0[f"{k} - Qty"] / temp0["All States - Qty"]

        temp0 = temp0.fillna(0)

    st.subheader('All channels')
    all_vs_wa = temp0.copy()
    st.dataframe(temp0)
    csv = convert_df(temp0)
    st.download_button(label=f"Download all channels as CSV", data=csv, file_name=f'all_channels_grouped.csv', mime='text/csv')
    for i in temp0.columns:
        if "USD" in i:
            del temp0[i]
    csv = convert_df(temp0)
    st.download_button(label=f"Download all channels - only Qty as CSV", data=csv, file_name=f'all_channels_grouped_only Qty.csv', mime='text/csv')

    st.markdown('---')
    ##############################
    # rest of AU vs WA
    ##############################
    all_vs_wa = all_vs_wa[["Date","All States - Qty","All States - Total_USD","WA - Qty","WA - Total_USD"]]

    all_vs_wa["WA - Qty %"] = all_vs_wa["WA - Qty"]/all_vs_wa["All States - Qty"]
    all_vs_wa["Rest of AU - Qty"] = all_vs_wa["All States - Qty"] - all_vs_wa["WA - Qty"]
    all_vs_wa["Rest of AU - Total_USD"] = all_vs_wa["All States - Total_USD"] - all_vs_wa["WA - Total_USD"]
    all_vs_wa["Rest of AU - Qty %"] = 1 - all_vs_wa["WA - Qty %"]

    st.subheader("Rest of AU vs WA")
    st.dataframe(all_vs_wa)
    csv = convert_df(all_vs_wa)
    st.download_button(label=f"Download rest of AU vs WA as CSV", data=csv, file_name=f'rest_of_AU_vs_WA_grouped.csv',mime='text/csv')
    for i in all_vs_wa.columns:
        if "USD" in i:
            del all_vs_wa[i]
    csv = convert_df(all_vs_wa)
    st.download_button(label=f"Download rest of AU vs WA - only Qty as CSV", data=csv, file_name=f'rest_of_AU_vs_WA_grouped_only_Qty.csv',mime='text/csv')


    st.markdown('---')
    ##############################
    #Channels grouped individually
    ##############################

    for i in channel_groups:
        temp_data = data_state[data_state['Channel_Grouped'] == i].copy()
        del temp_data['Channel_Grouped']

        temp = temp_data.groupby(by=['Date']).sum().reset_index()[['Date', 'Qty', 'Total_USD']]

        temp_cols = [f"All States - {col}" for col in temp.columns]
        temp_cols[0] = 'Date'
        temp.columns = temp_cols

        temp0 = temp_data[temp_data['Delivery_State'] == states[0]].copy()[['Date', 'Qty', 'Total_USD']]

        temp0_cols = [f"{states[0]} - {col}" for col in temp0.columns]
        temp0_cols[0] = 'Date'
        temp0.columns = temp0_cols

        temp0 = pd.merge(temp, temp0, how="outer", on="Date")
        temp0[f"{states[0]} - Qty %"] = temp0[f"{states[0]} - Qty"] / temp0["All States - Qty"]

        for k in states[1:]:
            temp1 = temp_data[temp_data['Delivery_State'] == k].copy()[['Date', 'Qty', 'Total_USD']]
            temp1_cols = [f"{k} - {col}" for col in temp1.columns]
            temp1_cols[0] = 'Date'
            temp1.columns = temp1_cols
            temp0 = pd.merge(temp0, temp1, how="outer", on="Date")
            temp0[f"{k} - Qty %"] = temp0[f"{k} - Qty"] / temp0["All States - Qty"]

            temp0 = temp0.fillna(0)

        st.subheader(i)
        st.dataframe(temp0)
        csv = convert_df(temp0)
        st.download_button(label=f"Download {i} as CSV", data=csv, file_name=f'{i}_grouped.csv', mime='text/csv')
        for i in temp0.columns:
            if "USD" in i:
                del temp0[i]
        csv = convert_df(temp0)
        st.download_button(label=f"Download all channels - only Qty as CSV", data=csv, file_name=f'all_channels_grouped_only Qty.csv', mime='text/csv')
        st.markdown('---')


    data_selection = data.copy()

    st.dataframe(data_selection)

    csv = convert_df(data_selection)

    st.download_button(label="Download data as CSV", data=csv, file_name='Filtered - Ungrouped.csv', mime='text/csv')

    st.stop()

except:
    st.subheader("Upload a file - Don't forget to add the 'Delivery State' column before downloading the report")