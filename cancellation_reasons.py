import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import datetime
import streamlit as st

st.set_page_config(layout="wide")


file = st.file_uploader("Drag and drop a file")

data_orders = pd.read_csv(file)
data_can = data_orders[data_orders['Order Status'] == "Canceled"]
orders = [str(i) for i in data_can['Order ID']]

loading = st.empty()
loading.subheader(f"0.00% - 0 / {len(orders)}")

reasons = []

a = 0
for i in orders:
    a = a + 1
    try:
        url = "https://all.worldfront.co/axis/orders.php?action=edit&oID="+str(i)
        data = {'username': 'coskun','password': 'vateMuny73'}
        response = requests.post(url,auth = HTTPBasicAuth('coskun', 'vateMuny73'), data = data)
        url = response.text.split(' ')[-15][1:-4]
        response1 = requests.post(url,auth = HTTPBasicAuth('coskun', 'vateMuny73'), data = data)
        temp = response1.text.split('Reason: ')[-1].split('&')[0].split("<br />")[0]
        date = response1.text.replace('&nbsp;',"").split('Canceled')[0].split('"axisDate">')[-1].split('</span>')[0].split(",")[1]
        date = datetime.datetime.strptime(date,'%d%b%Y%H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        temp_reason = f'{a} done / {i} / {temp[:50]} / date: {date}'
        print(temp_reason)
        reasons.append(temp_reason)
        loading.empty()
        perc = str(f"{int(a*10000/len(orders))/100}% - {a} / {len(orders)}")
        loading.subheader(perc)

    except:
        print(f'{a} done - N/A')
        reasons.append("N/A")

reasons_df = pd.DataFrame()
reasons_df['Order ID'] = [i.split(" / ")[1] for i in reasons]
reasons_df['Barcode'] = [str(int(i)) for i in data_can['Barcode']]
reasons_df['Priced at supplier'] = [i for i in data_can['Priced At supplier']]
reasons_df['Reason'] = [i.split(" / ")[2] for i in reasons]
reasons_df['Date purchased'] = [i for i in data_can['Date Purchased']]
reasons_df['Cancellation date'] = [i.split("date: ")[1] for i in reasons]

reasons_df_res = pd.DataFrame(reasons_df.groupby(by='Reason').count()['Order ID'])
reasons_df_res = reasons_df_res.rename(columns = {'Order ID':'Count'})
reasons_df_res = reasons_df_res.sort_values(by = 'Count', ascending=False)

reasons_df_sup = pd.DataFrame(reasons_df.groupby(by='Priced at supplier').count()['Order ID'])
reasons_df_sup = reasons_df_sup.rename(columns = {'Order ID':'Count'})
reasons_df_sup = reasons_df_sup.sort_values(by = 'Count', ascending=False)

reasons_df_bar = pd.DataFrame(reasons_df.groupby(by='Barcode').count()['Order ID'])
reasons_df_bar = reasons_df_bar.rename(columns = {'Order ID':'Count'})
reasons_df_bar = reasons_df_bar.sort_values(by = 'Count', ascending=False)

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

st.write(reasons_df)

reasons_df.to_csv('Cancellation reasons report.csv')