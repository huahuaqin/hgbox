# -*- coding:utf-8 -*-

from jira.exceptions import JIRAError
from requests.exceptions import ConnectTimeout


class JiraException(Exception):
    def __init__(self, e, *args, **kw):
        Exception.__init__(self)
        self.e = e

    def __str__(self):
        err_msg = u''
        if isinstance(self.e, ConnectTimeout):
            err_msg = str('登陆JIRA超时;请确认地址正确/网络正常！')
        return err_msg

