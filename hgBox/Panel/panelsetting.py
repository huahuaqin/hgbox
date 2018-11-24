# -*- coding:utf-8 -*-
import wx
from business import *

class PanelSetting(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.sett = Setting()
        self.init_ui()
        self.init()

    def init_ui(self):
        """
        界面初始化
        :return:
        """
        # jira 服务器地址
        self.txt_jira_server = wx.StaticText(self, -1, label=u'Jira地址:', pos=(10, 10))
        self.in_jira_server = wx.TextCtrl(self, -1, size=(400, -1), pos=(100, 10))

        # jira 用户名密码
        self.txt_jira_user = wx.StaticText(self, -1, label=u'Jira用户:', pos=(10, 50))
        self.in_jira_user = wx.TextCtrl(self, -1, size=(150, -1), pos=(100, 50))
        self.txt_jira_pwd = wx.StaticText(self, -1, label=u'Jira密码:', pos=(300, 50))
        self.in_jira_pwd = wx.TextCtrl(self, -1, size=(150, -1), pos=(350, 50))

        # jira项目
        self.txt_jira_prj = wx.StaticText(self, -1, label=u'Jira项目:', pos=(10, 90))
        self.in_jira_prj = wx.TextCtrl(self, -1, size=(400, -1), pos=(100, 90))

        #保存按钮
        self.btn_save = wx.Button(self, -1, label=u'保存', pos=(200, 300))
        self.Bind(wx.EVT_BUTTON, self.on_btn_save, self.btn_save)

        # jira登陆验证
        self.btn_jira_login_chk = wx.Button(self, -1, label=u'jira登陆验证', pos=(300, 300))
        self.Bind(wx.EVT_BUTTON, self.on_btn_jira_login_chk, self.btn_jira_login_chk)


    def init(self):
        jira_server = self.sett.get_value('JIRA_INFO', 'jira_server')
        jira_user = self.sett.get_value('JIRA_INFO', 'jira_user')
        jira_pwd = self.sett.get_value('JIRA_INFO', 'jira_pwd')
        jira_prj = self.sett.get_value('JIRA_INFO', 'jira_prj')
        self.in_jira_server.SetValue(jira_server)
        self.in_jira_user.SetValue(jira_user)
        self.in_jira_pwd.SetValue(jira_pwd)
        self.in_jira_prj.SetValue(jira_prj)

    def on_btn_save(self, event):
        """
        保存修改内容到配置文件中
        :param event:
        :return:
        """
        jira_server = self.in_jira_server.GetValue()
        user = self.in_jira_user.GetValue()
        pwd = self.in_jira_pwd.GetValue()
        prj = self.in_jira_prj.GetValue()
        upd_info = (
            ['JIRA_INFO', 'jira_server', jira_server],
            ['JIRA_INFO', 'jira_user', user],
            ['JIRA_INFO', 'jira_pwd', pwd],
            ['JIRA_INFO', 'jira_prj', prj],
        )
        self.sett.upd(upd_info)
        wx.MessageBox(u'修改成功', u'' ,wx.OK | wx.ICON_INFORMATION)

    def on_btn_jira_login_chk(self, event):
        """
        jira信息验证
        :return:
        """
        try:
            JiraExtend()
            dlg = wx.MessageDialog(self, u'登陆成功', style=wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
        except Exception, e:
            dlg = wx.MessageDialog(self, str(e), style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
