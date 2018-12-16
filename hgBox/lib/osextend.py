# -*- coding:utf-8 -*-

import os


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
