from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, get_m2m_display
from generic import models


class StudentModelForm(StartXModelForm):
    class Meta:
        model = models.Student
        fields = ['tutor']


class StudentHandler(StartXHandler):
    order_by = ['id']
    model_form_class = StudentModelForm
    list_display = ['account', 'qq', 'mobile', 'emergency_contract', 'score',
                    get_field_display('状态', 'student_status'),
                    get_m2m_display('已买课程', 'courses'),'tutor']

    def get_add_btn(self, request, *args, **kwargs):
        return None

    def get_list_display(self, request, *args, **kwargs):
        """
        预留的钩子函数
        :return: 为不同权限的用户设置预留的扩展，自定义显示列
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit)
        return value
