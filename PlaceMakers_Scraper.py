import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="PlaceMakers_Scraper", layout="wide")

def clean_string(text):
    remove = ['"', "'", ':']
    for i in remove:
        text = text.replace(i, "")
    return text

def on_button_click():
    st.write("Scrape PlaceMakers")
    
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
    
    name_list = []
    crc_code_list = []
    id_list = []
    price_list = []
    
    for response in responses:
        products = response.split('<div class="product-block')
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
            except:
                pass
    
    data = pd.DataFrame()
    data['Name'] = name_list
    data['CRC Code'] = crc_code_list
    data['SKU'] = id_list
    data['Price'] = price_list
    
    st.dataframe(data)

if st.button("Scrape PlaceMakers"):
    on_button_click()
