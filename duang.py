# -*- coding: utf-8 -*-
# duang duang 的持续访问某个 url

import getopt
import threading
import time
import tkinter.messagebox as messagebox
import urllib
import logging
from tkinter import *
from urllib import request
from urllib.request import HTTPRedirectHandler


class OpenerHTTPRedirectHandler(HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        print(headers.headers)
        return HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)

    def http_error_302(self, req, fp, code, msg, headers):
        print(headers.headers)
        return HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)


def refresh(options):
    req = request.Request(options.url)
    urllib.request.build_opener(OpenerHTTPRedirectHandler)
    req.add_header("User-Agent", "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, "
                                 "like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36")
    with request.urlopen(req) as f:
        status = f.status
    if options.sleep:
        time.sleep(options.sleep)
    return status


class Options(object):
    url = None
    count = None
    sleep = None

    def __str__(self):
        return "<%s url=%s, count=%s, sleep=%s>" % \
               (self.__class__.__name__, self.url, self.count, self.sleep)


def parse_options(argv):
    print(argv)
    opts, args = getopt.getopt(argv, "u:c:s:", ["url=", "count=", "sleep="])
    if len(opts) == 0:
        print("请输入参数，例如 --url=google.com --count=100 --sleep=2")
        raise AttributeError()

    options = Options()
    for k, v in opts:
        if k == "--url":
            options.url = v
        elif k == "--count":
            options.count = v
        elif k == "--sleep":
            options.sleep = v
    print(options.__str__())
    if not options.url:
        print("请输入一个地址,例如： --url=www.google.com")
        raise AttributeError()
    return options


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        self.fm_top = Frame(self)
        # label_url
        self.label_url = Label(self.fm_top, text="地址:", padx=5)
        self.label_url.pack(side=LEFT)
        # input_url
        self.input_url = Entry(self.fm_top)
        self.input_url.pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)
        self.fm_top.pack(fill=X, pady=5)

        self.fm_center = Frame(self)
        # label_count
        self.label_count = Label(self.fm_center, text="次数:", padx=5)
        self.label_count.pack(side=LEFT)
        # input_count
        self.input_count = Entry(self.fm_center, width=5)
        self.input_count.insert(0, "100")
        self.input_count.pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)
        # label_sleep
        self.label_sleep = Label(self.fm_center, text="间隔时间:", padx=5)
        self.label_sleep.pack(side=LEFT)
        # input_sleep
        self.input_sleep = Entry(self.fm_center, width=5)
        self.input_sleep.insert(0, "0")
        self.input_sleep.pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)
        # btn_action
        self.btn_action = Button(self.fm_center, text='开始', command=self.action)
        self.btn_action.pack(side=RIGHT, padx=10)
        self.fm_center.pack(fill=X)

        self.label_text_var = StringVar()

        self.fm_bottom = Frame(self)
        self.label = Label(self.fm_bottom, textvariable=self.label_text_var, width=50, height=15)
        self.label.pack()
        self.fm_bottom.pack(fill=X)

    def action(self):
        url = self.input_url.get()
        count = self.input_count.get()
        sleep = self.input_sleep.get()

        if re.match(r"^\+?[1-9][0-9]*$", count):
            count = int(count)
        else:
            messagebox.showinfo("提示", "次数只能是数字，不能是0")
            return
        if not re.match(r"^\+?[0-9]*$", sleep):
            messagebox.showinfo("提示", "间隔时间只能是数字")
            return
        if not url:
            messagebox.showinfo("提示", "请输入地址")
        else:
            options = Options()
            options.url = url
            options.count = count
            options.sleep = int(sleep)
            t = threading.Thread(target=main, args=(options, self.label_text_var))
            t.setDaemon(True)
            t.start()


def main(options, label_text=None):
    i = 0
    if options.count:
        count = options.count
    else:
        count = 100
    while i < count:
        status = refresh(options)
        i += 1
        text = "已访问%s次 - status:%s" % (i, status)
        if not label_text:
            print(text)
        else:
            label_text.set(text)
    text_end = "结束访问，总共%s次" % count
    if not label_text:
        print(text_end)
    else:
        label_text.set(text_end)


def center(win):
    """
    centers a tkinter window
    :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    fm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * fm_width
    height = win.winfo_height()
    title_bar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + title_bar_height + fm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


if __name__ == "__main__":
    try:
        if len(sys.argv[1:]) == 0:
            root = Tk()
            root.title("duang")
            Application(root)
            center(root)
            root.mainloop()
        else:
            main(parse_options(sys.argv[1:]))
    except Exception as e:
        logging.error(e.args)
        sys.exit(1)
