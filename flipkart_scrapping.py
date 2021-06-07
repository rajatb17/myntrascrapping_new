# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:46:28 2021

@author: Administrator
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import math
from datetime import datetime
from pandas.io.json import json_normalize
import os
import urllib
from selenium.webdriver.common.action_chains import ActionChains
import matplotlib
import matplotlib.pyplot as plt
import re
#from pymongo import MongoClient
import json

#edit
url = 'https://www.myntra.com/lifestyle?extra_search_param=isautosuggestentry%3atrue%3a%3aid%3a2297-lifestyle'
path_chrome = r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe'
path = r'D:\Rajat stuff\myntra_scraping.csv'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
site = 'Myntra'
        
#defining the result container
division_lst = []
dept_lst = []
cat_lst = []
cat_url_lst = []
product_name_lst = []
product_brand_lst = []
product_url_lst = []
cur_price_lst = []
page_no_lst = []
currency_lst = []
org_price_lst = []
disc_per_lst = [] 
index_lst = []
time_lst = []
site_lst = []
offer_lst = []
disc_avail_lst = []

#page = requests.get(url,headers=headers)
#, proxies = PROXY
#source = page.text

browser = webdriver.Chrome(executable_path = path_chrome)
browser.get(url)
source = browser.page_source
                        
#creating the beautiful soup object
soup = BeautifulSoup(source, 'html5lib')
#print(soup)

itm_count = 0
itm_count = soup.find('span', {'class':'title-count'}).text.strip().split()[1]
#print(itm_count)


item_list = soup.findAll('li', {'class' : 'product-base'})
#print(len(item_list))
#print(item_list)
#print(item_list)
curr_price = []
price = []
orig_price = []
product_disc_1 = []
product_disc_2 = []
#product_disc_1 = soup.findAll('span',{'class':'product-discountPercentage'})
#for i in product_disc_1:
    #print(i.text) #doubt 1
#    product_disc_2.append(i.text) 
#print(product_disc_2)    
index = 0
number = 0
#zxc = []

for it in item_list:
    product_brand = it.find('h3', {'class' : 'product-brand'}).text.strip().split()
    product_name = it.find('h4',{'class':'product-product'}).text.strip()
#    product_disc_1 = it.find('span',{'class':'product-discountPercentage'})
    #for i in product_disc_1:
    #print(i.text) #doubt 1
    #zxc = product_disc_1.text
    #product_disc_2.append(zxc) 
    #product_disc_2.append(product_disc_1) 

    product_url = 'https://www.myntra.com/'+it.find('a')['href']
    product_price = it.find('div',{'class':'product-price'}) #includes both current and discounted price
    price = product_price.find('span').text.strip().split()#.rstrip('Rs.')  
    curr_price.append(price[1].rstrip('Rs.'))
    orig_price.append(price[-1])
    product_price_1 = ((int(orig_price[number]) -  int(curr_price[number]))/int(orig_price[number]) * 100)
    product_disc_1.append(product_price_1)
    product_disc_2 = round(product_disc_1[number])
    disc_avail = bool(product_disc_2)
    now = datetime.now()
    now = now.strftime("%m/%d/%Y %H:%M:%S")
    index = index+1
#print(now)

#product_df = pd.read_csv(path)

    index_lst.append(index)
    time_lst.append(now)
    product_name_lst.append(product_name)
    product_brand_lst.append(product_brand[0])
    product_url_lst.append(product_url)
    cur_price_lst.append(curr_price[number])
    org_price_lst.append(orig_price[number])
    disc_avail_lst.append(disc_avail)
    disc_per_lst.append(product_disc_2)
    site_lst.append(site)
    
    number = number+1
    
    item_dict = {'Index':index_lst,
                 'TimeStamp':time_lst,
#             'Division': division_lst,
#             'Department': dept_lst,
#             'Category': cat_lst,
#             'CategoryUrl': cat_url_lst,
                 'Site': site_lst,
                 'ProductName': product_name_lst,
                 'ProductUrl': product_url_lst,
#             'Page No':page_no_lst,
#             'Tag':offer_lst,
                 'ProductBrand': product_brand_lst,
                 'OriginalPrice':org_price_lst,
                 'CurrentPrice':cur_price_lst,
                 'DiscAvailable':disc_avail_lst,
                 'Discount%': disc_per_lst}

#print(product_disc_1.text)
#print("---------------")
#print(orig_price)

item_df = pd.DataFrame(item_dict)

