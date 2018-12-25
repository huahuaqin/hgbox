# -*- coding:utf-8 -*-

import os
from ftplib import FTP
import random,string
import shutil
from lib.osextend import zip_f, run_cmd
from lib.wrap import timer
from lib.ftpextend import FtpExtend
from multiprocessing import Queue


class EnvManage(object):
    """

    """
    def __init__(self):
        """

        :return:
        """
        self.q = Queue()
        pass

    def exp_db(self, db_info, des_path):
        """

        :param db_info: 数据库信息 tuple (数据库实例,用户名,密码)i.e (orcl,otcts,otcts)
        :param des_path:
        :return:
        """
        if len(db_info) != 3:
            raise Exception('db_info 参数个数错误')
        if not (os.path.isfile(des_path) and des_path.endswith('.dmp')):
            Exception('导出路径错误')
        # exp_file_name = os.path.join(des_path, 'tmp.dmp')
        exp_cmd = 'exp %s/%s@%s file=%s' % (db_info[0],db_info[1],db_info[2],des_path)
        self.q.put(u'---------------开始执行数据库备份:---------------\n')
        for ret_code, sout in run_cmd(exp_cmd, 600):
            if ret_code is None and sout:
                self.q.put(sout)

    def backup(self, db_info, version, subsys, pack_path, ftp_info):
        """

        :param db_info:
        :param version:
        :param subsys:
        :param pack_path:
        :param ftp_info:
        :return:
        """
        # 创建临时文件夹
        cur_path = os.getcwd()
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        tmp_dir = os.path.join(cur_path, random_str[:-1])
        ver_path = os.path.join(tmp_dir, version)
        subsys_path = os.path.join(ver_path, subsys)
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        os.makedirs(tmp_dir)
        os.makedirs(ver_path)
        os.makedirs(subsys_path)

        # 数据库导出
        dmp_name = '%s_%s.dmp' % (version, subsys)
        self.exp_db(db_info,os.path.join(subsys_path, dmp_name))
        # 升级包复制
        self.q.put(u'\n---------------拷贝升级包:------------------\n')
        shutil.copytree(pack_path, os.path.join(subsys_path,'%s_%s' % (version,subsys)))
        # 压缩打包
        zip_name = '%s_%s.zip' % (version, subsys)
        zip_path = os.path.join(ver_path, zip_name)
        self.q.put(u'\n---------------压缩文件:------------------\n')
        zip_f(zip_path, subsys_path)
        '''
        # 上传ftp
        fe = FtpExtend(ftp_info[0],ftp_info[1],ftp_info[2],ftp_info[3])
        upload_dir = '/%s'%version
        if not fe.dir_exist(upload_dir):
            fe.mkd(upload_dir)
        fe.cwd(upload_dir)
        fe.upload_file(zip_path,zip_name.encode('gbk'))
        '''

if __name__ == '__main__':
        env = EnvManage()
        env.exp_db(('123','123','123'),u'F:\\')
        # print ftp.pwd()