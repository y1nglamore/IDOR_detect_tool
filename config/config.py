import sys 
import os
import traceback 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from lib.singleton import Singleton
from lib.pathutil import path_join

@Singleton
class Config(object):
    
    def __init__(self) -> None:
        self.config = None

    def __parse_config(self) -> None:  # sourcery skip: simplify-generator
        config = None
        self.config = {
            'host' : [],
            'port' : [],
            'cookie' : '',
            'mrs' : []
        }
        with open(path_join('config/config.yml'), 'r', encoding="utf-8") as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        try:
            for h in config['host']:
                self.config['host'].append(h)
            for p in config['port']:
                self.config['port'].append(p)
            self.config['cookie'] = config['cookie'] 
            for m in config['matchreplace']:
                self.config['mrs'].append(m)
        except Exception as e:
            print("Error: 配置解析出错，请检查")
            traceback.print_exc()
            exit(0)

    def get_config(self) -> dict:
        if self.config is None:
            self.__parse_config()
        return self.config

    def check_config(self) -> bool :
        if ('host' not in self.config) or ('cookie' not in self.config) or ('mrs' not in self.config):
            print("Error: 配置出错，请检查")
            return False
        if type(self.config['host']) != list or type(self.config['mrs']) != list or type(self.config['cookie']) != str:
            print("Error: 配置出错，请检查")
            return False 
        if self.config['cookie'] == '':
            print("Error: 配置出错，请检查，cookie不能为空")
            return False
        return True
    

