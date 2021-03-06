from urllib.request import quote

import requests
from PyQt5.Qt import *
from lxml import etree

from config_url import search_book_url
from utils import get_random_useragent


class SearchBook(QThread):
    search_finished = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.blink = None
        self.bname = None

    def set_bname(self, bname):
        self.bname = bname

    def run(self):
        self.get_books()

    def get_books(self):
        # url = https://www.biquge.tv/modules/article/search.php?searchkey=%B5%C1%C4%B9
        encodestr = quote(self.bname, encoding="utf-8")

        heardes = {
            'User-Agent': get_random_useragent()
        }

        res = requests.get(url=search_book_url + encodestr,
                           headers=heardes)
        res.encoding = 'gbk'

        xobj = etree.HTML(res.text)

        # //*[@id="nr"]
        datas = xobj.xpath('//ul[@class="list_content"]')
        books = []
        for data in datas:
            bname = data.xpath('.//li[1]/a/text()')[0]
            blink = data.xpath('.//li[1]/a/@href')[0]
            bauthor = data.xpath('.//li[3]/a/text()')[0]
            bsize = data.xpath('.//li[4]/text()')[0]
            binfo = {'bname': bname, 'bauthor': bauthor, 'bsize': bsize, 'blink': blink}
            books.append(binfo)
        # print(books)
        self.search_finished.emit(books)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    sb = SearchBook()
    sb.set_bname('异星虫族')
    sb.search_finished.connect(lambda books: print(books))
    sb.start()
    sys.exit(app.exec_())
