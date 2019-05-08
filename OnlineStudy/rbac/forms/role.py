from django import forms
from rbac.models import Role


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
