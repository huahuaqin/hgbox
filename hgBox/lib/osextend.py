# -*- coding:utf-8 -*-

import os
import re
from lib.wrap import timer
import subprocess
from time import sleep
import zipfile


def lst_all_file(dir_path=None, postfix=()):
        """
        获取某个目录下的所有文件路径,包含子文件夹下的；
        :param dir_path: 文件夹路径;
        :param postfix: 文件类型; list or set ,('txt','sql')
        :return: list
        """
        all_file_path = []
        if not os.path.exists(dir_path):
            raise Exception
        for main_path, sub_dir, file_name_list in os.walk(dir_path):
            if '.svn' in main_path:
                continue
            for file_name in file_name_list:
                file_path = os.path.join(main_path, file_name)
                file_postfix = file_path.split('.')[-1]
                if postfix and file_postfix not in postfix:
                    continue
                all_file_path.append(file_path)
        return all_file_path


def is_contain_chinese(in_str):
    """
    检查字符串中是否有中文
    :param in_str:
    :return:
    """
    if re.findall(ur'[\u4e00-\u9fa5]+',in_str):
        return True
    return False


def run_cmd(cmd,timeout=60):
    """
    执行cmd命令
    :param cmd:
    :param timeout:
    :return:
    """
    obj = subprocess.Popen(cmd.encode('gbk'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while obj.returncode is None:
        obj.poll()
        yield [None,obj.stdout.readline()]

    yield [obj.returncode,u'执行结束']


@timer
def zip_f(zip_path, src_path):
        """
        压缩成zip文件
        :param zip_path: 压缩后的文件路径
        :param src_path: 要压缩的文件夹/文件
        :return:
        """
        if os.path.isfile(src_path):
            with zipfile.ZipFile(zip_path,'w', zipfile.ZIP_DEFLATED) as zp:
                zp.write(src_path)
        elif os.path.isdir(src_path):
            file_list = lst_all_file(src_path)
            with zipfile.ZipFile(zip_path,'w', zipfile.ZIP_DEFLATED) as zp:
                for f in file_list:
                    # print f
                    zp.write(f,f.split(src_path)[-1])
        else:
            raise Exception('压缩路径错误')



if __name__ == '__main__':
    import re
    import subprocess
    path = u'E:\\SVN\\Package\\OTC1.0.5.6_中信建投_4\\5.PKG_OTCITF_V1.0.5.6_中信建投_4\\OTCMC\\bin\\add_kdfcfs_newcfg(需要修改).xml'
    #out = subprocess.call(path.encode('gbk'), shell=True)
    out=re.findall(ur'[\u4e00-\u9fa5]+',path)
    print out
