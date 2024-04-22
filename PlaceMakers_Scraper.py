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
# NZ - PlaceMakers
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

    #data1 = pd.DataFrame()

    #data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    #merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    #st.dataframe(merged_data)

##########
# NZ - Super Cheap Auto
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
        'CRC Battery Maintenance Cleaner 300g' : '5097',
        'CRC Prep It - 400mL' : '2114',
        'CRC AC Charge Refrigerant R134a Air Conditioner Refill - 400g' : '5101',
        'CRC AC Charge Refrigerant R134a Refill  and  Hose - 400g' : '5100',
        'CRC Etch It - 400mL' : '2110',
        'CRC Prime It - 400mL' : '2091',
        'CRC Battery Terminal Protector 300g' : '5098'
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
    
    #data1 = pd.DataFrame()
    
    #data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    #merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    #st.dataframe(merged_data)

##########
# NZ - The Warehouse
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

    #data1 = pd.DataFrame()

    #data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    #merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    #st.dataframe(merged_data)

##########
# NZ - The ToolShed
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
    
    #data1 = pd.DataFrame()
    
    #data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    #merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    
    #st.dataframe(merged_data)

##########
# AU - Total Tools
##########

def on_button_click_AU_TotalTools():
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

    data.loc[data['CRC Code'] == 'Fluid', 'CRC Code'] = '3065'

    st.dataframe(data)

##########
# AU - Super Cheap Auto
##########

def on_button_click_AU_Super():
    st.write("Scrapping started")
    
    url = "https://www.supercheapauto.com.au/search?prefn1=srgBrand&prefv1=CRC%7CADOS&sz=60"
    response = requests.get(url)
    
    products = response.text.split(';" title="')
    
    name_list, id_list, price_list, link_list, first_price_list = [],[],[],[],[]
    
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
        first_price_list.append(products[i].split('price">$')[2].split('<')[0])
      except:
        first_price_list.append("")
      try:
        link_list.append("https://www.supercheapauto.com.au" + products[i].split('href="')[1].split('"')[0])
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
        'CRC Battery Maintenance Cleaner 300g' : '5097',
        'CRC Mass Air Flow Sensor Cleaner 300g' : '5014',
        'CRC Throttle Body and Air Intake Cleaner 400g' : '5079',
        'CRC Battery Terminal Protector 300g' : '5098',
        '5.56 Multi-Purpose Lubricant CRC 400g' : '5005',
        'CRC Oil Fighter Oil Stain Remover - 400mL' : '1751967',
        'CRC Automotive Electronic Cleaner - 350g' : '5013',
        'CRC Aerostart 300g' : '5051',
        'Lanoshield CRC 350g' : '3051',
        'Marine 66 CRC 300g' : '6006',
        'CRC Prep It - 400mL' : '2114',
        'CRC Prime It - 400mL' : '2091',
        'CRC Etch It - 400mL' : '2110',
        'CRC SmartWasher Mobile Parts Cleaning Startup Kit - SW-23-1' : 'SW-23'
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
    data['First Price'] = first_price_list
    data['Link'] = link_list

    st.dataframe(data)
    
    #data1 = pd.DataFrame()
    
    #data1['CRC Code'] = ['3020','3027','3036','3040','3055','3058','3059','3061','3063','3064','3097','3145','3358','3410','5006','5009','5012','5014','5015','5018','5019','5028','5029','5035','5037','5070','5089','5500','1751837','1751839','1751840','1751841','1751842','1751846','1751847','1751848','1752426','1752455','5022','5023','5025','5026','5044','5045','5047','5069','9009','9011','9015','9017','9060','9220','9225','9230','9235','9240','9302','9304','9308','8288','20365','20369','20380','20384','20388','20392','20395','20400','2105','2087','2090','2125','2129','3073','3075','14610','18418','1753336','EVR1','EVR5','4420','4490','4492','5115','7063','7064','7072','7073','7074','7075','8002','8006','8008','8009','8010','8012','8014','8017','8020','8022','8026','8034','8110','8180','8200','8202','8204','8270','8490','8492','8494','8498','1751844','1753108','5040','6028','2015','2016','2018','2053','2071','3013']
    #merged_data = data1.merge(data, on='CRC Code', how='left').fillna("")
    #st.dataframe(merged_data)

##########
# AU - BFC
##########

