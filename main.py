import os
import re
import time
import datetime
import requests
import json
import pandas as pd
import traceback
import parse
from bs4 import BeautifulSoup as bs
from selenium import webdriver

######################################################
import create_plot
######################################################
#https://jeongwookie.github.io/2019/03/18/190318-naver-finance-data-crawling-using-python/
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') 
chrome_options.add_argument('--disable-gpu') 
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--lang=ko_KR')

driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver', options=chrome_options)
    #'/usr/bin/chromedriver'
    #'/home/prohenho7138/Downloads/chromedriver'
driver.implicitly_wait(1)

def crawling_table(drivers, code, page, csv, get_path):
    try:
        driver = drivers
        site = 'https://finance.naver.com/item/sise_day.nhn?code={code}&page={page}'.format(code = code, page = page)
        driver.get(site)
        #https://finance.naver.com/item/sise_day.nhn?code=263750&page=1

        html = driver.page_source
        soup = bs(html, 'lxml')
        
        driver.execute_script('window.open("about:blank", "_blank");')
        driver.close()
    
        tabs = driver.window_handles
        driver.switch_to.window(tabs[-1])
        
        return soup
    except Exception as error:
        traceback.print_exc()
    return None

def len_table(html):
    try:
        soup = html
        find_table = soup.find('table', class_ = 'Nnavi')
        last_table = find_table.find('td', class_ = 'pgRR')
        len_table = last_table.a.get('href').rsplit('&')[1]
        len_table = len_table.split('=')[1]
        len_table = int(len_table)
        return len_table
    except Exception as error:
        traceback.print_exc()
    return None

def create_csv(data, csv):
    try:
        result = data
        if os.path.isfile(csv):
            result.to_csv(csv, mode = 'a', header = False)
            re_result = pd.read_csv(csv, index_col = 0)
            all_result = re_result.sort_values(by = ['날짜'], axis = 0)
            all_result = all_result.drop_duplicates('날짜', keep = 'first')
            all_result.to_csv(csv, mode = 'w')
        else:
            result.to_csv(csv, mode = 'w')
        return result
    except Exception as error:
        traceback.print_exc()
    return None

######################################################
#263750 펄어비스
code = '005930' #삼성
page = 1
csv = './code/{code}/{code}.csv'.format(code = code)
png = './code/{code}/{code}.png'.format(code = code)
get_path = './code/{code}'.format(code = code)

result = crawling_table(driver, code, page, csv, get_path)
len_table = len_table(result)

for page in range(1, int(len_table) + 1):
    result = crawling_table(driver, code, page, csv, get_path)
    result = pd.read_html(str(result.find('table')), header = 0)[0]
    result = result.dropna()
    if os.path.isdir(get_path):
        create_csv(result, csv)
        print(str(round(page / len_table * 100)) + "% 완료했습니다.")
    else:
        os.makedirs(get_path)
        create_csv(result, csv)

save_png = create_plot.create_plot(code, csv, png)

driver.quit()
######################################################