# -*- coding:utf-8 -*-

import os
from threading import Thread
import wx
from business import *


def wrap_exception(func):
    """
    装饰器，异常时弹出框显示异常信息
    :param func:
    :return:
    """
    def wrapper(self, *arg, **kw):
        try:
            return func(self, *arg, **kw)
        except Exception, e:
            # print str(e)
            dlg = wx.MessageDialog(self, str(e), style=wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            self.roll_back()
    return wrapper


class PanelTestCaseChk(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        """
        界面布局初始化
        :return:
        """
        # jira 版本信息
        self.label_ver = wx.StaticText(self, -1, label=u'版本号', pos=(10, 10))
        self.in_ver = wx.TextCtrl(self, -1, size=(300, -1), pos=(100, 10))

        # 用例目录,提供路径选择框
        self.label_case_path = wx.StaticText(self, -1, label=u'用例目录', pos=(10, 50))
        self.in_path = wx.TextCtrl(self, -1, size=(300, -1), pos=(100, 50))
        # 文件夹选择框按钮
        self.btn_select_dir = wx.Button(self, -1, size=(20, -1), label=u'..', pos=(400, 50))
        self.Bind(wx.EVT_BUTTON, self.on_btn_select_dir, self.btn_select_dir)

        # 测试用例检查按钮
        self.btn_chk_test = wx.Button(self, -1, label=u'用例检查', pos=(10, 100))
        self.Bind(wx.EVT_BUTTON, self.on_btn_chk_test, self.btn_chk_test)

        # 开发单元测试用例检查按钮
        self.btn_unit_test_chk = wx.Button(self, -1, label=u'单元用例检查', pos=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_btn_unit_test_chk, self.btn_unit_test_chk)

        # 子任务版本检查
        self.btn_subtask_sync = wx.Button(self, -1, label=u'子任务版本检查', pos=(200, 100))
        self.Bind(wx.EVT_BUTTON, self.on_btn_subtask_sync, self.btn_subtask_sync)

        # 结果展示
        self.txt_result = wx.TextCtrl(self, -1, size=(550, 400), pos=(10, 130), style=wx.TE_MULTILINE)

        self.btns = (self.btn_chk_test, self.btn_unit_test_chk, self.btn_subtask_sync)

    def on_btn_select_dir(self, event):
        """
        文件夹选择框
        :param event:
        :return:
        """
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.in_path.SetValue(dlg.GetPath())
        dlg.Destroy()

    def on_btn_chk_test(self, event):
        """
        测试用例检查按钮响应事件
        :param event:
        :return:
        """
        # 先把按钮该页面的按钮置灰,
        self._disable_btn()
        self.txt_result.SetValue(u'处理中...')
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self.chk_test, args=())
        t.start()

    def on_btn_unit_test_chk(self, event):
        """
        单元用例检查按钮响应事件
        :param event:
        :return:
        """
        self._disable_btn()
        self.txt_result.SetValue(u'处理中...')
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self.unit_test_chk, args=())
        t.start()

    def on_btn_subtask_sync(self, event):
        """
        子任务版本检查按钮响应事件
        :param event:
        :return:
        """
        self._disable_btn()
        self.txt_result.SetValue(u'处理中...')
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self.subtask_sync, args=())
        t.start()

    @wrap_exception
    def chk_test(self):
        """
        测试用例检查处理函数
        :return:
        """
        if not self._get_value():
            self.roll_back()
            return
        version, case_path = self._get_value()
        je = JiraExtend()
        result = je.check_case_coverage(version, case_path)
        self.txt_result.SetValue(result)
        self._enable_btn()

    @wrap_exception
    def unit_test_chk(self):
        """
        单元测试用例检查处理函数
        :return:
        """
        if not self._get_value():
            self.roll_back()
            return
        version, case_path = self._get_value()
        pass
        self.txt_result.SetValue('')
        self._enable_btn()

    @wrap_exception
    def subtask_sync(self):
        """
        子任务版本检查处理函数
        :return:
        """
        if not self._get_value():
            self.roll_back()
            return
        version, case_path = self._get_value()
        je = JiraExtend()
        ret = je.sub_task_sync_version(version)
        if not ret:
            result = u'全部子任务版本正确'
        else:
            result = u''
            for r in ret:
                result = u'%s\r\n%s' % (result, r)
            result = u'以下jira的子任务版本可能存在问题，请检查：\r\n %s' %result
        self.txt_result.SetValue(result)
        self._enable_btn()

    @wrap_exception
    def _get_value(self):
        """
        获取用户输入
        :return:
        """
        je = JiraExtend()
        version = self.in_ver.GetValue()
        case_path = self.in_path.GetValue()
        if not os.path.isdir(case_path):
            dlg = wx.MessageDialog(self, u'用例目录无效', style = wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return
        if not je.version_exist(version):
            dlg = wx.MessageDialog(self, u'版本[%s]在jira中不存在' % version, style = wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return
        return version, case_path

    def _disable_btn(self, btn_obj=()):
        """
        把页面按钮置灰
        :param btn_obj:
        :return:
        """
        btn_obj = self.btns if btn_obj == () else btn_obj
        for b in btn_obj:
            if not isinstance(b, wx.Button):
                continue
            b.Disable()

    def _enable_btn(self, btn_obj=()):
        """
        把页面按钮置位Enable
        :param btn_obj:
        :return:
        """
        btn_obj = self.btns if btn_obj == () else btn_obj
        for b in btn_obj:
            if not isinstance(b, wx.Button):
                continue
            b.Enable()

    def roll_back(self):
        """
        异常后回滚界面状态
        :return:
        """
        self._enable_btn()
        self.txt_result.SetValue(u'')

