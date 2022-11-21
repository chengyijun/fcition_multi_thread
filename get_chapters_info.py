# -*- coding:utf-8 -*-
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup

from utils import get_safe_file_name, get_random_useragent


class Chapters(QThread):
    chapters_got = pyqtSignal([list])

    def __init__(self, parent=None, bname=None, blink=None):
        super().__init__(parent)
        self.bname = get_safe_file_name(bname)
        self.blink = blink
        self.datas = []

    def task(self):
        heardes = {
            'User-Agent': get_random_useragent()
        }

        res = requests.get(url=self.blink, headers=heardes)
        # res.encoding = 'gbk'

        bs = BeautifulSoup(res.text, "lxml")
        cs = bs.select("div.list>ul>li>a")

        for index, chapter in enumerate(cs, start=1):
            title = chapter.get("title")
            href = chapter.get("href")

            data = {
                'total': len(cs),
                'index': index,
                'title': title,
                'href': href
            }
            self.datas.append(data)
        self.chapters_got[list].emit(self.datas)

    def run(self):
        self.task()


def main():
    import sys
    app = QApplication(sys.argv)

    chapters = Chapters(blink='https://www.biquge7.top/37360', bname='鬼吹灯')
    chapters.chapters_got.connect(lambda x: print(x))
    chapters.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
