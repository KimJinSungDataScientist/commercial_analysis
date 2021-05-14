# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'start.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title_text = QtWidgets.QLabel(self.centralwidget)
        self.title_text.setGeometry(QtCore.QRect(100, 100, 691, 61))
        font = QtGui.QFont()
        font.setFamily("한컴 고딕")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title_text.setFont(font)
        self.title_text.setObjectName("title_text")
        self.search_text = QtWidgets.QLabel(self.centralwidget)
        self.search_text.setGeometry(QtCore.QRect(180, 250, 351, 21))
        self.search_text.setObjectName("search_text")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(540, 270, 181, 21))
        self.search_button.setObjectName("search_button")
        self.search_input = QtWidgets.QTextEdit(self.centralwidget)
        self.search_input.setGeometry(QtCore.QRect(160, 270, 371, 21))
        self.search_input.setObjectName("search_input")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_text.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'한컴 고딕\'; font-size:14pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Gulim\'; font-size:16pt; color:#55aaff;\">서울특별시 AI 상권분석 프로그램</span></p></body></html>"))
        self.search_text.setText(_translate("MainWindow", "원하시는 지역명과 상권을 입력하세요"))
        self.search_button.setText(_translate("MainWindow", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
