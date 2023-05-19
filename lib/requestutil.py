import mitmproxy.http as http 
import html
from mitmproxy.net.http.http1.assemble import assemble_request

def hack_request(raw, url=None):
    import requests_raw
    r = requests_raw.raw(url=url, data=raw.encode(), verify=False)
    # print(r.text)
    return r.text


def get_api(flow: http.HTTPFlow) -> str:
    # 返回请求的path host port
    return f"{flow.request.pretty_host}:{str(flow.request.port)}{flow.request.path.split('?')[0]}"

def get_raw(flow: http.HTTPFlow, pretty_host = None) -> str:
    raw = assemble_request(flow.request).decode('utf-8')
    if pretty_host:
        raw = raw.replace(flow.request.host, pretty_host)
    return raw

def resp_htmlencode(resp: str) -> str:
    return html.escape(resp)


# def hack_request(raw, real_host = None, url=None):
#     import HackRequests
#     hack = HackRequests.hackRequests()
#     hh = hack.httpraw(raw, real_host=real_host) if real_host else hack.httpraw(raw)
#     return hh.text()