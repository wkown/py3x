# -*- coding:utf-8 -*-
import re
import os
import requests
import time

class Spider:
    url=''
    timeout=30
    session=''
    target_root_dir = 'html'
    pattern = {
        'js': re.compile(r'<script.*?src=[\'\"](.*?)[\'\"].*?</script>', re.IGNORECASE),
        'css': re.compile(r'<link.*?href=[\'\"](.*?)[\'\"].*?>', re.IGNORECASE),
        'page_image': re.compile(r'<img.*?src=[\'\"](.*?)[\'\"].*?>', re.IGNORECASE),
        'css_image': re.compile(r'url\([\'\"]?(.*?)[\'\"]?\)', re.IGNORECASE),
    }
    dirs = {'js': 'js',
            'css': 'css',
            'page_image': 'images_page',
            'css_image': 'images',
            'font': 'fonts',
            'inner_css': '../images',
            'inner_font': '../fonts',
            'inner_import_css': '.',
            }
    font_ext = ('.ttf', '.eot', '.svg', '.woff', '.woff2')
    inner_files = {'css': {'pattern': re.compile('url\([\'\"]?(.*?)[\'\"]?\)', re.IGNORECASE), 'dir': '../images'}}
    on_save_basename = True

    def __init__(self,url):
        self.url=url
        self.session=requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }

    def getCodeStr(self, result, target_charset='utf-8'):
        # gb2312
        try:
            myResult = result.decode('gb2312').encode(target_charset, 'ignore')
            return myResult
        except:
            pass
            # utf-8
        try:
            myResult = result.decode('utf-8').encode(target_charset, 'ignore')
            return myResult
        except:
            pass

        # unicode
        try:
            myResult = result.encode(target_charset, 'ignore')
            return myResult
        except:
            pass
            # gbk
        try:
            myResult = result.decode('gbk').encode(target_charset, 'ignore')
            return myResult
        except:
            pass
            # big5
        try:
            myResult = result.decode('big5').encode(target_charset, 'ignore')
            return myResult
        except:
            pass

    def file_put_contents(self, filename, content, mode='wb'):
        """
        write something to a file
        :param filename:
        :param content:
        :return:
        """
        if content is None:
            return
        try:
            f = open(self.getCodeStr(filename), mode)
            f.write(content)
            f.close()
        except IOError as e:
            print(e)

    def file_get_contents(self, url):
        """
        read the file content
        :param url:
        :return:
        """
        if url.find('http://') != -1 or url.find('https://') != -1:
            try:
                req = self.session.get(url)
                return req.content
            except Exception as e:
                msg = u'下载文件 %s 时报出错误: %s' % (url, e)
                print("file %s download error: %s" % (url, e))
                self.log(msg)
                return None

        if not os.path.isfile(url):
            url = self.target_root_dir + '/' + url
        if not os.path.isfile(url):
            return
        f = open(url, 'rb')
        content = f.read()
        f.close()
        return content

    def log(self, msg, log_file='download'):
        if msg is None:
            return
        #if isinstance(msg, unicode):
        #    msg = msg.encode('utf-8', 'ignore')

        return self.file_put_contents(self.target_root_dir + '/' + '%s.log' % log_file,
                                 "[%s] %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg), 'ab')
    def run(self):
        print(self.file_get_contents(self.url))

def main():
    sp1 = Spider('http://www.baidu.com')
    sp1.run()


if __name__ == "__main__":
    main()