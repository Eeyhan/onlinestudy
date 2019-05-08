from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from rbac.forms import menu
from rbac.service.urls import memory_reverse
from django.forms import formset_factory
from rbac.service.routers import get_all_url_dict
from collections import OrderedDict
from django.utils.module_loading import import_string
from django.conf import settings


def menu_list(request):
    """
    菜单列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()
    mid = request.GET.get('mid')
    second_menu_id = request.GET.get('sid')

    # 一级、二级菜单
    menu_exists = models.Menu.objects.filter(id=mid).exists()
    if not menu_exists:
        mid = None
    if mid:
        second_menu = models.Permission.objects.filter(menu__id=mid)
    else:
        second_menu = []

    # 二级、三级菜单
    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:
        permission_menu = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permission_menu = []

    return render(request, 'rbac/menu_list.html', {'menus': menus,
                                                   'mid': mid,
                                                   'second_menu': second_menu,
                                                   'second_menu_id': second_menu_id,
                                                   'permission_menu': permission_menu})


def menu_add(request):
    """
    添加菜单
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = menu.MenuModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    form = menu.MenuModelForm(request.POST)
    if form.is_valid():
        form.save()

        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, id):
    """
    编辑菜单
    :param request:
    :param id: 对象id
    :return:
    """
    obj = models.Menu.objects.filter(id=id).first()
    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = menu.MenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = menu.MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()

        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, id):
    """
    删除菜单
    :param request:
    :param id: 删除对象id
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Menu.objects.filter(id=id).delete()
    return redirect(url)


def second_menu_add(request, pk):
    """
    二级菜单添加
    :param request:
    :param mid: 一级菜单id
    :return:
    """
    if request.method == 'GET':
        menu_object = models.Menu.objects.filter(id=pk).first()
        form = menu.SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/change.html', {'form': form})
    form = menu.SecondMenuModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
    """
    二级菜单编辑
    :param request:
    :param id: 一级菜单id
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = menu.SecondMenuModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = menu.SecondMenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
    """
    二级菜单删除
    :param request:
    :param id: 二级菜单id
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def permission_add(request, pk):
    """
    添加权限
    :param request:
    :param sid:
    :return:
    """
    if request.method == 'GET':
        form = menu.PermissionModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = menu.PermissionModelForm(request.POST)
    if form.is_valid():
        permission_object = models.Permission.objects.filter(id=pk).first()
        if not permission_object:
            return HttpResponse('未关联二级菜单，请先关联再操作！')
        form.instance.pid = permission_object
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限
    :param request:
    :param id: 权限对象id
    :return:
    """
    obj = models.Permission.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('权限不存在')

    if request.method == 'GET':
        form = menu.PermissionModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = menu.PermissionModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
    """
    删除权限
    :param request:
    :param id: 权限对象id
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def multi_permission(request):
    """
    权限的批量操作
    :param request:
    :return:
    """
    # 获取所有的url
    post_type = request.GET.get('type')  # 提交的类型，是新建还是修改
    generate_formset_class = formset_factory(menu.MultiPermissionForm, extra=0)
    update_formset_class = formset_factory(menu.MultiUpdatePermissionForm, extra=0)

    generate_formset = None
    update_formset = None

    if request.method == 'POST' and post_type == 'generate':  # 批量添加
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data  # 临时存储正确数据
            has_error = False
            for i in range(formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:  # 没有错的话，多个数据同时添加
                models.Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset = formset

    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset

    # 获取此项目中所有url
    all_url = get_all_url_dict()
    router_set = set(all_url.keys())

    # 获取数据库中所有url
    db_url = models.Permission.objects.all().values('id', 'title', 'url', 'name', 'menu_id', 'pid_id')
    db_url_dict = OrderedDict()
    db_url_set = set()
    for item in db_url:
        db_url_dict[item['name']] = item
        db_url_set.add(item['name'])

    # 检测数据库与url中数据，数据条数一致，但数据是否一致
    for name, value in db_url_dict.items():
        router_row_dict = all_url.get(name)  # {'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 应该添加到数据库的权限，数据库没有，url内有，但必须有name别名
    if not generate_formset:
        generate_name_list = router_set - db_url_set
        generate_formset = generate_formset_class(
            initial=[row_dict for name, row_dict in all_url.items() if name in generate_name_list])

    # 应该删除数据库的权限，数据库有，url内没有

    delete_name_list = db_url_set - router_set
    delete_row_list = [row_dict for name, row_dict in db_url_dict.items() if name in delete_name_list]

    # 应该修改的权限，数据库和url内数目一致，但是具体数据不一致

    if not update_formset:
        update_name_list = router_set & db_url_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in db_url_dict.items() if name in update_name_list])

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'generate_formset': generate_formset,
            'delete_row_list': delete_row_list,
            'update_formset': update_formset,
        }
    )


def multi_permission_del(request, id):
    """
    批量页面的权限删除
    :param request:
    :param pk: 删除的权限对象id
    :return:
    """
    url = memory_reverse(request, 'rbac:multi_permission')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=id).delete()
    return redirect(url)


# def distribute_permission(request):
#     """
#     权限分配
#     :param request:
#     :return:
#     """
#     user_list = user_class.objects.all()
#     role_list = models.Role.objects.all()
#     all_menu_list = models.Menu.objects.all()
#     return render(request, 'rbac/distribute_permission.html',
#                   {'user_list': user_list,
#                    'role_list':role_list,
#                    'all_menu_list':all_menu_list})


