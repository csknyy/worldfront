import pandas as pd
import streamlit as st
import requests
import re
import json

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

    data1 = pd.DataFrame()

    data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    st.dataframe(merged_data)

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
      if "<" in products[i].split('">')[0]:
        pass
      else:
        name_list.append(products[i].split('">')[0])
      if "<" in products[i].split("/images/")[1].split("/")[0]:
        pass
      else:
        id_list.append(products[i].split("/images/")[1].split("/")[0])
      try:
        price_list.append(products[i].split('price">$')[1].split('<')[0])
      except:
        price_list.append("")
      try:
        link_list.append("https://www.supercheapauto.co.nz" + products[i].split('href="')[1].split('"')[0])
      except:
        link_list.append("")
    
    data = pd.DataFrame()
    data['Name'] = name_list
    
    CRC_name_code_dict = {
        'CRC Aeroclean Degreaser - 400g' : '5070',
        'CRC White Lithium Grease - 300g' : '5037',
        'CRC CO Contact Cleaner - 500mL' : '2016',
        'CRC Black It Enamel Paint, Gloss Black - 400g' : '5111',
        'CRC Surface Sanitiser Spray - 500mL' : '1752080',
        'CRC 5.56 Permastraw Multi-Purpose Lubricant 380mL' : '5029',
        'Multi-Lube Gel' : '5018',
        '808 Silicone Spray - 500mL' : '3055',
        'CRC Soft Seal Spray Protectant 400g' : '3013',
        'CRC Brakleen Blaster - 600g' : '5087',
        '5.56 Multi-Purpose Lubricant 420mL' : '1751837',
        'CRC Auto AC Pro Air Conditioner Cleaner' : '1753204',
        'CRC Black Zinc - 300g' : '2089',
        'CRC Engine Start 400mL' : '5040',
        'CRC Maniseal Exhaust Cement - Brown, 145g' : '5061',
        'Fuel Stabiliser 350mL' : '2815',
        'CRC Brakleen Brake and Parts Cleaner 600g' : '5089',
        'ADOS Contact Adhesive - F2 Multipurpose, 75ml' : '8002',
        'CRC Rust Converter 1 Litre' : '18418',
        'CRC Zinc It - 350g' : '2085',
        'CRC Rust Converter Aerosol 425g' : '14610',
        'CRC Tackle Guard Reel Lube 130ml' : '6028',
        'CRC De-Icer Aerosol - 400mL' : '5044',
        'CRC Rust Converter 250mL' : '3073',
        'Penetr8 - 210ml' : '5500',
        'CRC Noxy Spray Lubricant 400g' : '3027',
        'CRC Black It Enamel Paint, Matt Black - 400g' : '5110',
        'CRC Dust Buster - 250mL' : '2071',
        'ADOS Spray Adhesive - Multipurpose, 210ml' : '8015',
        'CRC Bright Zinc - 400mL' : '2087',
        'Evapo-Rust Spray Gel 500g' : '1753336',
        'CRC Salt Terminator Mixer - 946mL' : 'SX32M',
        'CRC Fiberlock Head Gasket Repair - 946mL' : '1224',
        'CRC Mass Air Flow Sensor Cleaner 400mL' : '5093',
        'ADOS Spray Adhesive - Multipurpose, 575ml' : '8017',
        'ADOS Contact Adhesive - F2 Multipurpose, 500ml' : '8009',
        'CRC Welding Anti-Spatter Spray - 300g' : '3358',
        'ADOS Contact Adhesive - F2 Multipurpose, 250ml' : '8008',
        'CRC Oil Fighter - 400mL' : '5069',
        'CRC GDI Intake Valve Cleaner - 400mL' : '5095',
        'Marine 556 Lubricant 420mL' : '1751839',
        'CRC Throttle Body Cleaner 500mL' : '5077',
        'ADOS Adhesive Remover Stuff Off - 500ml' : '8270',
        'CRC Belt Grip 400ml' : '3081',
        'ADOS Spray Adhesive - High Strength, 550ml' : '8180',
        'CRC Black It Enamel Paint, Satin Black - 400g' : '5112',
        'CRC Leak Stop Spray Seal 350g' : '8498',
        'CRC 5.56 Multi Purpose Lubricant - 4 Litre' : '1751846',
        'CRC Dry Glide - 150mL' : '3040',
        'Lanocote Multi-Purpose Lubricant - 500mL' : '3020',
        'CRC Clean-R-Carb - 400g' : '5081',
        'CRC Battery Maintenance Cleaner 300g' : '5097'
    }
    
    crc_code_list = []
    
    for i in data['Name']:
      try:
        crc_code_list.append(CRC_name_code_dict[i])
      except:
        crc_code_list.append("")
    
    data['CRC Code'] = crc_code_list
    
    data['Super Cheap Auto SKU'] = id_list
    data['Price'] = price_list
    data['Link'] = link_list

    st.dataframe(data)
    
    data1 = pd.DataFrame()
    
    data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    st.dataframe(merged_data)

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

    data1 = pd.DataFrame()

    data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    st.dataframe(merged_data)

##########
#The ToolShed
##########

