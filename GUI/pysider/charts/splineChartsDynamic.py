import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCharts import QtCharts
import threading
import random
import time


class RealTimeCurveQChartWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, f=None, *args, **kwargs):
        QtWidgets.QWidget.__init__(self)
        self.maxSize = 31  # 只存储最新的31个数据
        self.maxX = 300
        self.maxY = 100
        self.data = []

        #折线
        self.splineSeries = QtCharts.QSplineSeries()
        #离散点
        self.scatterSeries = QtCharts.QScatterSeries()
        self.scatterSeries.setMarkerSize(8)

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.splineSeries)
        self.chart.addSeries(self.scatterSeries)
        self.chart.legend().hide()
        self.chart.setTitle("实时动态曲线")
        self.chart.createDefaultAxes()
        self.chart.axisX().setRange(0, self.maxX)
        self.chart.axisY().setRange(0, self.maxY)

        self.chartView = QtCharts.QChartView(self.chart)
        #self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chartView)
        self.setLayout(layout)
        self.thread=None

    def dataRecieved(self, value):
        self.data.append(value)

        # 数据个数超过了最大数量，则删除最先接收到的数据，实现曲线向前移动
        while len(self.data) > self.maxSize:
            del (self.data[0])

        # 界面被隐藏后就没有必要绘制数据的曲线了
        if self.isVisible():
            self.splineSeries.clear()
            self.scatterSeries.clear()
            dx = self.maxX / (self.maxSize - 1)
            less = self.maxSize - len(self.data)

            i = 0
            while i < len(self.data):
                self.splineSeries.append(less * dx + i * dx, self.data[i])
                self.scatterSeries.append(less * dx + i * dx, self.data[i])
                i += 1

    def closeEvent(self, event:QtGui.QCloseEvent):
        if self.thread is not None:
            self.thread.stopFlag = True
            self.thread.join()
        return QtWidgets.QWidget.closeEvent(self,event)


class MyTread(threading.Thread):
    def __init__(self,widget):
        threading.Thread.__init__(self)
        self.widget=widget
        self.stopFlag=False
    def run(self):
        while not self.stopFlag:
            self.widget.dataRecieved(random.randint(10, 100))
            #经过测试0.003是极限
            time.sleep(0.003)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    w = RealTimeCurveQChartWidget()
    w.resize(700, 400)
    w.show()
    thread = MyTread(w)
    w.thread = thread
    thread.start()

    sys.exit(app.exec_())