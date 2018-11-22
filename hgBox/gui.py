# -*- coding:utf-8 -*-

import wx
from Panel import *


if __name__ == '__main__':
    app = wx.App(False)
    screen_size = wx.DisplaySize()   # 设备屏幕大小
    pos = (screen_size[0]/2-300, screen_size[1]/2-300)
    frame = wx.Frame(None, title=u"测试三部", size=(600, 600), pos=pos, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
    nb = wx.Notebook(frame)
    nb.AddPage(PanelTestCaseChk(nb), u'用例检查')
    nb.AddPage(PanelSetting(nb), u'参数设置')
    frame.Show()
    app.MainLoop()
