# -*- coding: utf-8 -*-
# @Author  : chengyijun
# @Time    : 2020/9/18 8:07
# @File    : test.py
# @desc:
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow


class Demo(QMainWindow):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent=parent)

        # 设置窗体无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


def main():
    import sys
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
