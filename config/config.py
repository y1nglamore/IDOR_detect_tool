import sys 
import os 
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
            'cookie' : '',
            'mrs' : []
        } 
        with open(path_join('config/config.yml'), 'r') as f:
            config = yaml.load(f, Loader=yaml.SafeLoader)
        for h in config['host']:
            self.config['host'].append(h )
        self.config['cookie'] = config['cookie'] 
        for m in config['matchreplace']:
            self.config['mrs'].append(m)

    def get_config(self) -> dict:
        if self.config is None:
            self.__parse_config()
        return self.config
    

