import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cancellation reasons", layout="wide")

#all_reasons = pd.read_csv('https://www.coskunyay.com/worldfront/orders_cancelled.csv')
all_cancel = pd.read_csv('https://raw.githubusercontent.com/csknyy/worldfront/main/orders_cancelled.csv')
all_restricted = pd.read_csv('https://raw.githubusercontent.com/csknyy/worldfront/main/restricted_cancelled.csv')

all_cancel['Date_temp'] = pd.to_datetime(all_cancel['Hour of Date Purchased'], format='%B %d, %Y, %I %p')
latest_date = str(all_cancel['Date_temp'].max())[:10].split("-")

all_restricted['Refund Reason'] = 'Restricted item'
all_reasons = pd.concat([all_cancel, all_restricted], ignore_index=True)

all_reasons['Refund Reason'] = [i.replace("Marked shipped but unable to fulfil","Unable to fulfil") for i in all_reasons['Refund Reason']]
all_reasons['Refund Reason'] = [i.replace("Unable to fulfill","Unable to fulfil") for i in all_reasons['Refund Reason']]

all_reasons = all_reasons.loc[:,['Order ID','Products Name','Refund Reason']]

cols = all_reasons.columns.to_list()
for i in range(len(cols)):
    cols[i] = cols[i].replace(" ", "_")
all_reasons.columns = cols

st.subheader(f"Orders cancelled before {latest_date[2]}-{latest_date[1]}-{latest_date[0]} are in the tool")

file = st.file_uploader("")