def on_button_click_AU_BFC():
    st.write("Scrapping started")

    import json

    url = 'https://www.bcf.com.au/search?prefn1=brand&prefv1=ADOS%7CCRC&sz=60'
    response = requests.get(url)
    
    results = int(response.text.split('Showing\n<span>\n\n1 - ')[1].split(' ')[0])
    
    item_links = []
    
    for i in range(1, results+1):
      item_links.append("https://www.bcf.com.au" + response.text.split(' class="name-link" href="')[i].split('"')[0])
    
    products = []
    
    for i in item_links:
      url = i
      response_temp = requests.get(url)
      temp = response_temp.text.split('{"ecommerce":{"email":"","detail":{"products":')[1].split('}}}')[0]
      products.append(json.loads(temp))
    
    ids = [i[0]['id'] for i in products]
    names = [i[0]['name'] for i in products]
    prices = [i[0]['price'] for i in products]
    
    data = pd.DataFrame()
    
    data['BCF SKU'] = ids
    data['Item Description'] = names
    data['Price'] = prices

    st.dataframe(data)

##########
# AU - Anaconda
##########

def on_button_click_AU_Anaconda():
    st.write("Scrapping started")

    import json
    
    url = 'https://www.anacondastores.com/search?q=crc:relevance:brand:crc'

    response = requests.get(url)
    
    products = []

    results = len(response.text.split("data-variantdata=\'")) - 1
    
    for i in range(1,results+1):
      temp = response.text.split("data-variantdata=\'")[i].split("\n")[0]
      products.append(json.loads(temp))
    
    names = [i['name'] for i in products]
    prices = [i['price']['toPrice'].replace('$','') for i in products]
    first_prices = [i['price']['toRegPrice'].replace('$','') for i in products]
    links = [i['variantUrl'] for i in products]
    
    data = pd.DataFrame()
    
    data['Item Description'] = names
    data['Price'] = prices
    data['First Price'] = first_prices
    data['Link'] = links

    st.dataframe(data)


if st.button("NZ - Scrape PlaceMakers"):
    on_button_click_Place()
    
if st.button("NZ - Scrape Super Cheap Auto"):
    on_button_click_Super()

if st.button("NZ - Scrape The Warehouse"):
    on_button_click_Warehouse()

if st.button("NZ - Scrape The ToolShed"):
    on_button_click_ToolShed()

select_text = st.radio("Select customer",["Bunnings", "Mitre 10", "The ToolShed", "Repco", "Sydney Tools"])

######################################################
######## Bunnings

if select_text == "Bunnings":
    text_input = st.text_input("Enter Bunnings text here:")
    if len(text_input) > 1:
        replacements = {' In-store only': '', 'ADOS': 'CRC ADOS', '808 Silicone': 'CRC 808 Silicone', 'CRC 550ml CRC': 'CRC 500ml', 'CRC ADOS CRC ADOS': 'CRC CRC ADOS', 'CRC ADOS 1L CRC': 'CRC ADOS 1L'}
        for old, new in replacements.items():
            text_input = text_input.replace(old, new)
        names = []
        prices = []
        price_flags = []
        for i in text_input.split('Compare')[1:]:
          names.append(i.split('CRC')[3].split(' (')[0].strip())
          price_flags.append(i.split('CRC')[2].strip())
          prices.append(i.split('$')[1].strip())
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['Price flag'] = price_flags
        data['Price'] = prices

        st.dataframe(data)

######################################################
######## Mitre 10

if select_text == "Mitre 10":
    text_input = st.text_input("Enter Mitre 10 text here:")
    if len(text_input) > 1:
        names,SKUs,prices,RRPs = [],[],[],[]
        text_input = text_input.replace('pack of 72','each')

        for i in text_input.split(' Choose a store for availability '):
          index = int((len(i.split(' ★')[0]) - 5)/2)
          names.append(i.split(' ★')[0][:-index].strip())
          SKUs.append(i.split('SKU: ')[1].split(' ')[0])
          prices.append(float(i.split('$')[1].split('each')[0].replace(' ','')+'00'))
          try:
            RRPs.append(i.split('RRP $')[1])
          except:
            RRPs.append('')
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['Mitre10 SKU'] = SKUs
        data['Price'] = prices
        data['First Price'] = RRPs
        
        st.dataframe(data)

