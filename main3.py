# -*-coding:utf-8-*-

# import fix_qt_import_error
import os
from math import ceil

from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QApplication, QHeaderView, QTableWidgetItem

from download_book import DWorker
from get_chapters_info import Chapters
from get_content import Worker
from merge_chapters import Merge
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
        # 需要下载书的章节信息
        self.chapters = None
        self.chapters_data = None
        self.bname = None
        # 小说章节下载线程
        self.worker1 = None
        self.worker2 = None
        self.worker3 = None
        self.worker4 = None
        self.worker5 = None
        # 各个线程是否下载完成
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.flag4 = False
        self.flag5 = False
        # 合并小说的线程
        self.merge = None
        # 起一个定时器 判定是否各线程下载结束 开始合并章节
        self.timer = None

    def search_book(self):
        # print("开始搜书")
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
        # print('共搜索到 {} 本'.format(len(books)))
        # print(books)
        if len(self.books) > 0:
            # print('展示搜索表格')
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

    def ctrl_download_info(self, book):
        # 在面板显示下载信息
        # print("当前正在下载", book['title'])
        self.textBrowser.append(book['title'])
        # if is_finished:
        #     # print("========> 下载完成 <========")
        #     self.textBrowser.append("========> 下载完成 <========")
        # 操作进度条进度发生改变
        # 设置进度条 长度范围

        if self.sender() == self.worker1:
            self.progressBar.setRange(0, int(book['total']))
            self.progressBar.setValue(int(book['index']))
            if int(book['total']) == int(book['index']):
                self.flag1 = True
        if self.sender() == self.worker2:
            self.progressBar_2.setRange(0, int(book['total']))
            self.progressBar_2.setValue(int(book['index']))
            if int(book['total']) == int(book['index']):
                self.flag2 = True
        if self.sender() == self.worker3:
            self.progressBar_3.setRange(0, int(book['total']))
            self.progressBar_3.setValue(int(book['index']))
            if int(book['total']) == int(book['index']):
                self.flag3 = True
        if self.sender() == self.worker4:
            self.progressBar_4.setRange(0, int(book['total']))
            self.progressBar_4.setValue(int(book['index']))
            if int(book['total']) == int(book['index']):
                self.flag4 = True
        if self.sender() == self.worker5:
            self.progressBar_5.setRange(0, int(book['total']))
            self.progressBar_5.setValue(int(book['index']))
            if int(book['total']) == int(book['index']):
                self.flag5 = True

    def download_the_book(self, i):
        # print('开始下载第 {} 本书'.format(i + 1))
        # print("书名：{} ---- 链接：{}".format(self.books[i]['bname'], self.books[i]['blink']))
        self.textBrowser.clear()
        self.textBrowser.setText('开始下载第 {} 本书 ---- < {} >'.format(i + 1, self.books[i]['bname']))

        # dwr = DWorker('https://www.biquge.tv/17_17293/')
        # self.dworker.set_bname_and_blink(self.books[i]['bname'], self.books[i]['blink'])
        # self.dworker.start()
        # 查询并返回需要下载本书的所有章节信息  由于是耗时操作 所以必须单独开线程
        self.chapters = Chapters(bname=self.books[i]['bname'], blink=self.books[i]['blink'])
        self.bname = self.books[i]['bname']
        self.chapters.chapters_got.connect(self.set_chapters_data)
        self.chapters.start()
        # print('-' * 50)

    def set_chapters_data(self, data):
        # print(data)
        self.chapters_data = data
        # 得到要下载的书章节信息之后 开始下载内容 由于耗时操作 所以起新线程
        workers_num = 5
        step = ceil(len(self.chapters_data) / workers_num)
        book_dir = os.path.join(os.getcwd(), self.bname)
        if not os.path.exists(book_dir):
            os.mkdir(book_dir)
        self.worker1 = Worker(datas=self.chapters_data[:step], bname=self.bname)
        self.worker1.download_info[dict].connect(self.ctrl_download_info)
        self.worker1.start()
        self.worker2 = Worker(datas=self.chapters_data[step:2 * step], bname=self.bname)
        self.worker2.download_info[dict].connect(self.ctrl_download_info)
        self.worker2.start()
        self.worker3 = Worker(datas=self.chapters_data[2 * step:3 * step], bname=self.bname)
        self.worker3.download_info[dict].connect(self.ctrl_download_info)
        self.worker3.start()
        self.worker4 = Worker(datas=self.chapters_data[3 * step:4 * step], bname=self.bname)
        self.worker4.download_info[dict].connect(self.ctrl_download_info)
        self.worker4.start()
        self.worker5 = Worker(datas=self.chapters_data[4 * step:5 * step], bname=self.bname)
        self.worker5.download_info[dict].connect(self.ctrl_download_info)
        self.worker5.start()
        # print('+' * 50)
        # 起定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.start_merge_chapters)
        self.timer.start(1000)

    def start_merge_chapters(self):
        status1 = self.worker1.isFinished()
        status2 = self.worker2.isFinished()
        status3 = self.worker3.isFinished()
        status4 = self.worker4.isFinished()
        status5 = self.worker5.isFinished()
        if all([status1, status2, status3, status4, status5]):
            # 合并章节
            self.textBrowser.append("\n\n小说合并中...")
            # 合并小说 删除小说章节文件 是耗时操作 需要起新线程做
            self.merge = Merge(bname=self.bname)
            self.merge.merged[bool].connect(self.merge_success)
            self.merge.start()
            # 停止定时器
            self.timer.stop()

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

    def merge_success(self, success_flag):
        if success_flag:
            self.textBrowser.append('=' * 20 + f'《{self.bname}》 合并完成 尽情享受吧' + '=' * 20)
            self.textBrowser.append(f'----> 存储位置：{os.path.join(os.getcwd(), self.bname)}.txt')
            # self.merge.stop()


def main():
    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle("Abel的小说爬虫")
    window.setWindowIcon(QIcon(':/icon/images/icon.ico'))
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
