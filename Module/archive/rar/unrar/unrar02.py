import rarfile
# 压缩文件rar/test.rar的密码为4位数字密码。暴力破解。
# 实际密码为2563
fp = rarfile.RarFile("rar/test.rar")
print('run')

for i in range(0, 10000):
    password = "%04d" % i
    try:
        fp.extractall('rar', pwd=password)
        print('success:{}'.format(password))
        break
    except:
        print("wrong:{}".format(password))
print('complete')
