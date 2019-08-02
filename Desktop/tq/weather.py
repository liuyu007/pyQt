from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
import widget
import sys

class MyWeather(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.mywidget = widget.Ui_Widget()
        self.mywidget.setupUi(self)
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.replyFinished)
        self.mywidget.pushButton.clicked.connect(self.request)

    def replyFinished(self, reply):
        str1 = reply.readAll()
        str2 = bytes.decode(str1.data(),encoding='utf8')
        self.mywidget.textBrowser.setText(str2)
        err = QJsonParseError()
        json_recev = QJsonDocument.fromJson(str1,err)
        if not json_recev.isNull():
            myobject = json_recev.object()
            if 'data' in myobject:
                myvalue = myobject['data']
                if myvalue.isObject():
                    myobject_data = myvalue.toObject()
                    if 'forecast' in myobject_data:
                        value = myobject_data['forecast']
                        if value.isArray():
                            value1 = value.toArray()[0].toObject()
                            self.tianqi = value1['type'].toString()
                            self.mywidget.lineEdit_2.setText(self.tianqi)
                            low = value1['low'].toString()
                            high = value1['high'].toString()
                            self.wendu = low[2:] + '-' + high[2:]
                            self.mywidget.lineEdit_3.setText(self.wendu)
                            fengxiang = value1['fengxiang'].toString()
                            fengli = value1['fengli'].toString()
                            self.fengli = fengxiang + fengli[9:-3]
                            self.mywidget.lineEdit_4.setText(self.fengli)



        reply.deleteLater()

    def request(self):
        city = self.mywidget.lineEdit.text() #str
        pre = 'http://wthrcdn.etouch.cn/weather_mini?city='
        res = pre + city
        print(res)
        url = QUrl(res)
        self.manager.get(QNetworkRequest(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather = MyWeather()
    weather.show()
    sys.exit(app.exec_())