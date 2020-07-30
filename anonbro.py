import requests
from bs4 import BeautifulSoup
import random


def anon_browser(url):
    global html_page
    s = requests.session()
    req = s.get('http://spys.me/proxy.txt')
    proxy_page = BeautifulSoup(req.text, 'html.parser')
    a = str(proxy_page)
    x = a.splitlines()
    random_server = random.randrange(10, 70)
    proxy_server = (x[random_server].split()[0])
    proxy = {'https': '{}'.format(proxy_server)}
    print('[-] Trying to connect to: ' + str(proxy).split()[-1].strip('}').strip("'"))

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/80.0.3987.163 Safari/537.36 '
    headers = {'User-Agent': user_agent}

    try:
        req_proxy = s.get(url, proxies=proxy, headers=headers)
        s.close()
        print('[+] Connected to: ' + str(proxy).split()[-1].strip('}').strip("'"))
        print(req_proxy.status_code)
        html_page = req_proxy

    except requests.exceptions.ProxyError:
        print('[!] Something Wrong trying again...\n')
        anon_browser(url)
    return html_page

