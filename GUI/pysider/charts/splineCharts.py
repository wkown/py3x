import sys
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCharts import QtCharts

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    series = QtCharts.QSplineSeries()
    series.setName("spline")
    series.append(0, 6)
    series.append(2, 4)
    series.append(3, 8)
    series.append(7, 4)
    series.append(10, 5)

    series2 = QtCharts.QSplineSeries()
    series2.setName("spline")
    series2.append(0, 7)
    series2.append(2, 5)
    series2.append(3, 9)
    series2.append(7, 5)
    series2.append(10, 6)

    chart = QtCharts.QChart()
    chart.legend().hide()
    chart.addSeries(series)
    chart.addSeries(series2)
    chart.setTitle("Simple spline chart example")
    chart.createDefaultAxes()
    chart.axes(QtCore.Qt.Vertical)[0].setRange(0, 10)
    chartView = QtCharts.QChartView(chart)
    chartView.setRenderHint(QtGui.QPainter.Antialiasing)
    window = QtWidgets.QMainWindow()

    window.setCentralWidget(chartView)
    window.resize(400, 300)
    window.show()

    sys.exit(app.exec_())
