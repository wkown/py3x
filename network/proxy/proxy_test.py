#!/usr/bin/python3
# -*- coding:utf-8 -*-
# 验证代理是否有效
import requests
import telnetlib


def test1(ip,port):
    proxy = "http://%s:%s" % (ip, port)
    try:
        resp = requests.get('https://www.baidu.com/', proxies={"http": proxy, "https": proxy}, timeout=20)
    except:
        return False
    else:
        return resp.status_code == 200


def test2(ip,port):
    try:
        telnetlib.Telnet(ip, port, timeout=20)
    except:
        return False
    else:
        return True
if __name__ == "__main__":
    print("proxy status: %s" % test1("127.0.0.1", "8888"))
    print("proxy status: %s" % test2("127.0.0.1", "8888"))
    print("proxy status: %s" % test1("127.0.0.1", "18888"))
    print("proxy status: %s" % test2("127.0.0.1", "18888"))
