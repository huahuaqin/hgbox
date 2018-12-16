# -*- coding:utf-8 -*-

from jira import JIRA
import os
import xlrd
from execptions import JiraException
from setting import Setting


def wrap_exception(func):
    """
    装饰器，异常时统一由JiraException 类处理
    :param func:
    :return:
    """
    def wrapper(self, *arg, **kw):
        try:
            return func(self, *arg, **kw)
        except Exception,e:
            raise JiraException(e)
    return wrapper


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
            if not (self._jira_server and self._user and self._password and self._jira_prj):
                raise JiraException(str('jira 参数信息不全，请先进行参数设置并进行验证'))
            return JIRA(self._jira_server, basic_auth=(self._user, self._password), max_retries=0, timeout=2)
        except Exception, e:
            raise JiraException(e)

    def check_case_coverage(self, version, case_dir):
        """
        检查用例覆盖情况
        :return:
        """
        uncoverjiras = self.jira_uncover_case(version, case_dir, u'需求编号')

        # 输出结果
        if len(uncoverjiras) > 0:
            result = u'测试用例未覆盖的需求数:%d\r\n测试用例未覆盖的jira如下：\r\n' %len(uncoverjiras)
            for uncoverjira in uncoverjiras:
                testers = u''
                for subtask in uncoverjira[1]:
                    subcontent = self._jira.search_issues('project=%s AND key=%s' % (self._jira_prj, str(subtask)))
                    for subissue in subcontent:
                        if u'Test' in subissue.fields.customfield_10211.value:
                            if subissue.fields.assignee.key not in testers:
                                testers = '%s %s' % (testers, subissue.fields.assignee.key)
                result = '%s%s %s\r\n' % (result, uncoverjira[0], testers)
                # print result
        else:
            result = u'测试用例已全部覆盖jira需求'
        return result

    def check_unit_case_coverage(self, version, case_dir):
        """
        检查开发单元测试用例
        :param version:
        :param case_dir:
        :return:
        """
        uncoverjiras = self.jira_uncover_case(version, case_dir, u'JIRA号')

        # 输出结果
        if len(uncoverjiras) > 0:
            result = u'单元测试用例未覆盖的需求数:%d\r\n未覆盖的jira如下：\r\n' %len(uncoverjiras)
            for uncoverjira in uncoverjiras:
                testers = u''
                for subtask in uncoverjira[1]:
                    subcontent = self._jira.search_issues('project=%s AND key=%s' % (self._jira_prj, str(subtask)))
                    for subissue in subcontent:
                        if u'Development' in subissue.fields.customfield_10211.value:
                            if subissue.fields.assignee.key not in testers:
                                testers = '%s %s' % (testers, subissue.fields.assignee.key)
                result = '%s%s %s\r\n' % (result, uncoverjira[0], testers)
        else:
            result = u'单元测试已全部覆盖jira需求'
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
            if not issue.fields.subtasks:
                ret_list.append(issue)
            for sub_task in issue.fields.subtasks:
                try:
                    sub_content = self._jira.search_issues('project=%s AND issue=%s' % (self._jira_prj, str(sub_task)))
                    sub_task_ver = sub_content[0].fields.fixVersions
                    if version not in [stv.name for stv in sub_task_ver]:
                        ret_list.append(issue)
                except Exception, e:
                    raise Exception('jira[%s]-subtask[%s]：%s' % (str(issue.key), str(sub_task.key),str(e)))
        return [i for i in set(ret_list)]

    @wrap_exception
    def version_exist(self, version, project=None):
        """
        检查某个项目下是否存在特定版本
        :param version:
        :param project:
        :return:
        """
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

    def jira_uncover_case(self, version, case_dir, col_name):
        """
        获取版本下没有测试用例的所有jira
        :param version:
        :param case_dir:
        :param col_name:
        :return:
        """
        testcasejiras = []
        uncoverjiras = []

        # 获取具体版本下的jira号
        story_issues = self.version_related_story_issue(self._jira_prj, version)
        jirakeys = ([issue.key, issue.fields.subtasks] for issue in story_issues)
        # 获取目录下excel用例中的jira号，只支持最新标准的用例模板
        files = [os.path.join(case_dir, f) for f in os.listdir(case_dir) if \
                 (os.path.isfile(os.path.join(case_dir, f)) and f.split('.')[-1] in ('xls', 'xlsx'))]
        for f in files:
            data = xlrd.open_workbook(f)
            sheets = data.sheets()
            for sheet in sheets:
                table = sheet
                nrows = table.nrows
                # 从第一行的名称获取'需求编号'所在的列
                for cl in range(table.ncols):
                    if table.cell(0, cl).value == col_name:
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
        return uncoverjiras


if __name__ == '__main__':
    '''
    jre = JiraExtend()
    jre.sync_sub_pjoect()
    '''
