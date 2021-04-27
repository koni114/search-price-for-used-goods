import common
from crawlingdata import BunjangCrawlingData

if __name__ == "__main__":

    import os
    current_dir = os.getcwd()
    print("current_dir : ", current_dir)
    config_info = common.get_yaml_file(file_path=current_dir, file_name="config.yaml", yaml_type="d")
    logging_info = common.get_yaml_file(file_path=current_dir, file_name="logging.yaml", yaml_type="d")

    # config setting
    crl_user_agent = config_info["crl_user_agent"]
    crl_chrome_path = config_info["crl_chrome_path"]

    # 번개 장터 크롤링
    bunjang_root_url = config_info["crl_bunjang_root_url"]

    product = ['애플워치']

    for page_num in range(2, 11):
        print("## page_num", page_num)
        if not page_num == 1:
            bunjang_root_url = bunjang_root_url + "/search/products?q=" + product[0] + "&&order=score&page=" + str(page_num)

        bunjang_search_window_xpath = config_info['bunjang']['search_window_xpath']
        bunjang_search_window_xpath_icon_xpath = config_info['bunjang']['search_window_xpath_icon_xpath']


        # logger setting
        bunjang_logger = common.set_logger(log_file_path='/Users/heojaehun/gitRepo/search-price-for-used-goods/log',
                                           log_file_name='bunjang.log',
                                           level='DEBUG')

        try:
            bunjang = BunjangCrawlingData(user_agent=crl_user_agent,
                                          chrome_path=crl_chrome_path,
                                          root_url=bunjang_root_url,
                                          search_window_xpath=bunjang_search_window_xpath,
                                          search_window_xpath_icon_xpath=bunjang_search_window_xpath_icon_xpath,
                                          page_num=page_num,
                                          logger=bunjang_logger
                                          )
        except Exception as e:
            bunjang_logger.error(e)

        browser = bunjang.set_crawling_option()
        bunjang.set_crawling_main_page(browser, product)
        crawling_data = bunjang.get_crawling_data(product=product, browser=browser)
        crawling_data.to_csv('./data/' + str(page_num) + "_" + product[0] + "_" + "bunjang.csv", mode='w')
