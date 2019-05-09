from startX.serivce.v1 import StartXHandler
from django.urls import re_path
from django.conf import settings


class AccountRegisterTrendHandler(StartXHandler):
    header_list = ['查看趋势', '查看趋势', '查看趋势', '查看趋势', '查看趋势']
    base_year = 2016

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_headers_list(self):
        return self.header_list

    def get_body_list(self):
        body_list = []
        year = self.base_year
        for i in range(0, len(self.header_list)):
            url = '<a href="%s" target=“_blank”>%s</a>' % (settings.TREND_URL % year, year)
            year += 1
            body_list.append(url)
        body_list = [body_list]
        return body_list

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        return
