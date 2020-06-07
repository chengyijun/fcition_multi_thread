# -*-coding:utf-8-*-

# import fix_qt_import_error

from PyQt5.Qt import *

from download_book import DWorker
from resource.fcition import Ui_Form
from search_book import SearchBook


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Abel的小说爬虫")
        self.move(600, 200)
        self.resize(400, 400)
        self.setupUi(self)
        # 设置表格 单元格宽度自动适应
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.books = None
        # 初始化下载器
        self.dworker = DWorker()
        self.dworker.download_finished.connect(self.ctrl_download_info)
        # 初始化进度条的值为0
        self.progressBar.setValue(0)
        # 初始化信息展示区 清空内容
        self.textBrowser.clear()
        # 初始化搜书
        self.sb = SearchBook()
        self.sb.search_finished.connect(self.fill_book_table)

    def search_book(self):
        print("开始搜书")
        # 更新信息展示区的内容
        self.textBrowser.clear()
        self.textBrowser.setText('火力全开，全力寻找中...')
        # 更新书籍表格之前 清空上一次数据
        for i in range(self.tableWidget_2.rowCount())[::-1]:
            self.tableWidget_2.removeRow(i)
        self.sb.set_bname(self.lineEdit.text())
        self.sb.start()

    def fill_book_table(self, books):
        self.books = books
        print('共搜索到 {} 本'.format(len(books)))
        print(books)
        if len(self.books) > 0:
            print('展示搜索表格')
            self.textBrowser.clear()
            self.textBrowser.setText('共搜索到 {} 本'.format(len(books)))
            self.tableWidget_2.setColumnCount(4)
            self.tableWidget_2.setRowCount(len(books))
            for index, book in enumerate(books):
                self.tableWidget_2.setItem(index, 0, QTableWidgetItem(book['bname']))
                self.tableWidget_2.setItem(index, 1, QTableWidgetItem(book['bauthor']))
                self.tableWidget_2.setItem(index, 2, QTableWidgetItem(book['bsize']))
                self.tableWidget_2.setCellWidget(index, 3, self.download_btn(index))
        else:
            self.textBrowser.setText('抱歉，您找的书暂时没有收录哦~~~')

    def ctrl_download_info(self, book, is_finished):
        # 在面板显示下载信息
        print("当前正在下载", book['title'])
        self.textBrowser.append(book['title'])
        if is_finished:
            print("========> 下载完成 <========")
            self.textBrowser.append("========> 下载完成 <========")
        # 操作进度条进度发生改变
        # 设置进度条 长度范围
        self.progressBar.setRange(0, int(book['total']))
        self.progressBar.setValue(int(book['index']) + 1)

    def download_the_book(self, i):
        print('开始下载第 {} 本书'.format(i + 1))
        print("书名：{} ---- 链接：{}".format(self.books[i]['bname'], self.books[i]['blink']))
        self.textBrowser.clear()
        self.textBrowser.setText('开始下载第 {} 本书 ---- < {} >'.format(i + 1, self.books[i]['bname']))

        # dwr = DWorker('https://www.biquge.tv/17_17293/')
        self.dworker.set_bname_and_blink(self.books[i]['bname'], self.books[i]['blink'])
        self.dworker.start()

    def download_btn(self, i):
        wg = QWidget()
        btn = QPushButton('下载')
        btn.setMinimumHeight(20)
        btn.clicked.connect(lambda: self.download_the_book(i))
        hbl = QHBoxLayout()
        hbl.addWidget(btn)
        hbl.setContentsMargins(0, 0, 0, 0)
        wg.setLayout(hbl)
        return wg


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Abel的小说爬虫")
    window.setWindowIcon(QIcon(':/icon/images/icon.ico'))
    window.show()
    sys.exit(app.exec_())
