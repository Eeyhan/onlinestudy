from django.shortcuts import render, redirect, HttpResponse
from rbac.models import User
from django.urls import reverse
from rbac.forms.user import UserModelForm, UpdateUserModelForm, ResetUserModelForm


def user_list(request):
    users = User.objects.all()
    return render(request, 'rbac/user_list.html', {'users': users})


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_reset_password(request, id):
    obj = User.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('不存在该用户')

    if request.method == 'GET':
        form = ResetUserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = ResetUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, id):
    obj = User.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('不存在该用户')

    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = UpdateUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_del(request, id):
    cancel = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': cancel})

    User.objects.filter(id=id).delete()
    return redirect(cancel)