def distribute_permission(request):
    """
    权限分配
    :param request:
    :return:
    """

    user_id = request.GET.get('uid')
    user_class = import_string(settings.RBAC_USER_MODLE_CLASS)
    user_object = user_class.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        # 用户和角色关系添加到第三张表（关系表）
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')
        # xx.字段.set()是多对多的插入数据
        user_object.roles.set(role_id_list)

    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色，然后再分配权限！')
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}

    # 获取当前用户对于角色的所有权限

    # 如果选中的角色，优先显示选中角色所拥有的权限
    # 如果没有选择角色，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}

    elif user_object:  # 未选择角色，但选择了用户
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions_dict = {}

    all_user_list = user_class.objects.all()

    all_role_list = models.Role.objects.all()

    menu_permission_list = []

    # 所有的菜单（一级菜单）
    all_menu_list = models.Menu.objects.values('id', 'title')
    """
    [
        {id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,'children':[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1 },]},
        {id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2 },{id:5,title:x1, menu_id:2 },]},
        {id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3 },]},
    ]
    """
    all_menu_dict = {}
    """
       {
           1:{id:1,title:菜单1,children:[{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },{id:2,title:x1, menu_id:1,children:[] },]},
           2:{id:2,title:菜单2,children:[{id:3,title:x1, menu_id:2,children:[] },{id:5,title:x1, menu_id:2,children:[] },]},
           3:{id:3,title:菜单3,children:[{id:4,title:x1, menu_id:3,children:[] },]},
       }
       """
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item

    # 所有二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')

    """
    [
        {id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
        {id:2,title:x1, menu_id:1,children:[] },
        {id:3,title:x1, menu_id:2,children:[] },
        {id:4,title:x1, menu_id:3,children:[] },
        {id:5,title:x1, menu_id:2,children:[] },
    ]
    """

    all_second_menu_dict = {}
    """
        {
            1:{id:1,title:x1, menu_id:1,children:[{id:11,title:x2,pid:1},] },   
            2:{id:2,title:x1, menu_id:1,children:[] },
            3:{id:3,title:x1, menu_id:2,children:[] },
            4:{id:4,title:x1, menu_id:3,children:[] },
            5:{id:5,title:x1, menu_id:2,children:[] },
        }
        """

    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row

        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 所有三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    """
    [
        {id:11,title:x2,pid:1},
        {id:12,title:x2,pid:1},
        {id:13,title:x2,pid:2},
        {id:14,title:x2,pid:3},
        {id:15,title:x2,pid:4},
        {id:16,title:x2,pid:5},
    ]
    """
    for row in all_permission_list:
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    """
    [
        {
            id:1,
            title:'业务管理'
            children:[
                {
                    'id':11, 
                    title:'账单列表',
                    children:[
                        {'id':12,title:'添加账单'}
                    ]
                },
                {'id':11, title:'客户列表'},
            ]
        },

    ]
    """

    return render(
        request,
        'rbac/distribute_permission.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
        }
    )
