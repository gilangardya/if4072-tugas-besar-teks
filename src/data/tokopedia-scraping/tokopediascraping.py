from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import datetime
from selenium.webdriver.common.by import By
import sys

url = "https://www.tokopedia.com/p/handphone-tablet/handphone?page="

if(len(sys.argv) != 3):
	print("Penggunaan: python tokopediascraping.py page-awal page-akhir > file.txt")
	exit(0)

driver = webdriver.Chrome()
driver.implicitly_wait(30)

for x in range(int(sys.argv[1]), int(sys.argv[2])):
    print('--------' + str(x))
    driver.get(url + str(x))
    soup_level1=BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup_level1.find_all("a", {"ng-click":"NgTrack('product', model.department_id)"}):
        try:
            url = link["ng-href"]
            driver.get(url)
            tab_button = driver.find_element_by_id('review-tab')
            tab_button.click()
            is_nextpage = True

            soup_level2=BeautifulSoup(driver.page_source, 'html.parser')
            title = soup_level2.find("h1", {"class":"rvm-product-title"}).contents
            price = soup_level2.find("span", {"itemprop":"price"})['content']
            condition = soup_level2.find("link", {"itemprop":"itemCondition"})['href']
            while (is_nextpage):
                soup_level2=BeautifulSoup(driver.page_source, 'html.parser')
                for review in soup_level2.find_all("div", {"class":"list-box-comment"}):
                    try:
                        body = review.find("span", {"class":"review-body"}).contents
                        reviewer = review.find("a", {"class":"text-black-7 fw-600 text-hover-green"}).contents
                        date = review.find("span", {"class":"text-black-18 fs-12 ml-8"}).contents
                        rating = review.find("meta", {"itemprop":"ratingValue"})['content']
                        a= ["Handphone", title, price, condition, body, rating, reviewer, date, str(datetime.datetime.now()), url]
                        print (str(a).encode("utf-8"))
                    except:
                        pass
                try:
                    next_but = driver.find_element_by_css_selector('.icon-chevron-right-alt.fs-20')
                    td_p_input = next_but.find_element_by_xpath('..')
                    td_p_input.click()  
                except:
                    is_nextpage = False
            
        except: 
            pass
driver.quit()
