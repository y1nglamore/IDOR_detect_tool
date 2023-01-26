from mitmproxy.tools.main import *
import warnings

warnings.filterwarnings("ignore")

if __name__ == '__main__':
    '''
    -p 8889 监听8889端口
    --mode regular 代理模式，regular表示HTTP代理，可以廁socks5等其他模式
    -q 安静模式 不输出mitmproxy的日志
    '''
    port = 8889
    print(f"[+] 启动HTTP代理http://127.0.0.1:{port}成功 请连接代理并访问mitm.it进行证书安装，以便进行HTTPS流量的抓取")
    mitmdump(args=['-p',f'{port}', '--mode','regular', '-s', 'addons.py', '-q'])


