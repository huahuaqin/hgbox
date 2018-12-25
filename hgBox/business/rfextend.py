# -*- coding:utf-8 -*-

import os
import re
from lib.wrap import timer
from lib.osextend import is_contain_chinese


class RFExtend(object):
    """

    """
    def __init__(self):
        # self._path=path
        self._tree_node=[]

    def lst_tree_node(self,path):
        """
        构造树形结构节点数据
        :param path:
        :return:
        """
        if not os.path.isdir(path):
            raise Exception('用例目录无效')
        tree_node=[]

        for main_path,sub_dir,file_name_list in os.walk(path):
            if '.svn' in main_path:
                continue
            if sub_dir != []:
                for sd in sub_dir:
                    if '.svn' == sd:
                        continue
                    sub_tree_node=self.lst_tree_node(os.path.join(main_path,sd))
                    tree_node.append({os.path.join(main_path,sd):sub_tree_node})
            tree_node.extend(file_name_list)
            return tree_node

    @staticmethod
    @timer
    def search_or_replace_content(path,src,rep=None):
        """

        :return:
        """
        if not os.path.isfile(path):
            raise ValueError('不是文件')

        with open(path, 'r') as f:
            content = f.read()
            if len(content) == 0:
                return 0
            in_str = src+rep if rep else src
            if is_contain_chinese(in_str):
                try:
                    content.decode('UTF-8')
                    src = src.encode('UTF-8')
                    if rep:
                        rep = rep.encode('UTF-8')
                except:
                    try:
                        src = src.encode('gbk')
                        if rep:
                            rep = rep.encode('gbk')
                    except:
                        pass

            '''
            try:
                content.decode('UTF-8')
                src = src.encode('UTF-8')
                if rep:
                    rep = rep.encode('UTF-8')
            except:
                try:
                    src = src.encode('gbk')
                    if rep:
                        rep = rep.encode('gbk')
                except:
                    pass
            '''

            pattern = re.compile(src)
            ret = pattern.findall(content)
        if rep and (src in content):
            content = re.sub(src, rep, content)
            # content = content.replace(src,rep)
            with open(path, 'w+') as f:
                f.write(content)
        return len(ret)


if __name__ == '__main__':
    path=u'E:\\SVN\\NewAutoTest\\PKG_OTCTS_V1.0.6.1 - 副本\\交易类业务\\开放式基金迁移\\基金预约认申购.txt'
    rfe = RFExtend()
    a=rfe.search_or_replace_content(path,u'预约认申赎委托表',u'秦华根测试')
    print a
