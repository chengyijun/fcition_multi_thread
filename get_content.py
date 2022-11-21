# -*- coding:utf-8 -*-

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup

from config import ROOT_PATH
from utils import get_safe_file_name, get_random_useragent


class Worker(QThread):
    download_info = pyqtSignal([dict])

    def __init__(self, parent=None, datas=None, bname=None):
        super().__init__(parent)
        # {'href': 'https://www.biquge.tv/18_18405/19534328.html', 'index': 1, 'title': '第1229章 又回尊王墓', 'total': 1240}
        self.bname = bname
        self.datas = datas

    def run(self):
        total = len(self.datas)
        for i, data in enumerate(self.datas, start=1):
            href = data.get('href')
            index = data.get('index')
            title = get_safe_file_name(data.get('title'))
            file_name = get_safe_file_name(self.bname)
            content = self.task(href)
            # print(f'{file_name}/{index}-{title}.txt')

            ROOT_PATH.joinpath(file_name).mkdir(parents=True, exist_ok=True)
            with open(f'{file_name}/{index}-{title}.txt', 'w', encoding='utf-8') as f:
                f.write(f'{title}\n{content}\n\n')
            data = {
                'total': total,
                'index': i,
                'title': title,
                'href': href
            }
            self.download_info[dict].emit(data)
            # 频率反扒
            # time.sleep(random.random() + 1)

    def task(self, href):
        heardes = {
            'User-Agent': get_random_useragent()
        }
        res = requests.get(url=href, headers=heardes, timeout=10)
        # res.encoding = 'gbk'
        bs = BeautifulSoup(res.text, "lxml")
        content = ""
        try:
            cs = bs.select_one("div.text")
            for index, paragraph in enumerate(cs.strings):
                if index == 0:
                    if "，更新快，，免费读！" in paragraph:
                        continue
                content += paragraph + "\n"
            print(content)

            # 内容清洗
        except:
            pass
            print('--------------章节删除 获取不到--------------')
        return content


def main():
    import sys
    app = QApplication(sys.argv)
    datas = [{'href': 'https://www.biquge7.top/37360/1', 'index': 1, 'title': '引子', 'total': 241}]
    worker = Worker(datas=datas, bname='鬼吹灯')
    worker.download_info[dict].connect(lambda x: print(x))
    worker.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
