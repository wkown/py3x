# -*- coding:utf-8 -*-
import re
import os,sys
import requests
import time
from urllib.parse import urlparse
is_python3 = sys.version_info.major == 3
if is_python3:
    unicode = str

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
            self.print(e)

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
                self.print("file %s download error: %s" % (url, e))
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

    def get_target_name(self, url, origin_name=True):
        """
        获取要保存的文件名
        :param url:
        :param origin_name:
        :return:
        """
        filename = os.path.basename(url.strip())

        pos = filename.find('?')
        if pos != -1:
            filename = filename[0: pos]

        if filename and not origin_name:
            path = os.path.dirname(url.strip()).replace('http://', '').replace('https://', '').replace('//', '').replace('..', '')
            filename = '%s-%s' % (path.replace('/', '-'), filename)
        return filename

    def real_url(self, uri, base_url=''):
        """
        返回真实的url
        :param uri:
        :param base_url:
        :return:
        """
        try:
            if uri.find('http://') == 0 or uri.find('https://') == 0:
                return uri
            if uri.startswith('//'):
                return 'http:%s' % uri

            url_info = urlparse(base_url)
            root_path = '%s://%s' % (url_info.scheme, url_info.netloc)

            if uri == '.' or not uri:
                uri = base_url
            elif uri[0] == '/':
                uri = root_path + uri
            else:
                uri = base_url + '/' + uri
            return uri
        except Exception as e:
            # charset error try again
            self.print(e)
            if not isinstance(uri, unicode):
                return self.real_url(self.getCodeStr(uri, 'utf-8').decode('utf-8'), base_url)

        try:
            if uri == '.' or not uri:
                uri = base_url
            elif uri[0] == '/':
                uri = root_path + uri
            else:
                uri = base_url + '/' + uri
        except Exception as e:
            self.log(e)
            return self.real_url(self.getCodeStr(uri, 'utf-8').decode('utf-8'), base_url)
        return uri

    @staticmethod
    def print(*args, sep=' ', end='\n', file=None):
        print(*args, sep=sep, end=end, file=file)

    def run(self):
        self.print(self.file_get_contents(self.url))


def main():
    sp1 = Spider('http://www.baidu.com')
    sp1.run()


if __name__ == "__main__":
    main()
