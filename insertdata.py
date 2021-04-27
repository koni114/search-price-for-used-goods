from pymongo import MongoClient
import common
import os
import re
import pandas as pd
import datetime
import pprint

if __name__ == "__main__":

    current_dir = os.getcwd()
    print("current_dir : ", current_dir)
    config_info = common.get_yaml_file(file_path=current_dir, file_name="config.yaml", yaml_type="d")

    # logger setting
    insert_data_logger = common.set_logger(log_file_path='/Users/heojaehun/gitRepo/search-price-for-used-goods/log',
                                       log_file_name='insertdata.log',
                                       level='DEBUG')

    mongodb_URI = config_info['mongodb_uri']
    mongodb_db = config_info['mongodb_db']
    client = MongoClient(mongodb_URI)

    db = client[mongodb_db]

    #- bunjang data
    bunjang_data_path = os.path.join(current_dir, 'data')

    #- get file list
    if not os.path.isdir(bunjang_data_path):
        insert_data_logger("there is not directory ! : directory path -->" + bunjang_data_path)
    else:
        file_list = os.listdir(bunjang_data_path)

        collection_name = 'bunjang'
        bunjang_csvfile_list = [bool for bool in file_list if collection_name in bool]
        filename = bunjang_csvfile_list[0]
        for filename in bunjang_csvfile_list:
            data = pd.read_csv(os.path.join(bunjang_data_path, filename))
            data.to_dict('records')









