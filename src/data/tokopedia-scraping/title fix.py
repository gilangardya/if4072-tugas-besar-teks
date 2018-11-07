from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import datetime
from selenium.webdriver.common.by import By
import sys
import time

driver = webdriver.Chrome()
driver.implicitly_wait(0)
data = pd.read_csv('link_unik_no_title.csv', names = ['link'])
data_array = np.array(data)

for link in data_array:
    try:
        link = link[0]
        proxies = {'http': 'http://davidtsaksomo:83002117@cache.itb.ac.id:8080', 'https': 'https://davidtsaksomo:83002117@cache.itb.ac.id:8080'}
        driver.get(link)
        page_content = BeautifulSoup(driver.page_source, "html.parser")
        title = page_content.find("span", {"itemprop":"name"}).contents[0]
        print("\""+title+"\",\""+link+"\"")
    except:
        pass

driver.quit()
