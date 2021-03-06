# -*- coding:utf-8 -*-
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from lxml import etree

from config_url import base_url
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
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)

        chapters_origin = xres.xpath('//div[@class="chapter"]/a/text()')
        true_index = 0
        for co in chapters_origin:
            if '第一章' in co:
                true_index = chapters_origin.index(co)
                break

        chapters = xres.xpath('//div[@class="chapter"]')[true_index:]
        total = len(chapters)

        for index, chapter in enumerate(chapters, start=1):
            title = chapter.xpath('./a/text()')[0]
            href = base_url + chapter.xpath('./a/@href')[0]

            data = {
                'total': total,
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

    chapters = Chapters(blink='https://qxs.la/120367/', bname='盗墓者笔录')
    chapters.chapters_got.connect(lambda x: print(x))
    chapters.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
