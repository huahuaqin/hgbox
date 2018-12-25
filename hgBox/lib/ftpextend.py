# -*- coding:utf-8 -*-

from ftplib import FTP
import os


class FtpExtend(FTP):
    """

    """
    def __init__(self,host,user,passwd,port=21,timeout=10):
        """

        :param ftp_server:
        :param user:
        :param pwd:
        :param port:
        :return:
        """
        FTP.__init__(self)
        self.host=host
        self.user=user
        self.passwd=passwd
        self.port=str(port)
        self.timeout = timeout
        # self.ftp =FTP()
        self._login()

    def _login(self):
        """

        :return:
        """
        self.connect(self.host,self.port,self.timeout)
        self.login(self.user,self.passwd)

    def lst_all_node(self, main_path='/'):
        """

        :param main_path:
        :return:
        """
        all_node = []
        node_list = []
        self.dir(main_path, node_list.append)
        for node in node_list:
            node_name = node.split()[3]
            if node.split()[2] == '<DIR>':
                # pwd = self.ftp.pwd()
                sub_dir_path = '%s/%s' % (main_path, node_name)
                nodes = self.lst_all_node(sub_dir_path)
                all_node.append({node_name: nodes})
            else:
                all_node.append(node_name)
        return all_node

    def upload_file(self, local_file, remote_file):
        """

        :param local_file:
        :param remote_file:
        :return:
        """
        if not os.path.isfile(local_file):
            raise Exception('本地路径[%s]不存在'%local_file)
        buf_size = 1024
        with open(local_file,'rb') as f:
            self.storbinary('STOR %s' % remote_file,f, buf_size)

    def upload_file_tree(self, local_path, remote_path):
        """

        :param local_path:
        :param remote_path:
        :return:
        """
        if not os.path.isdir(local_path):
            raise Exception('本地路径[%s]不存在'%local_path)
        if not self.dir_exist(remote_path):
            raise Exception('ftp目录[%s]不存在' %remote_path)

        self.cwd(remote_path)

        local_name_list = os.listdir(local_path)
        for local_name in local_name_list:
            src = os.path.join(local_path, local_name)
            if os.path.isdir(src):
                try:
                    self.mkd(local_name)
                except Exception as err:
                    raise Exception("目录已存在 %s ,具体错误描述为：%s" % (local_name, err))
                self.upload_file_tree(src, local_name)
            else:
                self.upload_file(src, local_name)
        self.cwd("..")

    def dir_exist(self,path):
        """
        判断ftp目录是否存在
        :param path:
        :return:
        """
        try:
            cur_path=self.pwd()
            self.cwd(path)
            self.cwd(cur_path)
            return True
        except:
            return False

if __name__== '__main__':
    host= '192.168.0.106'
    user = 'qhg'
    passwd = 'huahuaqin'
    fe = FtpExtend(host,user,passwd)
    # print fe.lst_all_node()
    fe.upload_file(u'D:\\pyproject\\git\\hgbox\\hgBox\\htyJLAVUa\\234\\q.txt',u'/abc/q.txt')

