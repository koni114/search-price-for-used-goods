from pymongo import MongoClient
import common
import os
import re
import pandas as pd
from gridfs import GridFS

if __name__ == "__main__":

    current_dir = os.getcwd()
    print("current_dir : ", current_dir)
    config_info = common.get_yaml_file(file_path=current_dir, file_name="config.yaml", yaml_type="d")
    logging_info = common.get_yaml_file(file_path=current_dir, file_name="logging.yaml", yaml_type="d")

    # logger setting
    insert_data_logger = common.set_logger(log_file_path=logging_info['bunjang_crawling']['log_file_path'],
                                           log_file_name=logging_info['bunjang_crawling']['log_file_name'],
                                           level=logging_info['bunjang_crawling']['log_level'])

    mongodb_URI = config_info['mongodb_uri']
    mongodb_db = config_info['mongodb_db']
    try:
        client = MongoClient(mongodb_URI)
    except Exception as e:
        insert_data_logger.error("MongoClient connection error!")
        insert_data_logger.error(e)

    db = client[mongodb_db]

    #- bunjang data
    bunjang_data_path = os.path.join(current_dir, 'data')

    #- get file list
    if not os.path.isdir(bunjang_data_path):
        insert_data_logger.error("there is not directory ! : directory path -->" + bunjang_data_path)
    else:
        file_list = os.listdir(bunjang_data_path)

        collection_name = 'bunjang'
        bunjang_csvfile_list = [bool for bool in file_list if collection_name in bool]
        for filename in bunjang_csvfile_list:
            data = pd.read_csv(os.path.join(bunjang_data_path, filename))
            data = data.drop('Unnamed: 0', axis=1)
            try:
                db.bunjang.insert_many(data.to_dict('records'))
            except Exception as e:
                insert_data_logger.error("MongoClient insert_many error!")
                insert_data_logger.error(e)











