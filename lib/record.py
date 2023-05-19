import os
import threading
from .pathutil import path_join

# 创建共享锁和排他锁对象
shared_lock = threading.RLock()
exclusive_lock = threading.Lock()

def record(api, is_vul: bool) -> None:
    # 首先判断vul.txt和normal.txt文件是否存在，不存在则创建
    if not os.path.exists(path_join('logs/vul.txt')):
        with open(path_join('logs/vul.txt'), 'w') as f:
            f.write('')
    if not os.path.exists(path_join('logs/normal.txt')):
        with open(path_join('logs/normal.txt'), 'w') as f:
            f.write('')

    # 获取共享锁
    shared_lock.acquire()
    try:
        # 读取文件内容
        if is_vul:
            with open(path_join('logs/vul.txt'), 'r') as f:
                content = f.read()
        else:
            with open(path_join('logs/normal.txt'), 'r') as f:
                content = f.read()

        # 判断内容是否已存在
        if api + '\n' in content:
            return

        # 获取排他锁
        exclusive_lock.acquire()
        try:
            if is_vul:
                with open(path_join('logs/vul.txt'), 'a') as f:
                    f.write(api + '\n')
            else:
                with open(path_join('logs/normal.txt'), 'a') as f:
                    f.write(api + '\n')
        finally:
            # 释放排他锁
            exclusive_lock.release()
    finally:
        # 释放共享锁
        shared_lock.release()