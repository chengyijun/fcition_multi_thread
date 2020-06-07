# -*- coding:utf-8 -*-


class A:
    pass


def main():
    a = A()
    b = A()
    c = a

    print(id(a))
    print(id(b))
    print(id(c))


if __name__ == '__main__':
    main()