######################################################
######## The ToolShed
if select_text == "The ToolShed":
    text_input = st.text_input("Enter The ToolShed text here:")
    if len(text_input) > 1:
        replacements = {'5 Stars4 Stars3 Stars2 Stars1 Star ': '', ' Inc GST': '', 'ADD TO CART ': ''}

        for old, new in replacements.items():
            text_input = text_input.replace(old, new)
        
        products = [i.strip() for i in text_input.split('MORE INFO')[:-1]]
        
        names, CRC_codes, prices = [],[],[]
        
        for i in products:
          ind = int((len(i.split(' ')) - 4) / 2)
          names.append(' '.join(i.split(' ')[:ind]))
          CRC_codes.append(i.split(' ')[ind*2])
          prices.append(i.split('$')[1])
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['CRC codes'] = CRC_codes
        data['Price'] = prices

        st.dataframe(data)

######################################################
######## Repco
if select_text == "Repco":
    text_input = st.text_input("Enter Repco text here:")
    if len(text_input) > 1:
        text_input = text_input.replace(' Repco Petrol & Diesel Injector Cleaner Restore lost power and boost fuel economy when adding Repco Fuel Injector Cleaner next time you fill up. Shop Now ','')
        text_input = text_input.replace('CRC Belt Dressing 350G/500Ml CRC Belt Dressing 350G/500Ml', 'CRC Belt Dressing 350G/500Ml CRC Belt Dressing 350G/500Ml - 1753472')
        text_input = text_input.replace('ADOS', 'ADOS CRC')
        text_input = text_input.replace('Contact Adhesive F2 Mp 75ml', 'CRC Contact Adhesive F2 Mp 75ml')
        text_input = text_input.replace('CRC Prime It - Red Oxide Primer 400ml - 2091', 'CRC Prime It Red Oxide Primer 400ml - 2091')

        products = [i.strip() for i in text_input.split('CRC')[2::2]]

        names, CRC_codes, prices, price_flags, price_flags1, price_flags2, first_prices = [], [], [], [], [], [], []
        
        for i in products:
          names.append(i.split(' - ')[0])
          CRC_codes.append(i.split(' - ')[1].split(' ')[0])
          prices.append(i.split('$')[1].split(' ')[0])
          try:
            price_flags1.append(' '.join(i.split('$')[1].split(' ')[1:]) + '$' + i.split('$')[2])
          except:
            price_flags1.append('')
        
        price_flags2 = ['CLEARANCE' if i.strip().split(' ')[-1] == 'CLEARANCE' else '' for i in text_input.split('CRC')[1::2]]
        for i,j in zip(price_flags1,price_flags2):
          price_flags.append(i+j)
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['CRC codes'] = CRC_codes
        data['Price'] = prices
        data['Price flag'] = price_flags

        st.dataframe(data)

######################################################
######## Sydney Tools
if select_text == "Sydney Tools":
    text_input = st.text_input("Enter Sydney Tools text here:")
    if len(text_input) > 1:
        replacements = {'CRC 2085 350g CRC Zinc It': 'CRC 2085 350g Zinc It',
                        'CRC 2089 400ml CRC Black Zinc': 'CRC 2089 400ml Black Zinc',
                        'CRC 18418 1L CRC Rust Converter': 'CRC 18418 1L Rust Converter',
                        'CRC 14610 425g CRC Rust Converter Aerosol': 'CRC 14610 425g Rust Converter Aerosol'}
        
        for old, new in replacements.items():
            text_input = text_input.replace(old, new)
        
        test_list = text_input.split("CRC ")[::3][1:]
        
        new_list,indexes = [],[]
        
        for i in range(len(test_list)):
          temp = test_list[i].strip()
          check = [ "FREE SHIPPING", "Clearance"]
          for word in check:
            if word in temp:
              indexes.append([i+1,word])
              temp = test_list[i].replace(word,"")
          new_list.append(temp.strip())
        
        crc_codes = [i.split(" ")[0] for i in new_list]
        prices = [i.split(" ")[-1] for i in new_list]
        names = [' '.join(i.split(" ")[1:-1]) for i in new_list]
        
        data = pd.DataFrame()
        
        data['CRC Code'] = crc_codes
        data['Item Description'] = names
        data['Price'] = prices
        
        data['Flag'] = ''
        
        for ind in indexes:
          data['Flag'][ind[0]] = ind[1]
    
        st.dataframe(data)

st.markdown('---')

if st.button("AU - Scrape The Total Tools"):
    on_button_click_AU_TotalTools()

if st.button("AU - Scrape Super Cheap Auto"):
    on_button_click_AU_Super()

#if st.button("AU - Scrape BCF"):
#    on_button_click_AU_BFC()

