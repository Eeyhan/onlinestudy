from startX.serivce.v1 import StartXHandler, Option, get_field_display, get_datetime_format
from django.urls import reverse, re_path


class AccountRegisterRecordHandler(StartXHandler):
    def get_add_btn(self, request, *args, **kwargs):
        return None

    list_display = ['username', 'career',
                    get_field_display('学历', 'education'),
                    get_datetime_format('注册日期', 'date')]

    def get_urls(self):
        """预留的重新自定义url钩子函数,主要是覆盖掉默认的url,并设置name别名"""

        patterns = [
            re_path(r'^list/$', self.wrapper(self.changelist), name=self.get_list_name),

        ]
        patterns.extend(self.extra_url())
        return patterns

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value
