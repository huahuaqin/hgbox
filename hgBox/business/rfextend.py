# -*- coding:utf-8 -*-

import os
import re
import chardet


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
            tree_node.extend(file_name_list)
            if sub_dir != []:
                for sd in sub_dir:
                    if '.svn' == sd:
                        continue
                    sub_tree_node=self.lst_tree_node(os.path.join(main_path,sd))
                    tree_node.append({os.path.join(main_path,sd):sub_tree_node})
            return tree_node

    @staticmethod
    def search_or_replace_content(path,src,rep=None):
        """

        :return:
        """
        flag=False
        if not os.path.isfile(path):
            raise ValueError('不是文件')

        pattern = re.compile(src)
        with open(path, 'r') as f:
            content = f.read()
            '''
            try:
                content = content.decode('gbk')
                flag = True
            except:
                pass
                ch = chardet.detect(content)
                if ch['confidence'] == 1.0:
                    content = content.decode(ch['encoding'])
                else:
                    pass
                '''

            ret = pattern.findall(content)
        if rep and ret:
            content = re.sub(src, rep, content)
            # content = content.replace(src,rep)
            with open(path, 'r+') as f:
                f.write(content)
        return len(ret)


if __name__ == '__main__':
    path=r'E:\SVN\NewAutoTest\PKG_OTCTS_V1.0.6.1\fee_init.sql'
    rfe = RFExtend()
    a=rfe.search_or_replace_content(path,'OTC_FEE_TMPL')
    print a
