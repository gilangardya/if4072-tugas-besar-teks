from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import datetime
from selenium.webdriver.common.by import By
import sys
import time

tok_url = "https://www.tokopedia.com/p/handphone-tablet/handphone?ob=5&page="

if(len(sys.argv) != 3):
    print("Penggunaan: python tokopediascraping.py page-awal page-akhir > file.txt")
    exit(0)

driver = webdriver.Chrome()
driver.implicitly_wait(0)

for x in range(int(sys.argv[1]), int(sys.argv[2])):
    try:
        print('--------page' + str(x))
        driver.get(tok_url + str(x))
        soup_level1=BeautifulSoup(driver.page_source, 'html.parser')
        alternate = True
        for link in soup_level1.find_all("a", {"ng-click":"NgTrack('product', model.department_id)"}):
            if alternate:
                try:
                    url = link["ng-href"]
                    driver.get(url)
                    driver.find_element_by_xpath("//*[@id='review-tab']").click()
                    soup_level2=BeautifulSoup(driver.page_source, 'html.parser')
                    title = soup_level2.find("h1", {"class":"rvm-product-title"}).contents[0]
                    if (str(title) == '\r\n'):
                    	title = soup_level2.find("span", {"itemprop":"name"}).contents[0]
                    price = soup_level2.find("span", {"itemprop":"price"})['content']
                    condition = soup_level2.find("link", {"itemprop":"itemCondition"})['href']
                    for i in range (2,7):
                        try:
                            time.sleep(2)
                            driver.find_element_by_xpath("//*[@class='product-review-filter']/ul/li["+str(i)+"]").click()
                            is_nextpage = True
                            while (is_nextpage):
                                time.sleep(2)
                                for review in driver.find_elements_by_xpath("//*[@class='list-box-comment']"):
                                    try:
                                        review_source = BeautifulSoup(review.get_attribute("innerHTML"), 'html.parser')
                                        body = review_source.find("span", {"class":"review-body"}).contents[0]
                                        reviewer = review_source.find("a", {"class":"text-black-7 fw-600 text-hover-green"})
                                        if reviewer is None:
                                            reviewer = review_source.find("span", {"class":"text-black-7 fw-600"})
                                        reviewer = reviewer.contents[0]
                                        date = review_source.find("span", {"class":"text-black-18 fs-12 ml-8"}).contents[0]
                                        rating = review_source.find("meta", {"itemprop":"ratingValue"})['content']
                                        a= ["Handphone", title, price, condition, body, rating, reviewer, date, str(datetime.datetime.now()), url]
                                        print (str(a[0])+"||||"+str(a[1])+"||||"+str(a[2])+"||||"+str(a[3])+"||||"+str(a[4])+"||||"+str(a[5])+"||||"+str(a[6])+"||||"+str(a[7])+"||||"+str(a[8])+"||||"+str(a[9]))
                                    except:
                                        pass

                                try:
                                    driver.find_element_by_xpath("//div[@class='pagination pull-right']//i[@class='icon-chevron-right-alt fs-20']").click()
                                except:
                                    is_nextpage = False
                        except:
                            pass
                except:
                    pass
            alternate = not(alternate)
    except:
        pass

driver.quit()
