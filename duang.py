# -*- coding: utf-8 -*-
# duang duang 的持续访问某个 url

import time
import getopt
import urllib
import threading
import tkinter.messagebox as messagebox
from urllib import request
from urllib.request import HTTPRedirectHandler
from tkinter import *


class OpenerHTTPRedirectHandler(HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, httpmsg):
        print(httpmsg.headers)
        return HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, httpmsg)

    def http_error_302(self, req, fp, code, msg, httpmsg):
        print(httpmsg.headers)
        return HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, httpmsg)


def refresh(options):
    req = request.Request(options.url)
    urllib.request.build_opener(OpenerHTTPRedirectHandler)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
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
        self.label_url = Label(self.fm_top, text="地址：")
        self.label_url.pack(side=LEFT)
        self.input_url = Entry(self.fm_top)
        self.input_url.pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)
        self.fm_top.pack(fill=X, pady=5)

        self.fm_center = Frame(self)
        self.label_count = Label(self.fm_center, text="次数：")
        self.label_count.pack(side=LEFT)
        self.input_count = Entry(self.fm_center)
        self.input_count.insert(0, "100")
        self.input_count.pack(side=LEFT, expand=True, fill=X, padx=5, pady=5)
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
        if isinstance(count, int) or int(count):
            count = int(count)
        else:
            self.label_text_var.set("次数只能是数字")
            raise AttributeError()
        if not url:
            messagebox.showinfo('提示', "请输入地址")
        else:
            options = Options()
            options.url = url
            options.count = count
            t = threading.Thread(target=main, args=(options, self.label_text_var))
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


if __name__ == "__main__":
    try:
        if len(sys.argv[1:]) == 0:
            app = Application()
            app.master.title = "刷子"
            app.mainloop()
        else:
            main(parse_options(sys.argv[1:]))
    except Exception as e:
        sys.exit(1)
