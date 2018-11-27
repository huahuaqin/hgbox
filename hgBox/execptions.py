# -*- coding:utf-8 -*-

from jira.exceptions import JIRAError
from requests.exceptions import ConnectTimeout


class JiraException(Exception):
    def __init__(self, e, *args, **kw):
        Exception.__init__(self)
        self.e = e

    def __str__(self):

        if isinstance(self.e, ConnectTimeout):
            err_msg = '登陆JIRA超时;请确认地址正确/网络正常！'
        elif isinstance(self.e, JIRAError):
            if self.e.status_code == 401:
                err_msg = 'JIRA用户名/密码错误！'
        else:
            try:
                err_msg = str(self.e)
            except:
                err_msg = '未知错误'
        return err_msg


class SettingException(Exception):
    def __init__(self, section):
        err_msg = '配置文件中section[%s]不存在' %section
        Exception.__init__(self, err_msg)

