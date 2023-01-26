from mitmproxy.tools.main import *
import warnings

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    '''
    -p 8889 监听8889端口
    --mode socks5 代理模式
    -q 安静模式 不输出mitmproxy的日志
    '''
    port = 8889
    print(f"[+] 启动mitmproxy 127.0.0.1:{port}")
    mitmdump(args=['-p',f'{port}', '--mode','socks5', '-s', 'addons.py', '-q'])

