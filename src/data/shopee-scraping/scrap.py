from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as ec

from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import json
import re
from time import gmtime, strftime
import csv

url = "https://shopee.co.id/Handphone-Tablet-cat.40.1211?page=0&sortBy=pop"

# create a new Chrome session
driver = webdriver.Chrome()
driver.implicitly_wait(300)
driver.get(url)

product_count = 1
total_count = 1
data = []
page = 0

while (page <= 99):

    soup = BeautifulSoup(driver.page_source, 'lxml')

    product_links = []
    product_rating_count = []

    while (len(product_links) == 0):
        result_item = driver.find_elements_by_xpath("//script[@type='application/ld+json']")

        while(len(result_item) < 52):
            result_item = driver.find_elements_by_xpath("//script[@type='application/ld+json']")

        for result in result_item:
            try:
                script_content = result.get_attribute('innerHTML')
            except:
                continue

            result_json = json.loads(script_content)
            if (result_json['@type'] == 'Product'):
                product_links.append(result_json['url'])
                try:
                    product_rating_count.append(int(result_json['aggregateRating']['ratingCount']))
                except:
                    product_rating_count.append(0)

    for idx, link in enumerate(product_links):

        if (product_rating_count[idx] != 0):
            item = {}
            try:
                driver.get(link)
                content = BeautifulSoup(driver.page_source, 'lxml')
            except Exception as e:
                break
            
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')

            # Kategori
            item['kategori'] = 'Handphone & Tablet'

            # Nama Produk
            item['nama_produk'] = ''
            try:
                product_name = driver.find_element_by_class_name('qaNIZv').text
                product_name = product_name.replace('Star Seller\n', '')
                item['nama_produk'] = product_name
            except Exception as e:
                pass

            # Harga
            item['harga'] = ''
            try:
                price = driver.find_element_by_class_name('_3n5NQx').text
                price = price.replace('Rp', '')
                item['harga'] = price
            except Exception as e:
                pass

            # Kondisi
            item['kondisi'] = '-'

            isRatingLoaded = False
            try:
                review_button = driver.find_element_by_class_name('M3KjhJ')
                review_button.click()

                review_position = driver.find_element_by_class_name('product-ratings')
                driver.execute_script("arguments[0].scrollIntoView();", review_position)

                isRatingLoaded = True
            except Exception as e:
                pass

            review_count = 1

            while (review_count <= product_rating_count[idx] and isRatingLoaded):
                reviews = []
                reviewers = []
                ratings = []
                reviews_time = []

                try:
                    reviews = driver.find_elements_by_css_selector('div.shopee-product-rating__main > div.shopee-product-rating__content')
                    reviewers = driver.find_elements_by_css_selector('div.shopee-product-rating__main > a')
                    ratings = driver.find_elements_by_css_selector('div.shopee-product-rating__main > div.shopee-product-rating__rating > svg > polygon')
                    reviews_time = driver.find_elements_by_css_selector('div.shopee-product-rating__main > div.shopee-product-rating__time')
                except Exception as e:
                    product_rating_count[idx] -= 6
                    continue

                for i in range(len(reviews)):
                    # Reviewer
                    item['reviewer'] = reviewers[i].text

                    # Rating
                    rating_count = 5
                    for n in range(0,5):
                        if (ratings[i*5 + n].get_attribute('fill') == 'none'):
                            rating_count -= 1
                    item['rating'] = str(rating_count)

                    # Review
                    item['review'] = reviews[i].text.strip().replace('\n', ' ')
                    
                    # Waktu Review
                    review_time = reviews_time[i].text
                    bar_char_idx = review_time.find('|')
                    if (bar_char_idx != -1):
                        review_time = review_time[:bar_char_idx-1]
                    item['tanggal_review'] = review_time

                    # Waktu Ambil
                    item['tanggal_ambil'] = strftime("%Y-%m-%d %H:%M", gmtime())

                    # url
                    item['url'] = driver.current_url
                    
                    # test
                    print(str(product_count) + ' - ' +str(review_count) + ' - ' + str(total_count))
                    
                    data.append(item.copy())

                    review_count += 1
                    total_count += 1

                    # checkpoint
                    if (total_count % 5000 == 0):
                        df = pd.DataFrame(data)
                        df.to_csv('shopee'+ str(total_count) +'.csv', encoding='utf-8', index=False, quoting=csv.QUOTE_ALL)
                        if (total_count != 5000):
                            os.remove('shopee'+ str(total_count-5000) +'.csv')


                # click next button
                try:
                    next_review_button = driver.find_element_by_css_selector('div.product-ratings__page-controller > button.shopee-icon-button--right')
                    next_review_button.click()
                except:
                    break
            
            product_count += 1

    page += 1

    df = pd.DataFrame(data)
    df.to_csv('shopee_page'+ str(page) +'.csv', encoding='utf-8', index=False, quoting=csv.QUOTE_ALL)

    try:
        next_url = 'https://shopee.co.id/Handphone-Tablet-cat.40.1211?page='+ str(page) +'&sortBy=pop'
        driver.get(next_url)
        content = BeautifulSoup(driver.page_source, 'lxml')
    except:
        continue
    

df = pd.DataFrame(data)
df.to_csv('shopee_final.csv', encoding='utf-8', index=False, quoting=csv.QUOTE_ALL)

#end the Selenium browser session
driver.quit()
