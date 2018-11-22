# -*- coding:utf-8 -*-

import os
from threading import Thread
import wx
from business import *


def wrap_exception(func):
    def wrapper(self, *arg, **kw):
        try:
            return func(self, *arg, **kw)
        except Exception, e:
            # print str(e)
            dlg = wx.MessageDialog(self, str(e), style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
    return wrapper


class PanelTestCaseChk(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
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
        self.btn_chk_test.Disable()
        if not self._get_value():
            self.btn_chk_test.Enable()
            self.txt_result.SetValue(u'')
            return
        version, case_path = self._get_value()
        self.txt_result.SetValue(u'处理中...')
        t = Thread(target=self.chk_test, args=(version, case_path,))
        t.start()

    @wrap_exception
    def chk_test(self, *args):
        je = JiraExtend()
        result = je.check_case_coverage(*args)
        self.txt_result.SetValue(result)
        self.btn_chk_test.Enable()

    @wrap_exception
    def _get_value(self):
        je = JiraExtend()
        version = self.in_ver.GetValue()
        case_path = self.in_path.GetValue()
        if not os.path.isdir(case_path):
            dlg = wx.MessageDialog(self, u'测试路径无效',style = wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return
        if not je.version_exist(version):
            dlg = wx.MessageDialog(self, u'版本在jira中不存在',style = wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return
        return version,case_path

