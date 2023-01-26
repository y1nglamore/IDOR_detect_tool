import mitmproxy.http as http
from config.config import Config
import re
from urllib.parse import urlparse
from core.replay import Replay
from lib.thread import my_thread
from lib.pathutil import path_join
from lib.requestutil import get_api

class Listener:
    def __init__(self) -> None:
        self.config = Config().get_config()

    def __is_static(self, flow: http.HTTPFlow) -> bool:
        # 判断是否在请求静态资源
        path = urlparse(flow.request.url).path
        static_ext = ['.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot', '.map', '.ico', '.webp', 'htm', 'html']
        return any(path.endswith(ext) for ext in static_ext)
    
    def __is_vul_exists(self, flow: http.HTTPFlow) -> bool:
        # 判断漏洞是否已存在
        # return False  # for test only
        content = open(path_join('logs/vul.txt'), 'r').read()
        return get_api(flow) in content

    def request(self, flow: http.HTTPFlow) -> None:
        for host_pattern in self.config['host']:
            if re.search(host_pattern, flow.request.pretty_host) and not self.__is_static(flow) and not self.__is_vul_exists(flow):
                my_thread(Replay, flow)
                break

addons = [
    Listener()
]
