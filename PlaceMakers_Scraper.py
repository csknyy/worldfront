import pandas as pd
import streamlit as st
import requests
import re

st.set_page_config(page_title="Price Scraper", layout="wide")


def clean_string(text):
    remove = ['"', "'", ':']
    for i in remove:
        text = text.replace(i, "")
    return text


##########
#PlaceMakers
##########

def on_button_click_Place():
    st.write("Scrapping started")
    
    url = "https://www.placemakers.co.nz/online/search?q=%3ASort+By%3Abrand%3ACRC&page=0"
    response = requests.get(url)
    
    searchResults = int(clean_string(response.text.split("searchResults")[1].split(",")[0]))
    page_count = searchResults / 20
    
    if page_count//1 == page_count:
        page_count = page_count
    else:
        page_count = page_count//1 + 1
    
    responses = []
    for i in range(0, int(page_count)):
        url = f"https://www.placemakers.co.nz/online/search?q=%3ASort+By%3Abrand%3ACRC&page={i}"
        response = requests.get(url)
        responses.append(response.text)
    
    products = []
    for i in range(len(responses)):
        response = responses[i]
        for i in range(len(response.split('<a class="name otherwise" href="/online/p/'))):
            products.append(response.split('<a class="name otherwise" href="/online/p/')[i])
    
    name_list = []
    crc_code_list = []
    id_list = []
    price_list = []
    link_list = []
    for i in range(1, len(products)):
        try:
            if "<" in products[i].split('"')[0]:
                pass
            else:
                id_list.append(products[i].split('"')[0])
            if "<" in products[i].split('\n\t\t\t\t\t\t\t')[1].split('</a>')[0]:
                pass
            else:
                name_list.append(products[i].split('\n\t\t\t\t\t\t\t')[1].split('</a>')[0])
            if "<" in products[i].split('Part Code: ')[1].split('<')[0]:
                pass
            else:
                crc_code_list.append(products[i].split('Part Code: ')[1].split('<')[0])
            price_list.append(products[i].split('$')[1].split('<')[0])
            link_list.append(products[i].split('data-product-url="')[1].split('"\n')[0])
        except:
            pass

    data = pd.DataFrame()
    data['Name'] = name_list
    data['CRC Code'] = crc_code_list
    data['PlaceMakers SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list
    
    st.dataframe(data)
    return data

##########
#Super Cheap Auto
##########

def on_button_click_Super():
    st.write("Scrapping started")
    
    url = "https://www.supercheapauto.co.nz/search?prefn1=srgBrand&prefv1=CRC%7CADOS&sz=60"
    response = requests.get(url)

    products = response.text.split(';" title="')
    
    name_list, id_list, price_list, link_list = [],[],[],[]
    
    for i in range(1, len(products)):
        try:
            if "<" in products[i].split('">')[0]:
                pass
            else:
                name_list.append(products[i].split('">')[0])
            if "<" in products[i].split("/images/")[1].split("/")[0]:
                pass
            else:
                id_list.append(products[i].split("/images/")[1].split("/")[0])
            price_list.append(products[i].split('price">$')[1].split('<')[0])
            link_list.append("https://www.supercheapauto.co.nz" + products[i].split('href="')[1].split('"')[0])
        except:
            pass
    
    data = pd.DataFrame()
    data['Name'] = name_list
    data['Super Cheap Auto SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list

    st.dataframe(data)

##########
#The Warehouse
##########

def on_button_click_Warehouse():
    st.write("Scrapping started")

    url = "https://www.thewarehouse.co.nz/search?prefn1=brand&prefv1=Ados%7CCRC&sz=64"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)

    products = response.text.split('a href="/p/')

    link_list = []
    id_list = []
    name_list = []
    price_list = []
    crc_code_list = []
    
    for i in range(1,len(products)):
      link_list.append("https://www.thewarehouse.co.nz/p/" + products[i].split('"')[0])
      id_list.append(link_list[i-1].split("/")[-1].split(".")[0])
    
    for item_url in link_list:
      response = requests.get(item_url)
      name_list.append(response.text.split('html","name":"')[1].split('"')[0])
      try:
        crc_code_list.append(response.text.split('},"mpn":"')[1].split('"')[0])
      except:
        try:
          crc_code_list.append(re.search(r'\b\d{4}\b', name_list[-1]).group(0))
        except:
          crc_code_list.append("")
      price_list.append(response.text.split('","price":"')[1].split('"')[0])
    
    data = pd.DataFrame()
    data['Name'] = name_list
    data['CRC Code'] = crc_code_list
    data['The Warehouse SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list

    st.dataframe(data)

if st.button("Scrape PlaceMakers"):
    on_button_click_Place()
    
if st.button("Scrape Super Cheap Auto"):
    on_button_click_Super()

if st.button("Scrape The Warehouse"):
    on_button_click_Warehouse()

data1 = pd.DataFrame()

data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
merged_data = data1.merge(data, on='CRC Code', how='outer').fillna("")
st.dataframe(merged_data)
