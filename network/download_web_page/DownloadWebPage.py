# -*- coding:utf-8 -*-
import re
import os
import sys
import requests
import time
from urllib.parse import urlparse

is_python3 = sys.version_info.major == 3
if is_python3:
    unicode = str


def getCodeStr(result, target_charset='utf-8'):
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


class Spider:
    url = ''
    base_url = ''
    base_name = 'index.html'

    timeout = 30
    session = ''
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

    def __init__(self, url):
        self.url = url
        self.session = requests.session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept-Encoding': ', '.join(('gzip', 'deflate')),
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }

    def getCodeStr(self, result, target_charset='utf-8'):
        return getCodeStr(result, target_charset)

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
            if isinstance(content, str):
                f.write(content.encode())
            else:
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
                if isinstance(req.content, bytes):
                    try:
                        return req.content.decode('utf-8')
                    except Exception as e:
                        pass
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
        if isinstance(content, bytes):
            return content.decode('utf-8')
        return content

    def replace_resource_path(self, matchObj, target_dir='', origin_name=True):
        """
        替换资源文件目录
        :param matchObj:
        :param target_dir:
        :return:
        """
        match = matchObj.group(1).strip()
        if not match:
            return ''

        if match.startswith('data:image'):
            return matchObj.group(0)

        if self.is_font_file(match):
            if target_dir.startswith('..'):
                target_dir = self.dirs['inner_font']
            else:
                target_dir = self.dirs['font']

        if match.endswith('.css') and target_dir.startswith('..'):
            target_dir = self.dirs['inner_import_css']

        return matchObj.group(0).replace(match, target_dir + '/' + self.get_target_name(match, origin_name))

    def replace_inner_source_file_path(self, matchObj):
        return self.replace_resource_path(matchObj, self.inner_files['css']['dir'], self.on_save_basename)

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
            path = (os.path.dirname(url.strip())
                    .replace('http://', '')
                    .replace('https://', '')
                    .replace('//', '')
                    .replace('..', '')
                    )
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
                uri = self.root_path + uri
            else:
                uri = base_url + '/' + uri
        except Exception as e:
            self.log(e)
            return self.real_url(self.getCodeStr(uri, 'utf-8').decode('utf-8'), base_url)
        return uri

    def download_files(self, file_list, dir, base_url='', origin_name=True):
        """
        下载文件列表
        :param file_list:
        :param dir:
        :param base_url:
        :param origin_name:
        :return:
        """
        if not os.path.isdir(self.target_root_dir + '/' + dir):
            self.print('curr dir: %s and I will make dir： %s\n' % (os.getcwd(), self.target_root_dir + '/' + dir))
            os.mkdir(self.target_root_dir + '/' + dir)

        for v in file_list:
            filename = self.get_target_name(v.strip(), origin_name)
            if filename == '':
                continue

            self.print("%s_filename:%s\n" % (dir, filename))
            if self.is_font_file(filename):
                self.download_file(self.dirs['font'] + '/' + filename, v, base_url)
                continue
            if filename.endswith('.css'):
                self.download_file(self.dirs['css'] + '/' + filename, v, base_url)
                continue
            self.download_file(dir + '/' + filename, v, base_url)

    def download_file(self, filename, target_url, base_url=''):
        """
        下载文件0
        :param filename:
        :param target_url:
        :param base_url:
        :return:
        """

        filename = self.target_root_dir + '/' + filename
        if not os.path.isdir(os.path.dirname(filename)):
            self.print('curr dir: %s and I will make dir： %s\n' % (os.getcwd(), dir))
            os.mkdir(os.path.dirname(filename))

        if os.path.isfile(filename):
            self.print('File: %s is exist.' % filename)
            return

        if target_url.strip().startswith('data:image'):
            self.print('URL seems not a file: %s .' % filename)
            return ''

        target_url = target_url.strip().replace('\'', '').replace('"', '')
        target_url = self.real_url(target_url, base_url)

        if not target_url:
            return

        self.print("download: %s \n" % target_url)
        self.file_put_contents(filename, self.file_get_contents(target_url))

    def is_font_file(self, filename):
        """
        根据文件名判断是否为字体文件
        :param filename:
        :return:
        """
        filename = self.get_target_name(filename.strip().lower())
        last_dot_index = filename.rfind('.')
        if last_dot_index > -1:
            if filename[last_dot_index:] in self.font_ext:
                return True
        return False

    def log(self, msg, log_file='download'):
        if msg is None:
            return
        # if isinstance(msg, unicode):
        #    msg = msg.encode('utf-8', 'ignore')

        return self.file_put_contents(self.target_root_dir + '/' + '%s.log' % log_file,
                                      "[%s] %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), msg), 'ab')

    @staticmethod
    def print(*args, sep=' ', end='\n', file=None):
        print(*args, sep=sep, end=end, file=file)

    def run(self):
        if not os.path.isdir(self.target_root_dir):
            os.mkdir(self.target_root_dir)
        # os.chdir(target_root_dir)

        page_content = self.file_get_contents(self.url)

        content = self.file_get_contents(self.url)
        for k, v in self.pattern.items():
            files1 = v.findall(content)
            self.print(files1)
            if not files1:
                continue

            # link 不一定是css
            if k == 'css':
                filesTemp = []
                for tFilename in files1:
                    if self.get_target_name(tFilename.strip()).endswith('.css'):
                        filesTemp.append(tFilename)
                self.print('Css Files:', filesTemp)
                files1 = filesTemp

            if self.on_save_basename:
                save_basename = not (k == 'page_image')
            else:
                save_basename = self.on_save_basename

            self.download_files(files1, self.dirs[k], self.base_url, save_basename)

            def replace_source_file_path(matchObj):
                """
                替换
                :param matchObj:
                :return:
                """
                return self.replace_resource_path(matchObj, self.dirs[k], save_basename)
                # match = matchObj.group(1)
                # if not match:
                #     return ''
                # if match.strip().startswith('data:image/'):
                #     return matchObj.group(0)
                #
                # return matchObj.group(0).replace(match, dirs[k] + '/' + wk_target_name(match, save_basename))

            # return str_replace(match[1],dirs[k].'/'.wk_basename(match[1]),match[0])
            page_content = v.sub(replace_source_file_path, page_content)

            if k == 'css':  # 如果是css 还要下载css中引用的文件
                for css_file in files1:
                    if not css_file.endswith('.css'):
                        continue
                    self.print('css/' + self.get_target_name(css_file))
                    css_content = self.file_get_contents('css/' + self.get_target_name(css_file, save_basename))
                    if css_content is None:
                        continue
                    css_matches = self.inner_files['css']['pattern'].findall(css_content)
                    if css_matches:
                        self.download_files(css_matches, self.dirs['css_image'],
                                            self.real_url(os.path.dirname(css_file), self.base_url),
                                            save_basename)
                        css_content = self.inner_files['css']['pattern'].sub(self.replace_inner_source_file_path,
                                                                             css_content)
                        self.file_put_contents(
                            self.target_root_dir + '/' + 'css/' + self.get_target_name(css_file, save_basename),
                            css_content)

        self.file_put_contents(self.target_root_dir + '/' + self.base_name, page_content)
        self.print("Download task is complete ^_^")
        self.print(
            "****************************************************************************************************")
        self.print(os.getcwd())
        # os.chdir('..')
        self.print(os.getcwd())


def main():
    sp1 = Spider('http://www.baidu.com')
    sp1.base_name = 'index.html'
    sp1.run()


if __name__ == "__main__":
    main()
