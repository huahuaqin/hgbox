# -*- coding:utf-8 -*-

import os
from threading import Thread

import wx

from business.jiraextend import JiraExtend


class PanelTestCaseChk(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.InitUI()

    def InitUI(self):
        self.txt_ver = wx.StaticText(self, -1, label=u'版本号', pos=(10, 10))
        self.in_ver = wx.TextCtrl(self, -1, size=(300, -1), pos=(100, 10))
        self.txt_case_path = wx.StaticText(self, -1, label=u'用例目录', pos=(10, 50))
        self.in_path = wx.TextCtrl(self, -1, size=(300, -1), pos=(100, 50))
        self.btn_select_dir = wx.Button(self, -1, size=(20, -1), label=u'..', pos=(400, 50))
        self.btn_chk_test = wx.Button(self, -1, label=u'用例检查', pos=(10, 100))
        self.txt_result = wx.TextCtrl(self, -1, size=(550, 400), pos=(10, 130),style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_BUTTON, self.on_btn_select_dir, self.btn_select_dir)
        self.Bind(wx.EVT_BUTTON, self.on_btn_chk_test, self.btn_chk_test)

    def on_btn_select_dir(self, event):
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.in_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_btn_chk_test(self, event):
        self.txt_result.SetValue(u'处理中...')
        self.btn_chk_test.Disable()
        t = Thread(target=self.chk_test, args=(version, case_path,))
        t.start()

    def chk_test(self, *args):
        je = JiraExtend(*args)
        result = je.check_case_coverage()
        self.txt_result.SetValue(result)
        self.btn_chk_test.Enable()

    def _get_value(self):
        version = self.in_ver.GetValue()
        case_path = self.in_path.GetValue()
        if not os.path.isdir(case_path):
            wx.MessageDialog(self, u'测试路径无效',style = wx.OK | wx.ICON_ERROR)
