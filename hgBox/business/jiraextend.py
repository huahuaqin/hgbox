# -*- coding:utf-8 -*-

from jira import JIRA,exceptions
import os
import configparser
import xlrd
from execptions import JiraException


class JiraExtend(object):
    """

    """
    def __init__(self, *args, **kw):
        self._cfg_file = 'config.ini'
        self._user = self.cfg_parser('JIRA_INFO', 'jira_user')
        self._password = self.cfg_parser('JIRA_INFO', 'jira_pwd')
        self._jira_server = self.cfg_parser('JIRA_INFO', 'jira_server')
        self._jira_prj = self.cfg_parser('JIRA_INFO', 'jira_prj')
        self._jira = self.login_jira()

    def login_jira(self):
        """

        :return:
        """
        try:
            return JIRA(self._jira_server, basic_auth=(self._user, self._password), max_retries=0, timeout=1)
        except Exception, e:
            raise JiraException(e)

    def cfg_parser(self, section, option, cfg_file=None):
        """
        获取配置文件中内容
        :param section:
        :param option:
        :param cfg_file:
        :return:
        """
        cfg_file = self._cfg_file if(cfg_file is None) else cfg_file
        if not os.path.exists(cfg_file):
            raise Exception
        cfg_handle = configparser.ConfigParser()
        cfg_handle.read(cfg_file)
        return cfg_handle.get(section, option)

    def check_case_coverage(self, version, case_dir):
        """
        检查用例覆盖情况
        :return:
        """
        jirakeys = []
        testcasejiras = []
        uncoverjiras = []
        result = ''

        # 获取具体版本下的jira号
        content = self._jira.search_issues('project = OTC AND issuetype = Story AND fixVersion = '+version+''.decode('gbk'),maxResults=200)
        for issue in content:
            jirakeys.append([issue.key, issue.fields.subtasks])

        # 获取目录下excel用例中的jira号，只支持最新标准的用例模板
        files = os.listdir(case_dir)
        jiracol = 1
        for f in files:
            data = xlrd.open_workbook(case_dir +'\\'+f)
            sheet_count = len(data.sheets())
            for sheet,i in zip(data.sheets(),range(sheet_count)):
                table = data.sheets()[i]
                nrows = table.nrows
                for row in range(nrows):
                    if row == 0:
                        for cl in range(table.ncols):
                            if table.cell(row, cl).value == u'需求编号':
                                jiracol = cl

                    cell_value = table.cell(row, jiracol).value
                    if cell_value not in testcasejiras:
                        testcasejiras.append(cell_value)

        # 检查没有用例覆盖的需求号
        for jirakey in jirakeys:
            num = 0
            for testcasejira in testcasejiras:
                if jirakey[0] in testcasejira:
                    num = 1
                    break
            if num == 0:
                uncoverjiras.append(jirakey)

        # 输出结果
        if len(uncoverjiras) > 0:
            result = u'测试用例未覆盖的需求数：' + str(len(uncoverjiras))+u'\r\n 测试用例未覆盖的jira如下：\r\n'
            # print u'测试用例未覆盖的jira如下：'
            for uncoverjira in uncoverjiras:
                testers = ''
                for subtask in uncoverjira[1]:
                    subcontent = self._jira.search_issues('project = OTC AND key = ' + str(subtask))
                    for subissue in subcontent:
                        if 'Test' in str(subissue.fields.customfield_10211):
                            if str(subissue.fields.assignee) not in testers:
                                testers = testers + ' ' + str(subissue.fields.assignee)
                    # print uncoverjira[0] + testers
                    result = result+(uncoverjira[0] + ' '+testers+'\r\n')
        else:
            # print u'\n测试用例已全部覆盖jira需求'
            result = u'测试用例已全部覆盖jira需求'

        # raw_input('')
        return result

    def sync_sub_pjoect(self):
        """
        检查子任务的版本号是否和主任务的一致，如果不一致则修改
        :return:
        """
        content = self._jira.search_issues('project = OTC AND issuetype = Story AND fixVersion = '+self._version+''.decode('gbk'),maxResults=200)
        for issue in content:
            # print issue.key
            for sub_task in issue.fields.subtasks:
                subcontent = self._jira.search_issues('project = OTC AND issue = ' + str(sub_task))
                sub_task_ver = subcontent[0].fields.fixVersions[0].name
                if sub_task_ver != self._version:
                    print subcontent[0].key

    def version_exist(self, version, project=None):
        prj = self._jira_prj if project is None else project
        vers = self._jira.project_versions(prj)
        return version in [v.name for v in vers]

if __name__ == '__main__':
    jre = JiraExtend()
    jre.sync_sub_pjoect()
