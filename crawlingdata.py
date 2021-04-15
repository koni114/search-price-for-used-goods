import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import time as t


class crawlingdata(object):
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


class bunjangCrawlingdata(crawlingdata):
    bunjang_cols = ['title', 'price', 'time', 'content', 'like', 'Attention', 'location']

    def __init__(self, user_agent, chrome_path, root_url, search_window_xpath, search_window_xpath_icon_xpath):
        super(bunjangCrawlingdata, self).__init__(user_agent,
                                                  chrome_path,
                                                  root_url,
                                                  search_window_xpath,
                                                  search_window_xpath_icon_xpath)

    def get_crawling_data_items(self, browser, transaction_num):

        t.sleep(3)  # - 페이지를 넘길 때, term을 주어야 데이터를 정상적이게 가져 올 수 있음
        browser.find_elements_by_class_name("sc-iFUGim")[transaction_num].click()  # - 하나의 제품 이미지 클릭
        t.sleep(3)
        soup = BeautifulSoup(browser.page_source, "lxml")  # - page source parser를 통해 source 가져옴
        title = soup.find('div', attrs={'class': 'sc-fIIFii iptAEp'}).get_text()  # - title class
        price = soup.find('div', attrs={'class': 'sc-frudsx kGPCet'}).get_text()  # - price class

        # - 지역인증 여부에 따라 class가 달라지므로, 이에 따른 로직 적용
        try:
            location = soup.find('div', attrs={'class': 'sc-kJdAmE jHNBWQ'}).get_text()
        except:
            location = soup.find('div', attrs={'class': 'sc-kJdAmE jVepRm'}).get_text()

        like = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[0].get_text()  # - 찜기능
        attention = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[1].get_text()  # - 관심
        time = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[2].get_text()  # - 시간
        content = soup.find('div', attrs={'class': 'sc-huKLiJ bfuCPC'}).get_text()  # - 본문 내용

        bunjang_data = [title, price, time, content, like, attention, location]
        print(bunjang_data)
        browser.back()

        return bunjang_data

    def get_crawling_data(self, product, browser):

        bunjang_crawling_contents = ['title', 'price', 'time', 'content', 'like', 'Attention', 'location']
        bunjang_data = pd.DataFrame(columns=bunjang_crawling_contents)

        page_num = 1
        limit_num = 1000
        while True:
            check_number = 0
            t.sleep(3)
            if page_num == 1:
                start = 1
            else:
                start = 2
            for j in range(start, len(browser.find_elements_by_class_name("sc-fdqjUm"))):
                browser.find_elements_by_class_name("sc-fdqjUm")[j].click()  # - page 클릭
                for page_items_num in range(100):
                    try:
                        bunjang_data_dict = self.get_crawling_data_items(browser, transaction_num=page_items_num)
                        row_names = str(page_num) + "_" + str(page_items_num)
                        for i in range(len(bunjang_data_dict)):
                            bunjang_data.loc[row_names, bunjang_crawling_contents[i]] = bunjang_data_dict[i]
                    except Exception as e:
                        print(e)
                        super(bunjangCrawlingdata, self).set_crawling_main_page(browser, product)
                        t.sleep(3)
                        browser.find_elements_by_class_name("sc-fdqjUm")[j].click()
                        browser.execute_script('window.scrollTo(0, 0)')
                        t.sleep(3)
                        bunjang_data_dict = self.get_crawling_data_items(browser, transaction_num=page_items_num)
                        row_names = str(page_num) + "_" + str(page_items_num)
                        for i in range(len(bunjang_data_dict)):
                            bunjang_data.loc[row_names, bunjang_crawling_contents[i]] = bunjang_data_dict[i]
                        print(bunjang_data_dict[0], " : ", page_items_num)

                        if check_number == limit_num:
                            break

                        check_number += 1
            break
        return bunjang_data
