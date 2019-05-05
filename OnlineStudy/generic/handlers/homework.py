from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, get_m2m_display
from generic import models
from startX.forms.widgets import DateTimePickerInput


class HomeworkHandler(StartXHandler):
    list_display = [get_m2m_display('课程','courses'), 'content']

    search_list = ['courses__contains']
