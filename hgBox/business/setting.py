# -*- coding:utf-8 -*-

from configparser import ConfigParser
import os
from execptions import SettingException

CFG_PATH = r'config.ini'
ATTR = {'JIRA_INFO': {'jira_server': '',
                      'jira_user': '',
                      'jira_pwd': '',
                      'jira_prj': ''},
        }


class Setting(dict):
    def __init__(self):
        dict.__init__(self)
        self.cfg = ConfigParser()
        self.init()
        self.cfg.read(CFG_PATH)

    def init(self):
        """
        判断参数配置文件是否存在，不存在则新增
        :return:
        """
        if not os.path.exists(CFG_PATH):
            with open(CFG_PATH, 'w+') as f:
                self.cfg.read_dict(ATTR)
                self.cfg.write(f)
        else:
            self.cfg.read(CFG_PATH)
            sections = self.cfg.sections()
            for key, value in ATTR.items():
                if key not in sections:
                    self.cfg[key] = value
                else:
                    options = self.cfg[key]
                    for k, v in value.items():
                        if k not in options:
                            self.cfg[key][k] = v
            with open(CFG_PATH, 'w+') as f:
                self.cfg.write(f)

    def upd(self, arg):
        """
        更新配置文件内容
        :param arg: e.g. [['a','b','c'],['a','d','e']] 'a'表示sections，'b'/'d' 表示option 'c'/'e'表示值
        :return:
        """
        with open(CFG_PATH, 'w+') as f:
            for a in arg:
                self.cfg.set(a[0], a[1], a[2])
            self.cfg.write(f)

    def get_value(self, sec, opt):
        a = self.cfg.get(sec, opt)
        return a

    def __getitem__(self, key):
        """

        :param key:
        :return:
        """
        try:
            return self.cfg[key]
        except KeyError:
            raise SettingException(key)


if __name__ == '__main__':
    '''
    sett = Setting()
    cfg = ConfigParser()
    cfg.read(CFG_PATH)
    print sett['JIRA_INFO']['jira_pwt']
    '''
    case_dir= r'D:\pyproject\git\hgbox\hgBox'
    files = [f for f in os.listdir(case_dir) if os.path.isfile(os.path.join(case_dir,f))] #and f.split('.')[1] in ('py', 'xlsx'))]

    print files
