from startX.serivce.v1 import StartXHandler, get_field_display, StartXModelForm, Option
from generic import models
from startX.forms.widgets import DateTimePickerInput


class HomeworkHandler(StartXHandler):
    list_display = ['courses', 'teacher', 'content']

    search_list = ['courses__contains']
