import contextlib
import json
import traceback
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import mitmproxy.http as http
from mitmproxy import ctx
from mitmproxy import exceptions
from bs4 import BeautifulSoup

from config.config import Config
from lib.requestutil import hack_request, get_raw
from lib.record import record
from lib.requestutil import get_api
from .dor import Dor
from .output import Output

class Replay:
    def __init__(self, source_flow: http.HTTPFlow) -> None:
        self.source_flow = source_flow
        self.pretty_host = self.source_flow.request.pretty_host
        self.modify_flow = source_flow.copy()
        self.api = get_api(self.source_flow)

        # 过滤html接口
        source_resp = source_flow.response.text
        if self.__is_resp_html(source_resp):
            return
        
        # 判断接口是否为json格式
        if not self.__is_resp_json(source_flow.response):
            return
        
        print(f"[*] 开始检测接口: {self.api}")
        
        self.__modify_flow()
        modify_resp = self.replay(self.modify_flow)

        if Dor(source_resp, modify_resp, source_flow).detect_vuln():
            print(f"[+] 发现漏洞 {self.api}")
            record(self.api, True)
            Output(self.api, self.source_flow, self.modify_flow, source_resp, modify_resp, self.pretty_host).output()
        else:
            record(self.api, False)

    def __is_resp_html(self, resp):
        # 检验是否为html响应
        return bool(BeautifulSoup(resp, "html.parser").find())
    
    def __is_resp_json(self, response: http.Response):
        # 检验是否为json响应
        if content_type := response.headers.get('Content-Type', ''):
            return content_type.startswith('application/') and 'json' in content_type
        try:
            json.loads(response.text)
            return True
        except Exception:
            return False



    def __parse_cookie(self, cookie: str) -> dict:
        cookie_dict = {}
        for c in cookie.split(';'):
            with contextlib.suppress(Exception):
                k, v = tuple(c.split('=', 1))
                cookie_dict[k] = v
        return cookie_dict
    
    def __modify_cookie(self, flow: http.HTTPFlow, new_cookie) -> None:
        # Modify the cookie here.
        flow.request.cookies.clear()

        for k, v in self.__parse_cookie(new_cookie).items():
            flow.request.cookies[k] = v

    def __replace(self, pattern, replace, origin):
        # 替换，若pattern为正则则正则替换，否则为字符串替换
        try:
            ptn = re.compile(pattern)
            return re.sub(ptn, replace, origin)
        except Exception:
            return origin.replace(pattern, replace)
        
    def __modify_flow(self) -> None:
        # Modify the flow here.
        config = Config().get_config()
        self.__modify_cookie(self.modify_flow, config['cookie'])
        self.__match_replace(self.modify_flow, config['mrs'])
    
    def __match_replace(self, flow: http.HTTPFlow, mrs: list) -> None:
        # Match and replace here.
        for mr in mrs:
            if mr['location'] == 'URL':
                flow.request.url = self.__replace(mr['pattern'], mr['replace'], flow.request.url)
            elif mr['location'] == 'PATH':
                flow.request.path = self.__replace(mr['pattern'], mr['replace'], flow.request.path)
            elif mr['location'] == 'BODY':
                flow.request.content = self.__replace(mr['pattern'], mr['replace'], flow.request.content)
            elif mr['location'] == 'HEADER':
                header_name = mr['replace']['name']
                header_value = mr['replace']['value']
                if header_name in flow.request.headers:
                    flow.request.headers[header_name] = self.__replace( mr['pattern'], header_value, flow.request.headers[header_name])
                else:
                    flow.request.headers[header_name] = header_value
            else:
                raise exceptions.OptionsError(f"Invalid location: {mr['location']}")
                
    @staticmethod
    def replay(*args) -> str:
        if len(args) == 1:
            flow = args[0]
            pretty_host = flow.request.pretty_host
        elif len(args) > 1:
            self = args[0]
            flow = args[1]
            pretty_host = self.pretty_host

        raw = get_raw(flow, pretty_host = pretty_host)
        try:
            return hack_request(raw, url=flow.request.url)
        except Exception as e:
            print(f"hack_request error: {e}")
            traceback.print_exc()
            return None 