def on_button_click_ToolShed():
    st.write("Scrapping started")
    
    #manually scraped the SKUs#
    sku_list = ['15463', '16382', '17068', '14524', '15958', '12650', '17308', '40683', '40719', '12651', '12652', '12649', '12659', '16638', '12903', '40721', '40715', '12655', '40717', '40761', '15959', '40718', '12660', '12646', '40684', '16631', '12657', '12653', '14005', '14003', '14779', '38166', '12648', '16561', '35011', '12656', '40720', '12658', '14002', '20099', '12645', '40716', '40685', '12647', '40807', '40682']

    crc_code_list = []
    name_list = []
    price_list = []
    link_list = []
    sku_list1 = []
    
    for i in sku_list:
      print(i)
      url = f"https://www.thetoolshed.co.nz/product/{i}"
      response = requests.get(url)
      brand_temp = response.text.split('<title>')[1].split(' ')[0]
      if brand_temp == 'CRC' or brand_temp == 'ADOS':
        crc_code_list.append(response.text.split('<div class="value">')[1].split('<')[0])
        name_list.append(response.text.split('<title>')[1].split('</title>')[0])
        price_list.append(float(response.text.split('"price":"')[1].split('"')[0]))
        sku_list1.append(i)
        link_list.append(url)
    
      else:
        name_list2 = []
        crc_code_list2 = []
        price_list2 = []
        sku_list2 = []
        link_list2 = []
        try:
          try:
            original_i = i
    
            url = f"https://www.thetoolshed.co.nz/product-group/{i}"
            response = requests.get(url)
    
            for j in response.text.split('content_ids: [')[1].split("]")[0].replace('"','').split(','):
              crc_code_list2.append(j)
    
          except:
            i = original_i
    
            url = f"https://www.thetoolshed.co.nz/product/{i}"
            response = requests.get(url)
    
          for j in response.text.split('<div class="name">'):
            if len(j.split('<')[0].strip()) > 0:
              name_list2.append(j.split('<')[0].strip().replace(' &amp; ',' & '))
    
          for j in response.text.split('content_ids: [')[1].split("]")[0].replace('"','').split(','):
            crc_code_list2.append(j)
    
          for j in response.text.split('$'):
            try:
              if int(j.split(' ')[0][0]) > 0:
                price_list2.append(j.split(' ')[0].replace(',',''))
            except:
              pass
    
          for j in range(len(name_list2)):
            sku_list2.append(i)
          for j in range(len(name_list2)):
            link_list2.append(url)
    
          crc_code_list2 = crc_code_list2[:len(name_list2)]
          price_list2 = price_list2[:len(name_list2)]
    
        except:  
          crc_code_list.append('')
          name_list.append('')
          price_list.append('')
          sku_list1.append('')
          link_list.append('')
    
        for j in name_list2:
          name_list.append(j)
        for j in crc_code_list2:
          crc_code_list.append(j)
        for j in price_list2:
          price_list.append(j)
        for j in sku_list2:
          sku_list1.append(j)
        for j in link_list2:
          link_list.append(j)
    
    
    data = pd.DataFrame()
    data['CRC Code'] = crc_code_list
    data['Name'] = name_list
    data['ToolShed SKU'] = sku_list1
    data['Price'] = price_list
    data['Link'] = link_list
    
    st.dataframe(data)
    
    data1 = pd.DataFrame()
    
    data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    
    st.dataframe(merged_data)

##########
#AU - Total Tools
##########

def on_button_click_TotalTools():
    st.write("Scrapping started")

    url = "https://www.totaltools.com.au/brands/crc?p=1&product_list_limit=48"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)
    
    searchResults = int(response.text.split('"toolbar-number">')[3].split('<')[0])
    page_count = searchResults / 48
    
    if page_count//1 == page_count:
        page_count = page_count
    else:
        page_count = page_count//1 + 1
    
    response_text = ''
    responses = []
    for i in range(1, int(page_count)+1):
        url = f"https://www.totaltools.com.au/brands/crc?p={i}&product_list_limit=48"
        response = requests.get(url)
        responses.append(response.text)
        response_text = response_text + response.text

    products_text = response_text.split('"list":"CRC","category":"Brands\\/CRC",')

    products = []
    
    for i in range(1, len(products_text)):
      string_data = products_text[i].split(',"position"')[0]
      string_data = '{' + string_data + '}'
      products.append(json.loads(string_data))
    
    name_list = []
    crc_code_list = []
    id_list = []
    price_list = []
    for i in range(0, len(products)):
      for j,k in zip([id_list, name_list, price_list],['id', 'name', 'price']):
        try:
          j.append(products[i][k])
        except:
          j.append('')
        
    id_list = [i.replace('.','') for i in id_list]
    crc_code_list = [i.split(' ')[-1] for i in name_list]
    
    data = pd.DataFrame()
    data['Name'] = name_list
    data['CRC Code'] = crc_code_list
    data['Total Tools SKU'] = id_list
    data['Price'] = price_list

    st.dataframe(data)   


if st.button("NZ - Scrape PlaceMakers"):
    on_button_click_Place()
    
if st.button("NZ - Scrape Super Cheap Auto"):
    on_button_click_Super()

if st.button("NZ - Scrape The Warehouse"):
    on_button_click_Warehouse()

if st.button("NZ - Scrape The ToolShed"):
    on_button_click_ToolShed()

st.markdown('---')

if st.button("AU - Scrape The Total Tools"):
    on_button_click_TotalTools()
