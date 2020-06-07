# -*- coding:utf-8 -*-
from multiprocessing import Process
from queue import Queue

import requests
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication
from lxml import etree


class Downloader:
    base_url = 'http://www.biquge.tv'

    def __init__(self, blink=None):
        self.blink = blink

    def get_chapters(self):
        # https://www.biquge.tv/17_17293/

        heardes = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        res = requests.get(url=self.blink, headers=heardes)
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)

        chapters_origin = xres.xpath('//dd/a/text()')
        true_index = 0
        for co in chapters_origin:
            if '第一章' in co:
                true_index = chapters_origin.index(co)
                break

        chapters = xres.xpath('//dd')[true_index:]
        total = len(chapters)
        datas = []
        for index, chapter in enumerate(chapters, start=1):
            title = chapter.xpath('./a/text()')[0]
            href = self.base_url + chapter.xpath('./a/@href')[0]
            data = {'total': total, 'index': index, 'title': title, 'href': href}
            datas.append(data)
        return datas


class W(QThread):
    dinfo = pyqtSignal([dict])

    def __init__(self, q: Queue, pname):
        super().__init__()
        self.pname = pname
        self.q = q

    def get_chapter_content(self, href):
        heardes = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        res = requests.get(url=href, headers=heardes)
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)

        content = xres.xpath('//*[@id="content"]')[0].xpath('string(.)')
        return content

    def run(self) -> None:
        super().run()
        while True:
            self.task()
            if self.q.empty():
                break

    def task(self):
        # sleep(1)
        data = self.q.get()
        href = data.get('href')
        index = data.get('index')
        title = data.get('title')
        content = self.get_chapter_content(href=href)
        file_name = f'{index}-{title}.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'正在爬取 {file_name}')
        info = {
            'index': index,
            'title': title
        }
        self.dinfo[dict].emit(info)
        self.q.task_done()


class Worker(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, datas=None):
        super().__init__(group, target, name, args, kwargs)

        self.w1 = None
        self.w2 = None
        self.w3 = None
        self.datas = datas
        self.q = None

    def task(self):
        print(666)
        self.q = Queue()
        for i in self.datas:
            self.q.put(i)
        self.w1 = W(q=self.q, pname=self.name)
        self.w2 = W(q=self.q, pname=self.name)
        self.w3 = W(q=self.q, pname=self.name)
        self.w1.start()
        self.w2.start()
        self.w3.start()

    def run(self):
        super().run()
        self.task()


def main():
    import sys

    app = QApplication(sys.argv)

    downloader = Downloader(blink='http://www.biquge.tv/17_17293/')
    res = downloader.get_chapters()
    print(res)
    datas = res
    worker = Worker(name='p1', datas=datas[:80])
    worker.start()
    worker2 = Worker(name='p2', datas=datas[80:160])
    worker2.start()
    worker3 = Worker(name='p3', datas=datas[160:240])
    worker3.start()
    worker4 = Worker(name='p4', datas=datas[240:])
    worker4.start()
    print(223)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
