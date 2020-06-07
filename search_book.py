import requests
from PyQt5.Qt import *
from urllib.request import quote, unquote

from lxml import etree
from config_url import search_book_url


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
        encodestr = quote(self.bname, encoding="gbk")

        heardes = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        }

        res = requests.get(url=search_book_url + encodestr,
                           headers=heardes)
        res.encoding = 'gbk'

        xobj = etree.HTML(res.text)

        # //*[@id="nr"]
        datas = xobj.xpath('//*[@id="nr"]')
        books = []
        for data in datas:
            bname = data.xpath('.//td[1]//text()')[0]
            blink = data.xpath('.//td[1]//a/@href')[0]
            bauthor = data.xpath('.//td[3]//text()')[0]
            bsize = data.xpath('.//td[4]//text()')[0]
            binfo = {'bname': bname, 'bauthor': bauthor, 'bsize': bsize, 'blink': blink}
            books.append(binfo)
        # print(books)
        self.search_finished.emit(books)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    sb = SearchBook()
    sb.set_bname('盗墓')
    sb.search_finished.connect(lambda books: print(books))
    sb.start()
    sys.exit(app.exec_())