if st.button("AU - Scrape Anaconda"):
    on_button_click_AU_Anaconda()


select_text = st.radio("Select customer",["Tool Kit Depot", "Anaconda", "Repco", "Sydney Tools", "Atom Supply", "Mitre 10", "Autobarn", "BFC", "Auto One", "Tools.com"])


######################################################
######## Tool Kit Depot

if select_text == "Tool Kit Depot":
    text_input = st.text_input("Enter Tool Kit Depot text here:")
    if len(text_input) > 1:
        list1 = [i.split(' DESCRIPTION: ')[0] for i in text_input.replace('Quick view ', '').split('... ')]
        list1 = [i.replace('CRC ','') for i in list1]
        
        raw_prices = [i.split(' ')[0] for i in list1[1:]]
        products = [list1[0]]
        
        for i in list1[1:-1]:
          products.append(' '.join(i.split(' ')[1:]))
        
        names = [i.split('CR')[0].split(' - ')[0].strip() for i in products]
        CRC_codes = [i.split('CR')[1].split(' ')[0].strip() for i in products]
        
        prices = [float(i.split('$')[1]) for i in raw_prices]
        first_prices = []
        for i in raw_prices:
          try:
            first_prices.append(float(i.split('$')[2]))
          except:
            first_prices.append('')
        
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['CRC Code'] = CRC_codes
        data['Price'] = prices
        data['First Price'] = first_prices
        data['TKD Price'] = (data['Price'] * 0.975).round(2)
        
        st.dataframe(data)


######################################################
######## Anaconda
if select_text == "Anaconda":
    text_input = st.text_input("Enter Anaconda text here:")
    if len(text_input) > 1:
        products = [i.strip() for i in text_input.split('CRC')[1:]]

        names = [i.split('(')[0].strip() for i in products]
        prices = [i.split('$')[1].strip() for i in products]
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['Price'] = prices

        st.dataframe(data)

######################################################
######## Repco

if select_text == "Repco":
    text_input = st.text_input("Enter Repco text here:")
    if len(text_input) > 1:
        remove_list = [' 3-7 Days Delivery 3-7 Days ', ' 30min C&C Delivery Same Day* ', ' 1-3 Days Delivery 1-3 Days ']

        try:
          text_input = text_input.replace('CRC Belt Dressing 350G/500Ml' , 'CRC Belt Dressing 350G/500Ml - 1753472')
        except:
          pass

        for i in remove_list:
          text_input = text_input.replace(i,'')
        
        text_input = text_input.replace('store finder icon Click to find in nearby store Not in stock at selected store.','In-Store')
        
        list1 = text_input.split('In-Store')[:-1]
        list1 = [i.split(' - ')[1:3] for i in list1]
        
        names = [i[0] for i in list1]
        CRC_codes = [i[1].split('$')[0].split('(')[0].strip() for i in list1]
        prices = [i[1].split('$')[1].split(' ')[0] for i in list1]
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['CRC Codes'] = CRC_codes
        data['Price'] = prices
    
        st.dataframe(data)

######################################################
######## Sydney Tools

if select_text == "Sydney Tools":
    text_input = st.text_input("Enter Sydney tools text here:")
    if len(text_input) > 1:
        test_list = text_input.split("CRC ")[::3][1:]
    
        new_list,indexes = [],[]
        
        for i in range(len(test_list)):
          temp = test_list[i].strip()
          check = [ "FREE SHIPPING", "Clearance"]
          for word in check:
            if word in temp:
              indexes.append([i+1,word])
              temp = test_list[i].replace(word,"")
          new_list.append(temp.strip())
        
        crc_codes = [i.split(" ")[0] for i in new_list]
        prices = [i.split(" ")[-1] for i in new_list]
        names = [' '.join(i.split(" ")[1:-1]) for i in new_list]
        
        data = pd.DataFrame()
        
        data['CRC Code'] = crc_codes
        data['Item Description'] = names
        data['Price'] = prices
        
        data['Flag'] = ''
        
        for ind in indexes: 
          data['Flag'][ind[0]] = ind[1]
    
        st.dataframe(data)

######################################################
######## Atom Supply

