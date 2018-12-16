# -*- coding:utf-8 -*-
import wx
import datetime


DEBUG = False


def wrap_wx_msg_exception(func):
    """
    装饰器，异常时弹出框显示异常信息
    :param func:
    :return:
    """
    def wrapper(self, *arg, **kw):
        try:
            return func(self, *arg, **kw)
        except Exception, e:
            dlg = wx.MessageDialog(self, str(e), style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            try:
                self.roll_back()
            except:
                pass
    return wrapper


def timer(func):
    """
    装饰器，用来统计执行时间
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        begin_time = datetime.datetime.now()
        a=func(*args, **kwargs)
        end_time = datetime.datetime.now()
        exec_time = (end_time-begin_time).total_seconds()
        if DEBUG:
            print '%s 执行时间: %s秒' % (func.__name__, exec_time)
        return a
    return wrapper
