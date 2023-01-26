import os
from .pathutil import path_join

def record(api, is_vul: bool) -> None:
    # 首先判断vul.txt和normal.txt文件是否存在，不存在则创建
    if not os.path.exists(path_join('logs/vul.txt')):
        with open(path_join('logs/vul.txt'), 'w') as f:
            f.write('')
    if not os.path.exists(path_join('logs/normal.txt')):
        with open(path_join('logs/normal.txt'), 'w') as f:
            f.write('')

    if is_vul:
        if api not in open(path_join('logs/vul.txt'), 'r').read():
            with open(path_join('logs/vul.txt'), 'a') as f:
                f.write(api + '\n')
    elif api not in open(path_join('logs/normal.txt'), 'r').read():
        with open(path_join('logs/normal.txt'), 'a') as f:
            f.write(api + '\n')

