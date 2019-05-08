from django.db import models


# Create your models here.

class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色标题', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class User(models.Model):
    """
    用户
    """
    username = models.CharField(verbose_name='用户名', max_length=32)
    passwd = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='邮箱', max_length=32, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name='所属角色', to=Role, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        abstract = True


class Menu(models.Model):
    """
    一级菜单表
    """
    title = models.CharField(verbose_name='一级菜单名称', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32, unique=True)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限
    """
    title = models.CharField(verbose_name='权限标题', max_length=128)
    url = models.CharField(verbose_name='含正则的URL', max_length=512)
    name = models.CharField(verbose_name='URL别名', max_length=512, null=True, blank=True)
    menu = models.ForeignKey(to='Menu', on_delete='cascade', verbose_name='所属菜单',
                             null=True, blank=True,
                             help_text='null表示不是菜单;非null表示是二级菜单')
    pid = models.ForeignKey(verbose_name='关联的权限', to='Permission',
                            null=True, blank=True, related_name='parents',
                            help_text='对于非菜单权限需要选择一个可以成为菜单的权限，用户做默认展开和选中菜单',
                            on_delete='cascade')

    def __str__(self):
        return self.title
