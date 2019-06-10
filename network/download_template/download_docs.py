# -*- coding:utf-8 -*-
__author__ = 'walkskyer'
"""
下载整站静态页晚间处理还有待优化20180206
"""

import urllib
import re
import os
from network.download_template.DownloadWebPage import Spider

if __name__ == "__main__":
    raw_url = input('input a url : ').strip()
    if not raw_url:
        exit(0)

    spider = Spider(raw_url)

    content = spider.file_get_contents(raw_url)
    spider.url = raw_url
    spider.base_url = os.path.dirname(raw_url)
    spider.base_name = 'index.html'
    spider.run()

    matches = re.findall('<a.*?href="(.*?)".*?>', content, re.DOTALL)

    baseUrl = os.path.dirname(raw_url)
    baseDir = spider.target_root_dir
    for match in matches:
        print(match)
        if not match.endswith('.html') or match == 'index.html':
            continue

        dir = os.path.dirname(match)
        file_url = baseUrl + '/' + match
        spider.target_root_dir = baseDir + '/' + dir
        spider.url = file_url
        spider.base_url = os.path.dirname(file_url)
        spider.base_name = os.path.basename(file_url)
        spider.run()
