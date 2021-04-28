import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time as t
from datetime import datetime


class CrawlingData(object):
    # class variable

    def __init__(self, user_agent, chrome_path, root_url, search_window_xpath, search_window_xpath_icon_xpath):
        self.user_agent = user_agent
        self.chrome_path = chrome_path
        self.root_url = root_url
        self.search_window_xpath = search_window_xpath
        self.search_window_xpath_icon_xpath = search_window_xpath_icon_xpath

    def set_crawling_option(self):
        options = Options()
        options.add_argument(f'user-agent={self.user_agent}')
        browser = webdriver.Chrome(chrome_options=options, executable_path=self.chrome_path)
        browser.maximize_window()
        return browser

    def set_crawling_main_page(self, browser, product):
        browser.get(self.root_url)
        elem = browser.find_element_by_xpath(self.search_window_xpath)  # 검색 insert box 위치 입력
        elem.click()
        elem.send_keys(product)  # - product 명이 입력됨
        elem = browser.find_element_by_xpath(self.search_window_xpath_icon_xpath)  # - 검색 아이콘 위치 입력
        elem.click()


class BunjangCrawlingData(CrawlingData):
    bunjang_cols = ['transaction_id','category','title', 'price',
                    'time', 'main_contents', 'like', 'click_number','seller_location',
                    'seller_review_num','item_image', 'user_info', 'data_collect_time']

    def __init__(self, user_agent, chrome_path, root_url, search_window_xpath,
                 search_window_xpath_icon_xpath, page_num, logger):
        super(BunjangCrawlingData, self).__init__(user_agent,
                                                  chrome_path,
                                                  root_url,
                                                  search_window_xpath,
                                                  search_window_xpath_icon_xpath)
        self.page_num = page_num
        self.logger = logger

    def get_crawling_data_items(self, browser, transaction_num, product_meta_code):

        current_time = t.strftime('%y%m%d%H%M%S')
        t.sleep(3)  # - 페이지를 넘길 때, term을 주어야 데이터를 정상적이게 가져 올 수 있음
        browser.find_elements_by_class_name("sc-iFUGim")[transaction_num].click()  # - 하나의 제품 이미지 클릭
        transaction_id = product_meta_code + "_" + current_time                                        # transcation_id
        category = product_meta_code                                                             # catgory
        t.sleep(3)
        soup = BeautifulSoup(browser.page_source, "lxml")  # - page source parser를 통해 source 가져옴
        title = soup.find('div', attrs={'class': 'sc-fIIFii iptAEp'}).get_text()                 # title
        price = soup.find('div', attrs={'class': 'sc-frudsx kGPCet'}).get_text()                 # price
        time = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[2].get_text()           # time
        main_contents = soup.find('div', attrs={'class': 'sc-huKLiJ bfuCPC'}).get_text()         # main_contents
        like = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[0].get_text()           # like
        click_number = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[1].get_text()   # click number
        try:
            seller_location = soup.find('div', attrs={'class': 'sc-kJdAmE jHNBWQ'}).get_text()   # seller_location
        except:
            seller_location = soup.find('div', attrs={'class': 'sc-kJdAmE jVepRm'}).get_text()
        seller_review_num = soup.find('div', attrs={'class': "sc-kBMPsl ivBHfZ"}).get_text()     # seller_review_num

        ## item_image ##

        ################
        user_info = soup.find('div', attrs={'class': "sc-biNVYa bNKxkj"}).get_text()             # user_info
        data_collect_time = str(datetime.strftime(datetime.strptime(current_time, "%y%m%d%H%M%S"), "%y-%m-%d %H:%M:%S"))

        bunjang_data = [transaction_id, category, title, price,
                        time, main_contents, like, click_number, seller_location,
                        seller_review_num, user_info, data_collect_time]
        self.logger.info(bunjang_data)
        browser.back()

        return bunjang_data

    def get_crawling_data(self, product, browser, product_meta_code):

        bunjang_data = pd.DataFrame(columns=BunjangCrawlingData.bunjang_cols)

        page_num = self.page_num
        limit_num = 1

        while True:
            t.sleep(3)
            if page_num == 1:
                start = 1
            else:
                start = 2  # - 11 page 부터 < 존재하므로, 2부터 시작
            # j = 1
            for j in range(start, len(browser.find_elements_by_class_name("sc-fdqjUm"))):
                browser.find_elements_by_class_name("sc-fdqjUm")[j].click()  # - page 클릭
                for page_items_num in range(100):
                    limit_num += 1
                    try:
                        bunjang_data_dict = self.get_crawling_data_items(browser, transaction_num=page_items_num,
                                                                         product_meta_code=product_meta_code)
                        row_names = str(page_num) + "_" + str(page_items_num)
                        for i in range(len(bunjang_data_dict)):
                            bunjang_data.loc[row_names, BunjangCrawlingData.bunjang_cols[i]] = bunjang_data_dict[i]
                    except Exception as e:
                        try:
                            super(BunjangCrawlingData, self).set_crawling_main_page(browser, product)
                            t.sleep(3)
                            browser.find_elements_by_class_name("sc-fdqjUm")[j].click()
                            browser.execute_script('window.scrollTo(0, 0)')
                            t.sleep(3)
                            bunjang_data_dict = self.get_crawling_data_items(browser, transaction_num=page_items_num,
                                                                             product_meta_code=product_meta_code)
                            row_names = str(page_num) + "_" + str(page_items_num)
                            for i in range(len(bunjang_data_dict)):
                                bunjang_data.loc[row_names, BunjangCrawlingData.bunjang_cols[i]] = bunjang_data_dict[i]
                            print(bunjang_data_dict[0], " : ", page_items_num)
                        except Exception as e:
                            self.logger.error(e)
                            return bunjang_data

                    print("item number : ", limit_num)
                    if limit_num == 100:
                        return bunjang_data

        return bunjang_data
