import yaml
import pandas as pd
import os
# file_path = os.getcwd()
# file_name = "config.yaml"
# yaml_type = "d"


def get_yaml_file(file_path=".", file_name="config.yaml", yaml_type="s"):
    """get yaml file variable to dict
    Args:
        file_path
        file_name
        yaml_type : s, d
    Returns
        dict type object
    Example:
        >>>
    """
    import yaml

    full_path = os.path.join(file_path, file_name)

    if not os.path.isfile(full_path):
        print("해당 경로에 해당 파일이 없습니다 : ", full_path)
    else:
        try:
            if yaml_type == 's':
                with open(full_path) as file:
                    conf_dict = yaml.load(file, Loader=yaml.FullLoader)

            else:
                with open(full_path) as file:
                    conf_dict = yaml.full_load(file)

        except Exception as e:
            print("getYAMLFIle : file open error! file_full_path : ", full_path)
            print(e)
            conf_dict = e

        return conf_dict


def set_logger(log_file_path='./log', log_file_name='test.log', level='ERROR'):
    import logging.handlers
    import os

    log_level = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level not in log_level:
        print("log_level error! : please select one of the following : [NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL]")

    # if not log file directory, make the dir
    if not os.path.isdir(log_file_path):
        print("해당 위치에 디렉토리를 생성합니다.", log_file_path)
        os.mkdir(log_file_path)

    log = logging.getLogger(log_file_name.split(".")[0])
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s;%(lineno)s] >> %(message)s')
    file_max_byte = 1024 * 1024 * 10
    file_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(log_file_path, log_file_name),
                                                        maxBytes=file_max_byte,
                                                        backupCount=5)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    log.setLevel(level=level)

    return log