#date as title for saving file             
date = datetime.now()
date = date.strftime("%Y%m%d")
#print(date)  
#saving the dataframe
file_path = os.path.join(path.rsplit('\\', 1)[0],'Output',date) #creating a file eveyrtime we scrape with the date as file title in Output folder
#print(file_path)
if not os.path.exists(file_path):
    os.makedirs(file_path)
else:
    pass 
            
#            records = json.loads(item_df.T.to_json()).values()
#            db.flipkart_plp.insert_many(records)
item_df.to_csv(os.path.join(file_path,'myntra_scraping.csv'), index=False)



#-----------PDP------------

features_lst = []
size_lst = []


            

size_dic = {}
h=0
l=0
prod_info = []
prod_offer = []
best_pr_price = []
prod_specs = []

# for itm in range(len(item_df)): #number of rows in dict above 
#     print(itm)
    # url_pdp = item_df.loc[itm,'ProductUrl'] #access pdp URL from dict using row and col index locn 
    
    
url_pdp = 'https://www.myntra.com/tops/code-by-lifestyle/code-by-lifestyle-women-pink-solid-top/13215138/buy'
browser = webdriver.Chrome(executable_path = path_chrome)
browser.get(url_pdp)
source_pdp = browser.page_source            
soup_pdp = BeautifulSoup(source_pdp, 'html5lib')

detail = soup_pdp.find('div', {'class':'meta-container'})#.text.split() #all info lines of product as single element in the list
#print(detail)

#storing each line individually in diff element and appending
for i in detail:
    line = i.text
    prod_info.append(line)
#print(prod_info)

best_price = int(soup_pdp.find('span', {'class' : 'pdp-offers-price'}).text.lstrip(' Rs.'))
best_pr_price.append(best_price)

offers = soup_pdp.findAll('div', {'class' : 'pdp-offers-labelMarkup'})
#print(offers)

for i in offers:
    line = i.text
    prod_offer.append(line)
#print(prod_offer)

specifications = soup_pdp.findAll('div', {'class':'index-row'})
#print(specifications)

int_dic = {}
flat_list_1 = []
flat_list_2 = []

#specifications table on myntra
for i in specifications:
    table_head = i.find('div', {'class':'index-rowKey'}).text.strip().split('\n')
    #print(table_head)
    #for j in table_head:
    flat_list_1.append(table_head)
    head = [item for sublist in flat_list_1 for item in sublist]
    #print(head)    
    table_value = i.find('div', {'class':'index-rowValue'}).text.strip().split('\n')
    #for j in table_value:
    flat_list_2.append(table_value)
    values = [item for sublist in flat_list_2 for item in sublist]
    #print(values)
int_dic = dict(zip(head,values))
#    line = i.text.strip('\n')
#    prod_specs.append(line)
print(int_dic)   
#print(values)
#print(head) 


#taking dept, category and group     
temp=[]
prod_group = []
prod_category = []
prod_dept = []
group = soup_pdp.findAll('a', {'class' : 'breadcrumbs-link'})
#print(group.text)
for i in group:
    line = i.text
    temp.append(line)
prod_group.append(temp[1])
prod_dept.append(temp[2])
prod_category.append(temp[3])
print(prod_group, prod_dept, prod_category) 





   # if i >0 and i<4:
    #     prod_group.append()


#    for i in cur_price:
#        price = i[2]   
#        print(price)
       #        if cur_price[2]== 'NA':
#            org_price = cur_price[1]
#        else:
#            org_price = cur_price[2]
#    print(org_price)

#    org_price = float(item.find('span',{'class':'pre_reduction'}).text.strip().split(' ')[0])
    #print(product_name)
#item = item_list[0]                                               
#product_name_lst = item.find('div', {'class':'product-price'})
#print(item_list)


#selenium


#soup = BeautifulSoup(source, 'html5lib')

#item_count = browser.find_element_by_class_name('title-count').text.split()[1]
#print(item_count)
#product_name = soup.find('h4', {'class' : 'product-product'}).text.strip()

#//*[@id="desktopSearchResults"]/div[2]/section/ul/li[1]/a
#//*[@id="desktopSearchResults"]/div[2]/section/ul/li[1]/a/div[2]/h3
#//*[@id="desktopSearchResults"]/div[2]/section/ul/li[1]/a/div[2]/div/span

#itm_list = browser.find_elements_by_class_name('results-base')
#print(itm_list)
#for i in itm_list:
#    products = i.find_element_by_xpath('//*[@id="desktopSearchResults"]/div[2]/section/ul/li[1]/a/div[2]/h3').text
#    print(products)
