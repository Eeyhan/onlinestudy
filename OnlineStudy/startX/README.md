# startX高效组件

一个基于django实现的快速自动生成增删改查的url，以及url对应的视图
原理和django的admin组件配置页面类似

## 开发环境


* django2
* python3


## 使用步骤

1. 主要的文件则是startX/serivce/v1 文件里的site对象

2. 将startX组件导入您的django项目，settings页面添加app
   添加app必须写全才能生效：'startX.apps.StartxConfig'
   
3. 根urls路由文件导入startX组件里的site对象


    from django.contrib import admin
    from django.urls import path
    from startX.serivce.v1 import site
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('start/', site.urls)
    ]

4. 在每个需要使用的业务app里创建一个startX.py文件
5. 在每个需要使用的业务app的apps.py文件做如下更改：
   
   这里我的业务app名为generic
    
    
    from django.apps import AppConfig
    from django.utils.module_loading import autodiscover_modules
    
    
    class GenericConfig(AppConfig):
        name = 'generic'
    
        def ready(self):
            autodiscover_modules('startX') 
    
    
   autodiscover_modules里的字符必须第4步和你创建的文件名一致
 
5. 以上已完成基本配置
   例：为一个表自动创建增删改查url，即对应的视图：
   
   * 1).业务generic里的models表：一个课程表
           
        
        class Course(models.Model):
            """
            课程表
            """
            name = models.CharField(verbose_name='课程名称', max_length=32)
        
            def __str__(self):
                return self.name
   
   * 2).在generic创建一个handler文件夹，里面放主要的handler操作类
        创建一个course.py 控制课程表
        
   * 3).course.py:
        
        
        from startX.serivce.v1 import StartXHandler
        from .base_promission import PermissionHandler
        
        
        class CourseHandler(PermissionHandler, StartXHandler):
            list_display = ['name']
   
   * 4).startX.py文件：
   
   
        from startX.serivce.v1 import site
        from generic import models
        from generic.handlers.course import CourseHandler
        
        
        site.register(models.Course, CourseHandler)
        # prev是url的后缀，一个表有多个操作对象时则可以如此配置
        site.register(models.Course, CourseHandler, prev='pub')
        
        
   * 5).启动项目，即可使用
   

## 说明：

   更多使用功能，在v1.py文件里，自行查看，基本都做了说明