try:
    data_can = pd.read_csv(file)
    data_can['Date Purchased'] = pd.to_datetime(data_can['Date Purchased'], format='%d/%m/%Y %H:%M:%S')
    data_can = data_can[data_can['Order Status'] == "Canceled"]
    try:
        del data_can["Image"]
    except:
        pass

    cols = data_can.columns.to_list()
    for i in range(len(cols)):
        cols[i] = cols[i].replace(" ", "_")
    data_can.columns = cols

    reasons_df = pd.DataFrame()
    reasons_df['Order_ID'] = [i for i in data_can['Order_ID']]
    reasons_df['Barcode'] = [str(int(i)) for i in data_can['Barcode']]
    reasons_df['Channel'] = [i for i in data_can['Channel']]
    reasons_df['Priced_at_supplier'] = [i for i in data_can['Priced_At_supplier']]
    reasons_df['Priced_at_supplier'].fillna("WF Stock, Fulfillment by Amazon", inplace = True)

    reasons = []
    for i in data_can['Order_ID']:
        try:
            reasons.append(all_reasons.query(f'Order_ID in [{i}]')['Refund_Reason'].values[0])
        except:
            reasons.append('NaN')
    reasons_df['Reason'] = reasons

    reasons_df['Date_Purchased'] = [i for i in data_can['Date_Purchased']]

    ################################################

    start_date = st.sidebar.text_input("Start date", "dd/mm/yyyy")
    try:
        start_date = pd.to_datetime(start_date, format="%d/%m/%Y")
    except:
        pass
    if start_date == "dd/mm/yyyy" or start_date == "":
        pass
    else:
        reasons_df = reasons_df.query("Date_Purchased > @start_date")

    end_date = st.sidebar.text_input("End date", "dd/mm/yyyy")
    try:
        end_date = pd.to_datetime(end_date, format="%d/%m/%Y")
    except:
        pass
    if end_date == "dd/mm/yyyy" or end_date == "":
        pass
    else:
        reasons_df = reasons_df.query("Date_Purchased < @end_date")

    st.sidebar.markdown("---")

    st.sidebar.header("Filters")
    reason_opt = [i for i in reasons_df["Reason"].unique()]
    reason_opt.sort()
    reason = st.sidebar.multiselect("Reason",options = reason_opt)
    channel_opt = [i for i in reasons_df["Channel"].unique()]
    channel_opt.sort()
    channel = st.sidebar.multiselect("Channel",options = channel_opt)
    pri_supplier_opt = [i for i in reasons_df["Priced_at_supplier"].unique()]
    pri_supplier_opt.sort()
    pri_supplier = st.sidebar.multiselect("Priced at supplier",options = pri_supplier_opt)
    barcode_opt = [i for i in reasons_df["Barcode"].unique()]
    barcode_opt.sort()
    barcode = st.sidebar.multiselect("Barcode",options = barcode_opt)
    columns_opt = [i for i in reasons_df.columns]
    columns_opt.sort()
    columns = st.sidebar.multiselect("Columns",options = columns_opt)

    if len(columns) == 0:
        columns = [i for i in reasons_df.columns]

    if len(reason) == 0:
        reason = [i for i in reasons_df["Reason"].unique()]

    if len(channel) == 0:
        channel = [i for i in reasons_df["Channel"].unique()]

    if len(pri_supplier) == 0:
        pri_supplier = [i for i in reasons_df["Priced_at_supplier"].unique()]

    if len(barcode) == 0:
        barcode = [i for i in reasons_df["Barcode"].unique()]

    data_selection = reasons_df.query("Channel == @channel & Priced_at_supplier == @pri_supplier & Barcode == @barcode & Reason == @reason")
    data_selection = data_selection[columns]
    data_selection['Order_ID'] = [str(i) for i in data_selection['Order_ID']]
    data_selection_nan = data_selection[data_selection['Reason'] == 'NaN']
    total_count = len(data_selection)
    nan_count = len(data_selection_nan)

    data_selection = data_selection[~(data_selection['Reason'] == 'NaN')]

    reasons_df_res = pd.DataFrame(data_selection.groupby(by='Reason').count()['Order_ID'])
    reasons_df_res = reasons_df_res.rename(columns = {'Order_ID':'Count'})
    reasons_df_res = reasons_df_res.sort_values(by = 'Count', ascending=False)
    reasons_df_res['%'] = [int(i*10000/sum(reasons_df_res['Count']))/100 for i in reasons_df_res['Count']]

    reasons_df_sup = pd.DataFrame(data_selection.groupby(by='Priced_at_supplier').count()['Order_ID'])
    reasons_df_sup = reasons_df_sup.rename(columns = {'Order_ID':'Count'})
    reasons_df_sup = reasons_df_sup.sort_values(by = 'Count', ascending=False)
    reasons_df_sup['%'] = [int(i*10000/sum(reasons_df_sup['Count']))/100 for i in reasons_df_sup['Count']]

    reasons_df_bar = pd.DataFrame(data_selection.groupby(by='Barcode').count()['Order_ID'])
    reasons_df_bar = reasons_df_bar.rename(columns = {'Order_ID':'Count'})
    reasons_df_bar = reasons_df_bar.sort_values(by = 'Count', ascending=False)
    reasons_df_bar['%'] = [int(i*10000/sum(reasons_df_bar['Count']))/100 for i in reasons_df_bar['Count']]



    st.subheader(f"Total of cancelled orders: {total_count} ----- Orders removed from report because 'NaN': {nan_count}")
    st.subheader(f"Orders with applicable reasons: {total_count-nan_count}")

    left_column, middle_column, right_column = st.columns(3)
    with left_column:
        st.subheader("Reason")
        st.dataframe(reasons_df_res)
    with middle_column:
        st.subheader("Priced at supplier")
        st.dataframe(reasons_df_sup)
    with right_column:
        st.subheader("Barcode")
        st.dataframe(reasons_df_bar)

    st.markdown("---")
    st.subheader("Applicable orders - Ungrouped")
    st.write(data_selection)

    if nan_count > 0:
        st.markdown("---")
        st.subheader("NaN orders - Ungrouped")
        st.write(data_selection_nan)
        st.markdown("Most likely these orders are not in the saved database yet")
    else:
        pass

    #reasons_df.to_csv('Cancellation_reasons_report.csv', index=False)

except:
    st.subheader("Upload a file")
    st.subheader("Don't forget to add the 'Priced At Supplier' column before downloading the report")