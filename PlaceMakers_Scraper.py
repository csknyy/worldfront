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
    data['PlaceMakers SKU'] = id_list
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

    products = response.text.split(';" title="')
    
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
    data['Super Cheap Auto SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list

    st.dataframe(data)

##########
#The Warehouse
##########

def on_button_click():
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
    
    items_done = 1
    
    for item_url in link_list:
      response = requests.get(item_url)
      name_list.append(response.text.split('html","name":"')[1].split('"')[0])
      try:
        crc_code_list.append(response.text.split('},"mpn":"')[1].split('"')[0])
      except:
        crc_code_list.append("")
      price_list.append(response.text.split('","price":"')[1].split('"')[0])
      st.write(f"{items_done} / {len(link_list)} done")
      items_done += 1
    
    data = pd.DataFrame()
    data['Name'] = name_list
    data['CRC Code'] = crc_code_list
    data['The Warehouse SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list

    st.dataframe(data)

###################################################################

if st.button("Scrape PlaceMakers"):
    on_button_click()

if st.button("Scrape Super Cheap Auto"):
    on_button_click()

if st.button("Scrape The Warehouse"):
    on_button_click()
