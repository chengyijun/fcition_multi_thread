# -*- coding:utf-8 -*-
import os
import re

import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from lxml import etree

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
            file_name = os.path.join(os.getcwd(), get_safe_file_name(self.bname))
            content = self.task(href)
            # print(f'{file_name}/{index}-{title}.txt')
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

        while True:
            res = requests.get(url=href, headers=heardes, timeout=10)
            res.encoding = 'gbk'
            xres = etree.HTML(res.text)
            content = ''
            try:
                content = xres.xpath('//*[@id="content"]')[0].xpath('string(.)')
                break
            except Exception as e:
                continue
                # print('--------------章节删除 获取不到--------------', e, href)

        # 内容清洗
        content = re.sub(r'\n', '', content)
        content = re.sub(r'ad\d+\(\);', '', content)
        content = re.sub(r'全新的短域名.*?提供更快更稳定的访问，亲爱的读者们，赶紧把我记下来吧.*?（全小说无弹窗）', '', content)
        return content


def main():
    import sys
    app = QApplication(sys.argv)
    datas = [
        {'href': 'https://www.biquge.tv/18_18405/19534328.html', 'index': 1, 'title': '第1229章 又回尊王墓', 'total': 1240},
        {'href': 'https://www.biquge.tv/18_18405/19534326.html', 'index': 2, 'title': '第1228章 再见小凤娇', 'total': 1240}]
    worker = Worker(datas=datas, bname='鬼吹灯')
    worker.download_info[dict].connect(lambda x: print(x))
    worker.start()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
