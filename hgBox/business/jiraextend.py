# -*- coding:utf-8 -*-

from jira import JIRA
import os
import configparser
import xlrd
from execptions import JiraException
from setting import Setting


class JiraExtend(object):
    """

    """
    def __init__(self, *args, **kw):
        self._sett = Setting()
        self._user = self._sett['JIRA_INFO']['jira_user']
        self._password = self._sett['JIRA_INFO']['jira_pwd']
        self._jira_server = self._sett['JIRA_INFO']['jira_server']
        self._jira_prj = self._sett['JIRA_INFO']['jira_prj']
        self._jira = self.login_jira()

    def login_jira(self):
        """

        :return:
        """
        try:
            return JIRA(self._jira_server, basic_auth=(self._user, self._password), max_retries=0, timeout=2)
        except Exception, e:
            raise JiraException(e)

    def check_case_coverage(self, version, case_dir):
        """
        检查用例覆盖情况
        :return:
        """
        testcasejiras = []
        uncoverjiras = []
        result = ''

        # 获取具体版本下的jira号
        story_issues = self.version_related_story_issue(self._jira_prj, version)
        '''
        for issue in content:
            jirakeys.append([issue.key, issue.fields.subtasks])
        '''
        jirakeys = ([issue.key, issue.fields.subtasks] for issue in story_issues)

        # 获取目录下excel用例中的jira号，只支持最新标准的用例模板
        files = [f for f in os.listdir(case_dir) if \
                 (os.path.isfile(os.path.join(case_dir, f)) and f.split('.')[1] in ('xls', 'xlsx'))]
        '''
        files = [os.path.join(root, f) for(root, dir, files) in os.walk(case_dir) \
                 for f in files if f.split('.')[1] in ('xls', 'xlsx')]
        '''
        for f in files:
            data = xlrd.open_workbook(f)  # (case_dir +'\\'+f)
            sheets = data.sheets()
            for sheet in sheets:
                table = sheet
                nrows = table.nrows
                # 从第一行的名称获取'需求编号'所在的列
                for cl in range(table.ncols):
                    if table.cell(0, cl).value == u'需求编号':
                        jiracol = cl
                        break
                else:
                    continue
                for row in range(1, nrows):
                    cell_value = table.cell(row, jiracol).value
                    if cell_value not in testcasejiras:
                        testcasejiras.append(cell_value)

        # 检查没有用例覆盖的需求号
        for jirakey in jirakeys:
            for testcasejira in testcasejiras:
                if jirakey[0] in testcasejira:
                    break
            else:
                uncoverjiras.append(jirakey)

        # 输出结果
        if len(uncoverjiras) > 0:
            result = u'测试用例未覆盖的需求数:%d\r\n 测试用例未覆盖的jira如下：\r\n' %len(uncoverjiras)
            for uncoverjira in uncoverjiras:
                testers = ''
                for subtask in uncoverjira[1]:
                    subcontent = self._jira.search_issues('project=%s AND key=%s' % (self._jira_prj, str(subtask)))
                    for subissue in subcontent:
                        if 'Test' in str(subissue.fields.customfield_10211):
                            if str(subissue.fields.assignee) not in testers:
                                testers = testers + ' ' + str(subissue.fields.assignee)
                result = result+(uncoverjira[0] + ' '+testers+'\r\n')
        else:
            result = u'测试用例已全部覆盖jira需求'

        return result

    def sub_task_sync_version(self, version):
        """
        检查子任务的版本号是否和主任务的一致，(如果不一致则修改)
        :return:
        """
        # 获取版本下的所有Story类型的issue
        ret_list = []
        story_issues = self.version_related_story_issue(self._jira_prj, version)

        for issue in story_issues:
            for sub_task in issue.fields.subtasks:
                sub_content = self._jira.search_issues('project=%s AND issue=%s' % (self._jira_prj, str(sub_task)))
                sub_task_ver = sub_content[0].fields.fixVersions[0].name
                if sub_task_ver != version:
                    ret_list.append(issue)
        return ret_list

    def version_exist(self, version, project=None):
        prj = self._jira_prj if project is None else project
        vers = self._jira.project_versions(prj)
        return version in [v.name for v in vers]

    def version_related_story_issue(self, project, version):
        """
        获取版本下的所有Story类型的
        :param project:
        :param version:
        :return:
        """
        return self._jira.search_issues('project = %s AND issuetype = Story AND fixVersion =%s ' % (project, version),\
                                        maxResults=200)

if __name__ == '__main__':
    jre = JiraExtend()
    jre.sync_sub_pjoect()
