# -*- coding:utf-8 -*-
import os

from PyQt5.QtCore import QThread, pyqtSignal

from utils import get_config


class Merge(QThread):
    merged = pyqtSignal([bool])

    def __init__(self, parent=None, bname=None):
        super().__init__(parent)
        self.bname = bname

    def task(self):
        self.merge_book(self.bname)
        self.delete_target_dir(f'./{self.bname}')
        self.merged[bool].emit(True)

    def run(self):
        self.task()

    def merge_book(self, bname):
        if not os.path.exists(f'./{bname}'):
            return
        files = os.listdir(f'./{bname}')
        # print(files)
        sorted_files = sorted(files, key=lambda x: int(str(x).split('-')[0]))
        # print(sorted_files)
        dlp = get_config().get('download').get('path')
        if not os.path.exists(dlp):
            dlp = get_config().get('download').get('default_path')

        with open(f'{dlp}/{bname}.txt', 'a', encoding='utf-8') as f:
            for file in sorted_files:
                with open(os.path.join(os.getcwd(), bname, file), 'r', encoding='utf-8') as f2:
                    content = f2.read()
                    f.write(content + "\r\n")

    def delete_target_dir(self, target_dir):
        if not os.path.exists(target_dir):
            return
        files = os.listdir(target_dir)
        for file in files:
            file = os.path.join(target_dir, file)
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                self.delete_target_dir(file)
            else:
                print('参数错误')
        os.removedirs(target_dir)


def main():
    pass


if __name__ == '__main__':
    main()
