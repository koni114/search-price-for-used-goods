from bs4 import BeautifulSoup  # - parser. http 통신
from selenium import webdriver  # - 동적으로 화면을 이동하여 크롤링 할 수 있게 하는 framework.
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time as t


# - 초기 설정. configuration 내용.
# - 크롬 드라이버 설치 필요.
def start_option():
    options = Options()
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    options.add_argument(f'user-agent={userAgent}')
    chrome_path = r"/Users/taewoong/Documents/coding/chromedriver"
    brower = webdriver.Chrome(chrome_options=options, executable_path=chrome_path)
    brower.maximize_window()
    return brower


# - 검색하고 싶은 삼품을 product 변수로 입력하면 해당 제품이 검색된 사이트로 들어가짐
def serch_p(brower, product):
    # - url setting
    url = "https://www.bunjang.co.kr/"
    brower.get(url)
    # - 입력할 수 있는 상품 검색 창을 찾고, 커서로 클릭(click())
    elem = brower.find_element_by_xpath("//*[@id='root']/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/input")
    elem.click()
    elem.send_keys(product)  # - product 명이 입력됨
    # xpath(html에서 img의 위치를 출력). className..
    elem = brower.find_element_by_xpath(
        "//*[@id='root']/div/div/div[3]/div[1]/div[1]/div[1]/div[1]/a/img")  # - 검색 아이콘을 찾는
    elem.click()


def Crawling(product, date):
    brower = start_option()
    serch_p(brower, product)
    data_bunjang = pd.DataFrame(columns=['title', 'price', 'time', 'content', 'like', 'Attention', 'location'])
    page_num = 1
    while True:
        t.sleep(3)
        if page_num == 1:
            start = 1
        else:
            start = 2
        for j in range(start, len(brower.find_elements_by_class_name("sc-fdqjUm"))):  # - page 길이
            brower.find_elements_by_class_name("sc-fdqjUm")[j].click()  # - page 클릭
            for i in range(100):
                try:
                    t.sleep(1)  # - 페이지를 넘길 때, term을 주어야 데이터를 정상적이게 가져 올 수 있음
                    brower.find_elements_by_class_name("sc-iFUGim")[i].click()  # - 하나의 제품 이미지 클릭
                    t.sleep(1)
                    soup = BeautifulSoup(brower.page_source, "lxml")  # - page source parser를 통해 source 가져옴
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
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'title'] = title
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'price'] = price
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'location'] = location
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'like'] = like
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'Attention'] = attention
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'time'] = time
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'content'] = content
                    brower.back()
                except:
                    serch_p(brower, product)
                    t.sleep(1)
                    brower.find_elements_by_class_name("sc-fdqjUm")[j].click()
                    brower.execute_script('window.scrollTo(0, 0)')
                    t.sleep(1)
                    brower.find_elements_by_class_name("sc-iFUGim")[i].click()
                    t.sleep(1)
                    soup = BeautifulSoup(brower.page_source, "lxml")
                    title = soup.find('div', attrs={'class': 'sc-fIIFii iptAEp'}).get_text()
                    price = soup.find('div', attrs={'class': 'sc-frudsx kGPCet'}).get_text()
                    try:
                        location = soup.find('div', attrs={'class': 'sc-kJdAmE jHNBWQ'}).get_text()
                    except:
                        location = soup.find('div', attrs={'class': 'sc-kJdAmE jVepRm'}).get_text()
                    like = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[0].get_text()
                    attention = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[1].get_text()
                    time = soup.find_all('div', attrs={'class': 'sc-fQfKYo kctXcC'})[2].get_text()
                    content = soup.find('div', attrs={'class': 'sc-huKLiJ bfuCPC'}).get_text()
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'title'] = title
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'price'] = price
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'location'] = location
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'like'] = like
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'Attention'] = attention
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'time'] = time
                    data_bunjang.loc[str(page_num) + "_" + str(i), 'content'] = content
                    brower.back()
            if time == date:
                break
            page_num += 1
        if time == date:
            break
    return data_bunjang


if __name__ == "__main__":
    product = input("검색할 제품 입력: ")
    date = input("수집 범위: ")
    data = Crawling(product, date)
    data.to_csv("bunjang.csv", mode='w')