if select_text == "Atom Supply":
    text_input = st.text_input("Enter Atom Supply text here:")
    if len(text_input) > 1:
        text_input = text_input.replace('More information','Add to Cart').replace('Missing Price','$')
    
        products = [i.strip() for i in text_input.split(' Add to Cart Add to Compare')][:-1]
        
        names = []
        for i in products:
          if len(i.split('CRC')[0])>0:
            names.append(i.split('CRC')[0].strip())
          else:
            try:
              names.append(i.split('CRC')[1].strip())
            except:
              pass
        
        ATOM_SKU = [i.split('ATOM Code: ')[1].split(' ')[0] for i in products]
        first_price = [i.split('$')[1].split(' ')[0] for i in products]
        actual_price = [i.split('$')[2].split(' ')[0] for i in products]
        
        data = pd.DataFrame()
        
        data['ATOM_SKU'] = ATOM_SKU
        data['Item Description'] = names
        data['First Price'] = first_price
        data['Actual Price'] = actual_price
    
        st.dataframe(data)
        
######################################################
######## Mitre 10

if select_text == "Mitre 10":
    text_input = st.text_input("Enter Mitre 10 text here:")
    if len(text_input) > 1:
        text_input = text_input.replace('Auto-Kolone', 'CRC Auto-Kolone')
        text_input = text_input.split('CRC')[0::2][1:]
    
        names = [i.split('$')[0].strip() for i in text_input]
        prices =[]
        
        for i in text_input:
          try:
            price = int(i.split('$')[1].split(' ')[0])/100
            prices.append(price)
          except:
            prices.append(' ')
    
        data = pd.DataFrame()
        data['Item Description'] = names
        data['Price'] = prices
    
        st.dataframe(data)

######################################################
######## Autobarn

if select_text == "Autobarn":
    text_input = st.text_input("Enter Autobarn text here:")
    if len(text_input) > 1:
        text_input = text_input.replace('GDI IVD Intake Valve Cleaner', 'GDI IVD Intake Valve Cleaner - 5319')
        text_input = text_input.replace('CRC Moto Plastic Polish 200mL- 1752430', 'CRC Moto Plastic Polish 200mL - 1752430')
        text_input = text_input.replace('CRC Auto AC Pro Cleaner 500mL- 1753204', 'CRC Auto AC Pro Cleaner 500mL - 1753204')
        text_input = text_input.replace('CRC Moto Metal Polish 200mL- 1752436', 'CRC Moto Metal Polish 200mL - 1752436')

        text_input = text_input.split('CRC')[1:]
        
        names = [i.split(' - ')[0].strip() for i in text_input]
        CRC_codes = [i.split(' - ')[1].split(' ')[0] for i in text_input]
        prices = [i.split('$')[1].split(' ')[0] for i in text_input]
        
        first_prices = []
        
        for i in text_input:
          try:
            first_prices.append(i.split('$')[2].split(' ')[0])
          except:
            first_prices.append('')
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['CRC Codes'] = CRC_codes
        data['Price'] = prices
        data['First Price'] = first_prices
        
        st.dataframe(data)

######################################################
######## BFC

if select_text == "BFC":
    text_input = st.text_input("Enter BFC text here:")
    if len(text_input) > 1:
        text_input = text_input.split(', , bcf_hi-res ')[1:]

        names = [i.split('$')[0].strip() for i in text_input]
        prices = [i.split('$')[1].split(' ')[0] for i in text_input]
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['Price'] = prices

        st.dataframe(data)

######################################################
######## Auto One

if select_text == "Auto One":
    text_input = st.text_input("Enter Auto One text here:")
    if len(text_input) > 1:
        text_input = text_input.replace('(PICKUP ONLY) ', '')
        prices = [i.split(' ')[-1].replace('$','') for i in text_input.split(' ADD TO CART Add to Compare')[:-1]]
        CRC_codes = [i.split(' ')[-2] for i in text_input.split(' ADD TO CART Add to Compare')[:-1]]

        data = pd.DataFrame()
        data['CRC Code'] = CRC_codes
        data['Price'] = prices

        st.dataframe(data)

######################################################
######## Tools.com

if select_text == "Tools.com":
    text_input = st.text_input("Enter Tools.com text here:")
    if len(text_input) > 1:
        products = [i.strip() for i in text_input.split(' Add To cart')][:-1]

        names = [i.split('$')[0].strip() for i in products]
        prices = [i.split('$')[1].split(' ')[0] for i in products]
        CRC_codes = [i.split(' ')[-1] for i in products]
        
        data = pd.DataFrame()
        data['Item Description'] = names
        data['CRC Code'] = CRC_codes
        data['Price'] = prices

        st.dataframe(data)
