# -*- coding:utf-8 -*-

from threading import Thread
import os
import wx
from basepanel import BasePanel
from business import *
from lib.osextend import lst_all_file
from lib import wrap_wx_msg_exception as wrap_exception


class PanelRF(BasePanel):
    '''
    RF 用例相关
    '''
    def __init__(self, parent):
        BasePanel.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        """
        界面布局初始化
        :return:
        """
        # 用例目录,提供路径选择框
        self.label_case_path = wx.StaticText(self, -1, label=u'用例目录', pos=(10, 10))
        self.in_path = wx.TextCtrl(self, -1, size=(400, -1), pos=(100, 10))
        # 文件夹选择框按钮
        self.btn_select_dir = wx.Button(self, -1, size=(20, -1), label=u'..', pos=(500, 10))
        self.Bind(wx.EVT_BUTTON, self.on_btn_select_dir, self.btn_select_dir)

        # 查找目标
        self.label_search = wx.StaticText(self, -1, label=u'查找目标', pos=(10, 40))
        self.in_search = wx.TextCtrl(self, -1, size=(400, -1), pos=(100, 40))

        # 替换内容
        self.label_replace = wx.StaticText(self, -1, label=u'替换内容', pos=(10, 70))
        self.in_replace = wx.TextCtrl(self, -1, size=(400, -1), pos=(100, 70))

        # 查找
        self.btn_search = wx.Button(self, -1, label=u'查找', pos=(100, 100))
        self.Bind(wx.EVT_BUTTON, self.on_btn_search, self.btn_search)

        # 替换
        self.btn_replace = wx.Button(self, -1, label=u'替换', pos=(200, 100))
        self.Bind(wx.EVT_BUTTON, self.on_btn_replace, self.btn_replace)

        # 树形结构
        self.tree,self.img_list = self._init_tree(self, pos=(10, 130), size=(570, 400), )

        self.btns = [self.btn_search,self.btn_replace]

    def on_btn_search(self, event):
        """

        :param event:
        :return:
        """
        # 先把按钮该页面的按钮置灰,
        self._disable_btn()
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self._search_or_replace, args=())
        t.start()

    def on_btn_replace(self, event):
        """

        :param event:
        :return:
        """
        # 先把按钮该页面的按钮置灰,
        self._disable_btn()
        # 使用线程调用(非阻塞)，避免处理时间过长导致界面卡死
        t = Thread(target=self._search_or_replace, args=((True,)))
        t.start()

    @wrap_exception
    def _search_or_replace(self,flag=False):
        """

        :return:
        """
        search_contxt = self.in_search.GetValue()
        replace_context = self.in_replace.GetValue()
        case_path = self.in_path.GetValue()
        if not os.path.isdir(case_path):
            raise Exception('用例目录无效')
        rf = RFExtend()
        root = self.tree.GetRootItem()
        if root:
            self.tree.Delete(root)
        root = self.tree.AddRoot(case_path, image=0)
        tree_node = rf.lst_tree_node(case_path)

        if flag:
            if not search_contxt.strip(' '):
                raise Exception('请输入要查找的内容!')
            if not replace_context.strip(' '):
                raise Exception('请输入要替换的内容!')
            self._upd_tree(root, tree_node,case_path,search_contxt,True)
            for f in lst_all_file(case_path):
                rf.search_or_replace_content(f,search_contxt,replace_context)
        else:
            if search_contxt.strip(' '):
                self._upd_tree(root, tree_node,case_path,search_contxt)
            else:
                self._upd_tree(root, tree_node)
        self._enable_btn()

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

    def _init_tree(self, parent, *args, **kwargs):
        """
        创建目录树形结构
        :param parent:
        :param root_name
        :return:
        """
        tree = wx.TreeCtrl(parent, *args, **kwargs)
        # 通过wx.ImageList()创建一个图像列表imglist并保存在树中
        img_list = wx.ImageList(16, 16, True, 2)
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER, size=wx.Size(16, 16)))
        img_list.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, size=(16, 16)))
        tree.AssignImageList(img_list)
        # root = tree.AddRoot(root_name, image=0)
        return tree, img_list

    def _upd_tree(self, node, item_list,main_path=None,search='',flag=False):
        """

        :param node:
        :param item_list:
        :return:
        """
        total_cnt=0
        if not isinstance(item_list, (list, tuple)):
            raise ValueError('入参[item_list]必须是列表')
        if not isinstance(node, wx.TreeItemId):
            raise ValueError('入参[node]必须是tree_node')

        for item in item_list:
            if isinstance(item, dict):
                for key, value in item.items():
                    node_name=key.split('\\')[-1]
                    child_node = self.tree.AppendItem(node, node_name, 0)
                    if isinstance(value, (list, tuple)):
                        cnt =self._upd_tree(child_node, value,key,search,flag)
                        total_cnt+=cnt
            elif isinstance(item, basestring):
                if isinstance(item, basestring):
                    if search !='':
                        path = os.path.join(main_path,item)
                        cnt = RFExtend.search_or_replace_content(path,search,)
                        item = '%s  (%s)' % (item,cnt)
                        total_cnt+=cnt
                self.tree.AppendItem(node, item, 1)
        if search !='':
            node_name='%s  (%s)' % (self.tree.GetItemText(node),total_cnt)
            self.tree.SetItemText(node,node_name)
        return total_cnt
