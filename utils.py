# -*- coding:utf-8 -*-
import os
import re

import yaml


def set_config(data: dict):
    yaml_file = os.path.join(os.getcwd(), "./config/main.yml")
    with open(yaml_file, 'w', encoding="utf-8") as f:
        f.write(yaml.dump(data))


def get_config():
    yaml_file = os.path.join(os.getcwd(), "./config/main.yml")
    with open(yaml_file, 'r', encoding="utf-8") as f:
        file_data = f.read()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


def delete_target_dir(target_dir):
    if not os.path.exists(target_dir):
        return
    files = os.listdir(target_dir)
    for file in files:
        file = os.path.join(target_dir, file)
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            delete_target_dir(file)
        else:
            print('参数错误')
    os.removedirs(target_dir)


def get_safe_file_name(file_name):
    return re.sub(r'[<,>,/,\\,|,:,",\',.,*,?]', '-', file_name)


def merge_book(bname):
    if not os.path.exists(f'./{bname}'):
        return
    files = os.listdir(f'./{bname}')
    # print(files)
    sorted_files = sorted(files, key=lambda x: int(str(x).split('-')[0]))
    # print(sorted_files)
    with open(f'./{bname}.txt', 'a', encoding='utf-8') as f:
        for file in sorted_files:
            with open(os.path.join(os.getcwd(), bname, file), 'r', encoding='utf-8') as f2:
                content = f2.read()
                f.write(content + "\r\n")


def main():
    merge_book('启禀王爷：王妃，又盗墓啦！')


if __name__ == '__main__':
    main()
