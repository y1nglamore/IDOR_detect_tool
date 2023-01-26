import os 

def base_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def config_dir():
    return os.path.join(base_dir(), 'config')

def path_join(path):
    return os.path.join(base_dir(), path)