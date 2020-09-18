# -*- coding: utf-8 -*-
# @Author  : chengyijun
# @Time    : 2020/9/18 8:07
# @File    : test.py
# @desc:
import typing

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog


class Demo(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        directory = QFileDialog.getExistingDirectory()
        print(directory)


def main():
    import sys
    app = QApplication(sys.argv)
    window = Demo()
    window.setWindowTitle("选择路径")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
