def ip():
    from urllib import request
    ip = request.urlopen('https://gitee.com/vxyi/quantum-ws-ip-address/raw/master/ip')
    print(ip.read().decode('utf-8'))

