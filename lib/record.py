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

# 在修改后的代码中，我们使用了共享锁（shared_lock）和排他锁（exclusive_lock）来控制对文件的读写操作。获取共享锁后，多个线程可以同时读取文件。而在执行写入操作之前，线程会获取排他锁以保证只有一个线程可以执行写入操作，以避免写入冲突。写入操作完成后，释放排他锁和共享锁，使其他线程能够获取锁并执行读取或写入操作。

# 这样的设计可以允许多个线程同时读取文件，但只允许一个线程执行写入操作，以保证线程安全性。