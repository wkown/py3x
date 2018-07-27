# 打开ie
import win32com.client
from time import sleep

ie = win32com.client.DispatchEx("InternetExplorer.Application")
ie.Navigate('https://baidu.com')
ie.Visible = 1
while ie.Busy:
    sleep(1)

doc = ie.Document
print(doc)
body = doc.body
print(body)
#kw = doc.getElementById('kw')
# print(kw)

for i in body.getElementsByTagName("input"):
    if i.id == 'kw':
        i.value = 'python 入门教程'

for i in body.getElementsByTagName("input"):
    if i.id == 'su':
        i.click()
        print('click')