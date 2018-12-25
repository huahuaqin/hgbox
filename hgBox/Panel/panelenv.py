# -*- coding:utf-8 -*-

from threading import Thread
# import os
import wx
from basepanel import BasePanel
from business import *
from lib import wrap_wx_msg_exception as wrap_exception
from lib.ftpextend import FtpExtend
from business import Setting
from time import sleep


class PanelEnv(BasePanel):
    '''
    RF 用例相关
    '''
    def __init__(self, parent):
        BasePanel.__init__(self, parent)
        self._default_setting = Setting()
        self.init_ui()
        self.env = EnvManage()

    def init_ui(self):
        """
        界面布局初始化
        :return:
        """
        self.label_ftp_server = wx.StaticText(self, -1, label=u'FTP地址:', pos=(10, 10))
        self.in_ftp_server = wx.TextCtrl(self, -1, size=(120, -1), pos=(60, 10),\
                                         value=self._default_setting['FTP_INFO']['ftp_server'])
        self.label_ftp_port = wx.StaticText(self, -1, label=u'端口:', pos=(190, 10))
        self.in_ftp_port = wx.TextCtrl(self, -1, size=(40, -1), pos=(220, 10),\
                                       value=self._default_setting['FTP_INFO']['port'])
        # FTP 用户名密码
        self.label_ftp_user = wx.StaticText(self, -1, label=u'用户:', pos=(270, 10))
        self.in_ftp_user = wx.TextCtrl(self, -1, size=(100, -1), pos=(300, 10),\
                                       value=self._default_setting['FTP_INFO']['ftp_user'])
        self.label_ftp_passwd = wx.StaticText(self, -1, label=u'密码:', pos=(410, 10))
        self.in_ftp_passwd = wx.TextCtrl(self, -1, size=(100, -1), pos=(440, 10),\
                                         value=self._default_setting['FTP_INFO']['ftp_passwd'])
        # ftp 连接测试
        self.btn_connect = wx.Button(self, -1, label=u'连接', pos=(540,10),size=(40, 25))
        self.Bind(wx.EVT_BUTTON, self.on_btn_connect, self.btn_connect)

        #数据库信息
        self.label_db_name = wx.StaticText(self, -1, label=u'数据库:', pos=(10, 40))
        self.in_db_name = wx.TextCtrl(self, -1, size=(120, -1), pos=(60, 40),value='otc_138')
        self.label_db_user = wx.StaticText(self, -1, label=u'用户:', pos=(190, 40))
        self.in_db_user = wx.TextCtrl(self, -1, size=(100, -1), pos=(220, 40),value='otcts')
        self.label_db_passwd = wx.StaticText(self, -1, label=u'密码:', pos=(330, 40))
        self.in_db_passwd = wx.TextCtrl(self, -1, size=(100, -1), pos=(360, 40),value='otcts')
        # 版本
        self.label_ver = wx.StaticText(self, -1, label=u'版本:', pos=(10, 70))
        self.in_ver = wx.TextCtrl(self, -1, size=(290, -1), pos=(60, 70))
        #子系统
        subsys_list=['报价','清算',]
        self.label_subsys = wx.StaticText(self, -1, label=u'子系统:', pos=(360, 70))
        self.in_subsys = wx.Choice(self,-1,size=(60, -1),pos=(400, 70),choices=subsys_list,)

        # 升级包目录,提供路径选择框
        self.label_pack_path = wx.StaticText(self, -1, label=u'升级包路径', pos=(0, 100))
        self.in_path = wx.TextCtrl(self, -1, size=(400, -1), pos=(60, 100))
        # 文件夹选择框按钮
        self.btn_select_dir = wx.Button(self, -1, size=(20, -1), label=u'..', pos=(470, 100))
        self.Bind(wx.EVT_BUTTON, self.on_btn_select_dir, self.btn_select_dir)

        # 备份
        self.btn_backup = wx.Button(self, -1, label=u'备份', pos=(100, 130))
        self.Bind(wx.EVT_BUTTON, self.on_btn_backup, self.btn_backup)

        # 升级
        self.btn_replace = wx.Button(self, -1, label=u'升级', pos=(200, 130))
        #self.Bind(wx.EVT_BUTTON, self.on_btn_replace, self.btn_replace)

        # 树形结构
        self._init_tree(self, pos=(10, 160), size=(200, 370), )
        # 结果展示
        self.txt_result = wx.TextCtrl(self, -1, size=(370, 370), pos=(210, 160), style=wx.TE_MULTILINE)

        self.btns = [self.btn_backup, self.btn_replace,self.btn_connect,self.btn_select_dir]

    def _init_tree(self, parent, *args, **kwargs):
        """
        创建目录树形结构
        :param parent:
        :param root_name
        :return:
        """
        self.tree = wx.TreeCtrl(parent, *args, **kwargs)
        # host,port,user,passwd = self._get_value([self.in_ftp_server,self.in_ftp_port,self.in_ftp_user,self.in_ftp_passwd])
        # 通过wx.ImageList()创建一个图像列表imglist并保存在树中
        img_list = wx.ImageList(16, 16, True, 2)
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        self.tree.AssignImageList(img_list)
        self.root = self.tree.AddRoot('/', image=0)
        '''
        if host and user and passwd and port:
            try:
                self.fe = FtpExtend(host, user, passwd, port)
                item_list = self.fe.lst_all_node()
                self._upd_tree(self.root, item_list)
            except:
                raise Exception
        '''

    def _upd_tree(self, node, item_list,main_path=None):
        """

        :param node:
        :param item_list:
        :return:
        """
        if not isinstance(item_list, (list, tuple)):
            raise ValueError('入参[item_list]必须是列表')
        if not isinstance(node, wx.TreeItemId):
            raise ValueError('入参[node]必须是tree_node')

        for item in item_list:
            if isinstance(item, dict):
                for key, value in item.items():
                    node_name=key.split('\\')[-1]
                    child_node = self.tree.AppendItem(node, node_name.decode('gbk'), 0)
                    if isinstance(value, (list, tuple)):
                        self._upd_tree(child_node, value,)
            elif isinstance(item, basestring):
                self.tree.AppendItem(node, item.decode('gbk'), 1)

    def on_btn_connect(self,event):
        """

        :param event:
        :return:
        """
        self._disable_btn()
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self._connect, args=())
        t.start()

    def on_btn_backup(self, event):
        """

        :param event:
        :return:
        """
        # 先把按钮该页面的按钮置灰,
        self._disable_btn()
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self._backup, args=())
        t1 = Thread(target=self._backup_msg,args=())
        t.start()
        t1.start()

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

    @wrap_exception
    def _backup(self):
        """

        :return:
        """
        host,port,user,passwd = self._get_value([self.in_ftp_server,self.in_ftp_port,self.in_ftp_user,self.in_ftp_passwd])
        db_name,db_user,db_passwd = self._get_value([self.in_db_name,self.in_db_user,self.in_db_passwd])
        version,pack_path = self._get_value([self.in_ver,self.in_path])
        subsys = self.in_subsys.GetString(self.in_subsys.GetCurrentSelection())
        for i in (db_name, db_user, db_passwd, version, pack_path, subsys):
            if not i:
                raise Exception('入参不能为空')
        self.env.backup((db_user,db_passwd,db_name),version,subsys,pack_path,(host,user,passwd,port))
        self._enable_btn()

    def _backup_msg(self):
        """

        :return:
        """
        self.txt_result.SetValue('')
        while 1:
            try:
                msg = self.env.q.get()
                self.txt_result.AppendText(msg.encode('utf-8'))
                sleep(0.1)
            except:
                raise

    @wrap_exception
    def _connect(self):
        """

        :return:
        """
        host, port, user, passwd = self._get_value([self.in_ftp_server,self.in_ftp_port,self.in_ftp_user,self.in_ftp_passwd])
        if not (host and user and passwd and port):
            raise Exception('FTP 服务器地址/端口/用户名/密码 不能为空')
        else:
            self.fe = FtpExtend(host, user, passwd, port)
            item_list = self.fe.lst_all_node()
            self.tree.DeleteChildren(self.root)
            self._upd_tree(self.root, item_list)
            self._enable_btn()
            wx.MessageDialog(self, u'登陆成功', style=wx.OK | wx.ICON_INFORMATION).ShowModal()