# -*- coding: utf-8 -*-
# @Author  : chengyijun
# @Time    : 2020/9/18 8:07
# @File    : test.py
# @desc:
import re
import typing

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog

def get_safe_file_name(file_name):
    return re.sub(r'[<,>,/,\\,|,:,",\',.,*,?]', '-', file_name)



def main():
    res = get_safe_file_name("\我是文件名")
    print(res)


if __name__ == '__main__':
    main()
