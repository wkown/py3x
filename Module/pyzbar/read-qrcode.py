# -*- coding:utf-8 -*-
import zxing

reader = zxing.BarCodeReader()
barcode = reader.decode("qrcode_google.png")
print(barcode.parsed)
