import threading

def my_thread(func, *args, **kwargs):

    t = threading.Thread(target=func, args=args, kwargs=kwargs)

    t.start()

    return t