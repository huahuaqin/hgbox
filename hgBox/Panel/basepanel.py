# -*- coding:utf-8 -*-
import wx


class BasePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.btns = None

    def init_ui(self):
        """

        :return:
        """
        pass

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

    def _get_value(self, inputs):
        """
        获取用户输入
        :param inputs: 输入框对象
        :return:
        """
        return [i.GetValue() for i in inputs if isinstance(i, wx.TextCtrl)]

    def roll_back(self):
        """
        异常后回滚界面状态
        :return:
        """
        self._enable_btn()

