import requests
import time
from bs4 import BeautifulSoup
import io
import sys
import csv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
name_list=[]
price_list=[]
holder_list=[]
start=1

parsing_list=["https://www.national-azabu.net/products/list?category_id=69&pageno=",
            "https://www.national-azabu.net/products/list?category_id=144&pageno=",
            "https://www.national-azabu.net/products/list?category_id=125&pageno=",
            "https://www.national-azabu.net/products/list?category_id=1&pageno=",
            "https://www.national-azabu.net/products/list?category_id=2&pageno=",
            "https://www.national-azabu.net/products/list?category_id=3&pageno=",
            "https://www.national-azabu.net/products/list?category_id=5&pageno=",
            "https://www.national-azabu.net/products/list?category_id=23&pageno=",
            "https://www.national-azabu.net/products/list?category_id=148&pageno=",
            ]
            
for url in parsing_list:
    website = requests.get(url+"1", headers=HEADERS) 
    website.encoding = 'UTF-8'
    time.sleep(1)  
    doc0 = BeautifulSoup(website.content, 'html.parser')

    pagelist = doc0.find("span", id="productscount")
    if pagelist:
        try:
            product_count = int(pagelist.text.strip())
            fullpage_list = (product_count + 99) // 100 
            for y in range(1, fullpage_list + 1):
                holder_list.append(url + f"{y}"+"&disp_number=100") 
            
        except ValueError:
            print("Item count does not exit")


with open('WholeFoods-2.csv', 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Item', 'Price'])

    for items in holder_list:
        website = requests.get(items, headers=HEADERS)
        website.encoding = 'UTF-8'
        time.sleep(1)
        doc = BeautifulSoup(website.content, 'html.parser')
        name_list_elements = doc.find_all("dt", class_="item_name")
        price_list_elements = doc.find_all("span", class_="price01_default")
        
        for name_element, price_element in zip(name_list_elements, price_list_elements):
            name = name_element.text.strip()
            price = "¥"+price_element.text.strip()
            writer.writerow([name, price])



