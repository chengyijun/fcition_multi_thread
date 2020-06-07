# -*- coding:utf-8 -*-
import os
from math import ceil
from multiprocessing import Process, cpu_count
from queue import Queue
from threading import Thread

import requests
from lxml import etree

from test4 import merge_book, get_safe_file_name, delete_target_dir


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
    def __init__(self, q: Queue, pname, bname):
        super().__init__()
        self.bname = bname
        self.pname = pname
        self.q = q

        if not os.path.exists(f'./{self.bname}'):
            os.mkdir(self.bname)

    def get_chapter_content(self, href):
        heardes = {
            'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                'Safari/537.36'
        }

        res = requests.get(url=href, headers=heardes)
        res.encoding = 'gbk'
        xres = etree.HTML(res.text)
        content = ''
        try:
            content = xres.xpath('//*[@id="content"]')[0].xpath('string(.)')
        except Exception as e:
            print('文章已被下架 爬取不到了' + e)
        finally:
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
        file_dir = self.bname
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
                 datas=None,
                 bname=None):
        super().__init__(group, target, name, args, kwargs)
        self.bname = bname
        self.datas = datas

    def task(self):
        q = Queue()
        for data in self.datas:
            q.put(data)
        w1 = W(q=q, pname=self.name, bname=self.bname)
        w2 = W(q=q, pname=self.name, bname=self.bname)
        w3 = W(q=q, pname=self.name, bname=self.bname)
        w4 = W(q=q, pname=self.name, bname=self.bname)
        w5 = W(q=q, pname=self.name, bname=self.bname)
        w1.start()
        w2.start()
        w3.start()
        w4.start()
        w5.start()

    def run(self):
        super().run()
        self.task()


def download_start(bname, blink):
    bname = get_safe_file_name(bname)
    downloader = Downloader(blink=blink)
    res = downloader.get_chapters()
    print(res)
    datas = res
    count = cpu_count()
    step = ceil(len(res) / count)
    workers = []
    for i in range(count):
        worker = Worker(name=f'p{i}', datas=datas[(step * i):(step * (i + 1))], bname=bname)
        workers.append(worker)
        worker.start()
    for worker in workers:
        worker.join()
    print('*' * 50)
    merge_book(bname)
    delete_target_dir(bname)
    print('下载完成')


def main():
    download_start('xxx', 'http://www.biquge.tv/42_42570/')


if __name__ == '__main__':
    main()
