# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fcition.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(758, 690)
        Form.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_4 = QtWidgets.QGroupBox(Form)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 50))
        self.lineEdit.setStyleSheet("font: 14pt \"黑体\";")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_5.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton.setStyleSheet("font: 14pt \"黑体\";")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.gridLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 200))
        self.textBrowser.setObjectName("textBrowser")
        self.horizontalLayout_3.addWidget(self.textBrowser)
        self.gridLayout.addWidget(self.groupBox_2, 2, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.groupBox_3)
        self.tableWidget_2.setMinimumSize(QtCore.QSize(0, 200))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(4)
        self.tableWidget_2.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, item)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(False)
        self.tableWidget_2.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_4.addWidget(self.tableWidget_2)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 2)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar_5 = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar_5.setProperty("value", 0)
        self.progressBar_5.setObjectName("progressBar_5")
        self.horizontalLayout.addWidget(self.progressBar_5)
        self.progressBar_4 = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar_4.setProperty("value", 0)
        self.progressBar_4.setObjectName("progressBar_4")
        self.horizontalLayout.addWidget(self.progressBar_4)
        self.progressBar_3 = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar_3.setProperty("value", 0)
        self.progressBar_3.setObjectName("progressBar_3")
        self.horizontalLayout.addWidget(self.progressBar_3)
        self.progressBar_2 = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar_2.setProperty("value", 0)
        self.progressBar_2.setObjectName("progressBar_2")
        self.horizontalLayout.addWidget(self.progressBar_2)
        self.progressBar = QtWidgets.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 2)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.search_book)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lineEdit.setPlaceholderText(_translate("Form", "请输入书名或作者"))
        self.pushButton.setText(_translate("Form", "搜索"))
        self.groupBox_2.setTitle(_translate("Form", "下载详情信息"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">--&gt;下载进度 10%</p></body></html>"))
        self.groupBox_3.setTitle(_translate("Form", "书籍列表"))
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "书名"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "作者"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("Form", "字数"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("Form", "操作"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("Form", "各线程下载进度"))
import resource_rc
