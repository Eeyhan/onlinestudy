#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms


class DateTimePickerInput(forms.TextInput):
    template_name = 'startX/forms/widgets/datetime_picker.html'
