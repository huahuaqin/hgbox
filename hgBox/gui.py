# -*- coding:utf-8 -*-

import os
from threading import Thread

import configparser
import wx

from business.jiraextend import JiraExtend


class PanelTestCaseChk(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.txt_ver = wx.StaticText(self, -1, label=u'版本号', pos=(10, 10))
        self.input_ver = wx.TextCtrl(self, -1, size=(300, -1), pos=(100, 10))
        self.txt_case_path = wx.StaticText(self, -1, label=u'用例目录', pos=(10, 50))
        self.input_path = wx.TextCtrl(self, -1, size=(300, -1), pos=(100, 50))
        self.btn_select_dir = wx.Button(self, -1, size=(20, -1), label=u'..', pos=(400, 50))
        self.btn_chk_test = wx.Button(self, -1, label=u'用例检查', pos=(10, 100))
        self.txt_result = wx.TextCtrl(self, -1, size=(550, 400), pos=(10, 130),style=wx.TE_MULTILINE)
        self.Bind(wx.EVT_BUTTON, self.onbtn_select_dir, self.btn_select_dir)
        self.Bind(wx.EVT_BUTTON, self.onbtn_chk_test, self.btn_chk_test)

    def onbtn_select_dir(self, event):
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.input_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def onbtn_chk_test(self, event):
        version = self.input_ver.GetValue()
        case_path = self.input_path.GetValue()
        if (version == '') or (case_path == ''):
            wx.MessageBox(u'版本/路径不能为空', u'' ,wx.OK | wx.ICON_WARNING)
            return
        self.txt_result.SetValue(u'处理中...')
        self.btn_chk_test.Disable()
        t = Thread(target=self.chk_test, args=(version, case_path,))
        t.start()

    def chk_test(self, *args):
        je = JiraExtend(*args)
        result = je.check_case_coverage()
        self.txt_result.SetValue(result)
        self.btn_chk_test.Enable()


class PanelCFG(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.txt_jira_server = wx.StaticText(self, -1, label=u'Jira地址:', pos=(10, 10))
        self.input_jira_server = wx.TextCtrl(self, -1, size=(400, -1), pos=(100, 10))
        self.txt_jira_user = wx.StaticText(self, -1, label=u'jira用户:', pos=(10, 50))
        self.input_jira_user = wx.TextCtrl(self, -1, size=(150, -1), pos=(100, 50))
        self.txt_jira_pwd = wx.StaticText(self, -1, label=u'jira密码:', pos=(300, 50))
        self.input_jira_pwd = wx.TextCtrl(self, -1, size=(150, -1), pos=(350, 50))
        self.btn_save = wx.Button(self, -1, label=u'保存', pos=(250, 100))
        self.Bind(wx.EVT_BUTTON, self.onbtn_save, self.btn_save)
        self.init()

    def init(self):
        cfg_handle = configparser.ConfigParser()
        cfg_name = 'config.ini'
        if not os.path.exists(cfg_name):
            with open(cfg_name, 'w+') as f:
                cfg_handle.read(cfg_name)
                cfg_handle.add_section('JIRA_INFO')
                cfg_handle.set('JIRA_INFO', 'jira_server', '')
                cfg_handle.set('JIRA_INFO', 'user', '')
                cfg_handle.set('JIRA_INFO', "password", '')
                cfg_handle.write(f)
                return
        cfg_handle.read(cfg_name)
        self.input_jira_server.SetValue(cfg_handle.get('JIRA_INFO','jira_server'))
        self.input_jira_user.SetValue(cfg_handle.get('JIRA_INFO','user'))
        self.input_jira_pwd.SetValue(cfg_handle.get('JIRA_INFO','password'))

    def onbtn_save(self, event):
        jira_server = self.input_jira_server.GetValue()
        user= self.input_jira_user.GetValue()
        pwd = self.input_jira_pwd.GetValue()
        cfg_name = 'config.ini'
        if not os.path.exists(cfg_name):
            with open(cfg_name, 'a+') as fp:
                pass
        cfg_handle = configparser.ConfigParser()
        cfg_handle.read(cfg_name)
        if 'JIRA_INFO' not in cfg_handle.sections():
            cfg_handle.add_section('JIRA_INFO')
        cfg_handle.set('JIRA_INFO', 'jira_server', jira_server)
        cfg_handle.set('JIRA_INFO', 'user', user)
        cfg_handle.set('JIRA_INFO', "password", pwd)

        with open(cfg_name, 'w+') as f:
            cfg_handle.write(f)

        wx.MessageBox(u'修改成功', u'' ,wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title=u"测试三部", size=(600, 600),)
    nb = wx.Notebook(frame)
    nb.AddPage(PanelTestCaseChk(nb), u'用例检查')
    nb.AddPage(PanelCFG(nb), u'参数设置')
    frame.Show()
    app.MainLoop()
