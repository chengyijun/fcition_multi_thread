# -*- coding:utf-8 -*-
from math import ceil
from multiprocessing import Process, cpu_count
from queue import Queue
from threading import Thread

import requests
from lxml import etree


class Downloader():
    base_url = 'http://www.biquge.tv'

    def __init__(self, blink=None):
        self.blink = blink

    def get_chapters(self):
        # https://www.biquge.tv/17_17293/

        heardes = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                'Safari/537.36'
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
            data = {
                'total': total,
                'index': index,
                'title': title,
                'href': href
            }
            datas.append(data)
        return datas


class W(Thread):
    def __init__(self, q: Queue, pname):
        super().__init__()
        self.pname = pname
        self.q = q

    def get_chapter_content(self, href):
        heardes = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                'Safari/537.36'
        }

        res = requests.get(url=href, headers=heardes)
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)

        content = xres.xpath('//*[@id="content"]')[0].xpath('string(.)')
        return content

    def run(self) -> None:
        super().run()
        while True:
            # 结束线程
            if self.q.empty():
                break
            # 耗时任务
            self.task()

    def task(self):
        # sleep(1)
        data = self.q.get()
        if not data:
            return
        href = data.get('href')
        index = data.get('index')
        title = data.get('title')
        content = self.get_chapter_content(href=href)
        file_dir = 'chapters'
        file_name = f'{file_dir}/{index}-{title}.txt'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'正在爬取 {file_name}')
        self.q.task_done()


class Worker(Process):
    def __init__(self,
                 group=None,
                 target=None,
                 name=None,
                 args=(),
                 kwargs={},
                 datas=None):
        super().__init__(group, target, name, args, kwargs)
        self.datas = datas

    def task(self):
        q = Queue()
        for i in self.datas:
            q.put(i)
        w1 = W(q=q, pname=self.name)
        w2 = W(q=q, pname=self.name)
        w3 = W(q=q, pname=self.name)
        w4 = W(q=q, pname=self.name)
        w5 = W(q=q, pname=self.name)
        w1.start()
        w2.start()
        w3.start()
        w4.start()
        w5.start()

    def run(self):
        super().run()
        self.task()


def main():
    downloader = Downloader(blink='http://www.biquge.tv/17_17293/')
    res = downloader.get_chapters()
    print(res)
    datas = res
    count = cpu_count()
    step = ceil(len(res) / count)
    workers = []
    for i in range(count):
        worker = Worker(name=f'p{i}', datas=datas[(step * i):(step * (i + 1))])
        workers.append(worker)
        worker.start()
    for worker in workers:
        worker.join()
    print('*' * 50)


if __name__ == '__main__':
    main()
