import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="Price Scraper", layout="wide")

##########
#PlaceMakers
##########

def clean_string(text):
    remove = ['"', "'", ':']
    for i in remove:
        text = text.replace(i, "")
    return text

def on_button_click():
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
    data['SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list
    
    st.dataframe(data)

##########
#Super Cheap Auto
##########

def on_button_click():
    st.write("Scrapping started")
    
    url = "https://www.supercheapauto.co.nz/search?prefn1=srgBrand&prefv1=CRC%7CADOS&sz=60"
    response = requests.get(url)
    
    name_list = []
    id_list = []
    price_list = []
    link_list = []
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
    data['SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list

    st.dataframe(data)

if st.button("Scrape PlaceMakers"):
    on_button_click()

if st.button("Scrape Super Cheap Auto"):
    on_button_click()
