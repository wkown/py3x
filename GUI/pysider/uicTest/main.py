#!/usr/bin/python3
# -*- coding:utf-8 -*-
#使用pyside2-uic 转换 pyside2-uic mainWindow.ui >  ui_mainWindow.py
#
import sys
from PySide2.QtWidgets import QApplication, QMainWindow,QPushButton
from PySide2.QtCore import QFile,QRect
# 将得到的ui_mainWindow.py导入
from GUI.pysider.uicTest.ui_mainWindow import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #添加自定义的控件
        self.pushButton1 = QPushButton()
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton1.setText("pushButton1")
        self.ui.verticalLayout.addWidget(self.pushButton1)

        # 修改控件时间
        self.ui.pushButton.clicked.connect(func)
        self.pushButton1.clicked.connect(self.pushButton1OnClick)


    def pushButton1OnClick(self):
        self.ui.lineEdit.setText("hello 啥？")


def func():
    print('hello world')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())