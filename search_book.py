from urllib.request import quote

import bs4
import requests
from PyQt5.Qt import *

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
        # https://www.biquge7.top/search?keyword=鬼吹灯
        # url = https://www.biquge.tv/modules/article/search.php?searchkey=%B5%C1%C4%B9
        encodestr = quote(self.bname, encoding="utf-8")

        heardes = {
            'User-Agent': get_random_useragent()
        }

        res = requests.get(url=search_book_url + encodestr,
                           headers=heardes)
        # res.encoding = 'gbk'

        # xobj = etree.HTML(res.text)
        #
        # # //*[@id="nr"]
        # datas = xobj.xpath('//ul[@class="list_content"]')

        bs = bs4.BeautifulSoup(res.text, "lxml")
        # .tui_1.fenlei
        items = bs.select(".tui_1.fenlei .tui_1_item")
        # print(items)

        # print(items.select(".tui_1_item .title a")[0].get("title"))
        # print(items.select(".tui_1_item .title span:nth-child(2)")[0].text)
        books = []
        for item in items:
            bname = item.select_one(".title a").get("title")
            blink = item.select_one(".title a").get("href")
            bauthor = item.select_one(".title span:nth-child(2)").text
            bsize = ""
            binfo = {'bname': bname, 'bauthor': bauthor, 'bsize': bsize, 'blink': blink}
            books.append(binfo)
        print(books)
        self.search_finished.emit(books)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    sb = SearchBook()
    sb.set_bname('鬼吹灯')
    sb.search_finished.connect(lambda books: print(books))
    sb.start()
    sys.exit(app.exec_())
