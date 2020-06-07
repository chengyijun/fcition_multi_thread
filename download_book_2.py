import os
import time
from queue import Queue

import requests
from PyQt5.Qt import *

from lxml import etree
from config_url import base_url


class Makedata:
    Q = Queue()

    def __init__(self):
        self.blink = None
        self.bname = None

    def set_bname_and_blink(self, bname, blink):
        self.blink = blink
        self.bname = bname

    def get_chapters(self):
        # https://www.biquge.tv/17_17293/

        heardes = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        res = requests.get(url=self.blink, headers=heardes)
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)
        is_finished = False

        chapters_origin = xres.xpath('//dd/a/text()')
        true_index = 0
        for co in chapters_origin:
            if '第一章' in co:
                true_index = chapters_origin.index(co)
                break

        chapters = xres.xpath('//dd')[true_index:]
        print('章节数据：')
        print(chapters)
        for c in chapters:
            self.Q.put(c)


class DWorker(QThread):
    CHAPTERS = Makedata.Q
    download_finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        while True:
            try:
                self.get_chapter_data()
            except Exception as e:
                print(e)
                break

    def get_chapter_data(self):
        total = self.CHAPTERS.qsize()
        chapter = self.CHAPTERS.get(timeout=5)
        title = chapter.xpath('./a/text()')[0]
        href = base_url + chapter.xpath('./a/@href')[0]
        content = self.get_chapter_content(href)
        # data_for_file = {'total': total, 'index': index, 'title': title, 'href': href, 'content': content}

        # # 在此处写文件
        # base_dir = './'
        # fname = os.path.join(base_dir, self.bname)
        # with open('{}.txt'.format(fname), 'a', encoding='utf-8') as f:
        #     f.write(data_for_file['title'] + '\n' + data_for_file['content'] + '\n')
        # # print('已写入文件 >> {}.txt'.format(fname))

        data = {'total': total, 'title': title, 'content': content}
        # if index + 1 == total:
        #     is_finished = True
        self.download_finished.emit(data)

    def get_chapter_content(self, href):
        heardes = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        res = requests.get(url=href, headers=heardes)
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)

        content = xres.xpath('//*[@id="content"]')[0].xpath('string(.)')
        return content


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    md = Makedata()
    md.set_bname_and_blink('盗墓', 'https://www.biquge.tv/17_17293/')
    md.get_chapters()


    def show_msg(data):
        print(data)


    dwr1 = DWorker()
    dwr1.download_finished.connect(show_msg)
    dwr1.start()
    dwr2 = DWorker()
    dwr2.download_finished.connect(show_msg)
    dwr2.start()
    dwr3 = DWorker()
    dwr3.download_finished.connect(show_msg)
    dwr3.start()

    sys.exit(app.exec_())
