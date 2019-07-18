# onlinestudy


利用django结合restful规范开发的一个在线视频教育平台，可播放，播放调用保利威加密视频，可购买，购买调用支付宝接口。
另内含一个后台管理平台，基于角色等级的控制，根据不同的角色有不同的菜单功能显示



## 更新进度：

* 2019/07/18
 
    + 删除不必要的代码
    + 说明django自带的admin后台和本项目的后台的差别
    + 感谢给我star的兄弟们，后续会发布更多我自己开发的开源项目
    
## 开发环境

* 后端：
    + django 2+
    + djangorestframework组件
    + python 3.7
* 前端：
    + vue 2.5.2
    + webpack 3.6.0
	+ Element-UI 2
	
* 规范协议：
    + restful 
    + PEP8协议
    
* 数据库：
    + mysql(业务逻辑部分)
    + redis(持久化存储登录状态，商城数据)
    
* 第三方组件/接口：
    + 支付宝支付接口
    + 极验验证码
    + 保利威加密视频
    + matplotlab数据可视化
    + kindeditor富文本编辑器
    + bootstrap-datepicker日期选择器

## 主要功能

* 前端部分：
    + 在线播放视频(本项目中由于加密视频平台的测试账号有效期已过，目前无法播放)
    + 登录注册均调用极验验证码验证机制
    + 课程相关展示 
    + 购物车、优惠券
    + 作业提交、问题提问、商品评价
* 后端部分：
    + 采用restful规范，利用django的DRF组极简与前端分离并做数据交互
    + 与前端部分的数据存储使用redis永久存储
* 后台部分：
    + 造了一个轮子 —— [django-startX](https://github.com/Eeyhan/django-startX "django-startX") 快速实现后台权限管理
    + 造了一个轮子 —— [django-rbac](https://github.com/Eeyhan/django-rbac "django-startX") 快速完成根据角色不同做不同的功能权限限制
    + 利用matplotlab模块，对注册用户、账单进行数据分析形成趋势图


## 数据库、账户相关


* 本项目不附带数据库源数据，自行配置数据库，在后端部分的根目录onlinestudy/onlinestudy/settings.py文件配置数据库，以下为mysql数据库的配置

``
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'HOST': '主机地址(IP地址)',
			'PORT': '数据库端口',
			'USER': '账户名',
			'PASSWORD': '密码',
			'NAME': '数据库名',
			# 'OPTIONS': {
			#     'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", 
			# },
		}
	}
``
* 终端下进入后端部分的根目录onlinestudy，使用如下命令迁移数据库

`` python manage.py makemigrations``
`` python manage.py migrate``

* 迁移之后自行创建数据库，根据自己的数据库账号密码进行登录验证

* 以下为本项目的登录界面：

![本项目后台](https://raw.githubusercontent.com/Eeyhan/pictures/master/django-backend.png)

* 登录成功界面：

![本项目后台](https://raw.githubusercontent.com/Eeyhan/pictures/master/django-backend2.png)
  
* django自带admin组件后台如下(该后台可以做快速处理，并不是本项目的后台)

![django自带后台](https://raw.githubusercontent.com/Eeyhan/pictures/master/django-admin.png)

* 登录成功界面：
![django自带后台](https://raw.githubusercontent.com/Eeyhan/pictures/master/django-admin2.png)
   
* 所有django自带admin组件后台的测试用户的密码都是123
* django自带admin组件后台的超级用户账户：root/123456


	
## 程序流程图

* http://naotu.baidu.com/file/c064fd111c5aac470d067f0c58942617

## 启动项目之前

* 后端部分请按照根目录的requirements.txt文件安装必须的第三方依赖
    + 安装命令
    
    ``pip install -r requirements.txt``
     
* 前端部分请进入根目录，运行如下命令安装必须的第三方依赖  
    + 前提请自行安装node.js
    
    ``npm install``   
    
    

## 启动项目

### 后端部分：
    进入后端根目录onlinestudy
    python manage.py runserver 127.0.0.1:8000 (启动地址随意)

### 自动转化代码为PEP8规范
    进入后端根目录onlinestudy
    
    ``autopep8 --in-place --aggressive --aggressive onlinestudy ``

### 单元测试
    进入后端根目录onlinestudy
    
    ``python manage.py test ``

### 前端部分：
    进入前端端根目录onlinestudy
    
    开发环境：npm run dev
    生产环境：npm run bulid

## 启动之后的界面展示

### 由于数据来源后端动态显示，所以无法在线展示，以下是图片展示

* 前端部分
    
    ![首页](https://raw.githubusercontent.com/Eeyhan/pictures/master/1.png)
    
    ![首页](https://raw.githubusercontent.com/Eeyhan/pictures/master/2.png)
    
    ![底部](https://raw.githubusercontent.com/Eeyhan/pictures/master/3.png)
    
    ![课程](https://raw.githubusercontent.com/Eeyhan/pictures/master/4.png)
    
    + 并且课程支持按标签，按热度，价格高低筛选
    
    ![课程部分](https://raw.githubusercontent.com/Eeyhan/pictures/master/5.png)
    
    + 滑到中下部自动出现购物车和回顶部的悬浮按钮
    
    ![高级课程](https://raw.githubusercontent.com/Eeyhan/pictures/master/6.png)
    
    ![课程详情部分](https://raw.githubusercontent.com/Eeyhan/pictures/master/7.png)
    
    ![课程详情部分](https://raw.githubusercontent.com/Eeyhan/pictures/master/8.png)
    
    ![购买部分](https://raw.githubusercontent.com/Eeyhan/pictures/master/33.png)
    
    + 如果未登录就会跳到登录页面
    
    ![登录页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/10.png)
    
    ![注册页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/32.png)
    
    ![登录之后进入首页](https://raw.githubusercontent.com/Eeyhan/pictures/master/11.png)
    
    ![购物车](https://raw.githubusercontent.com/Eeyhan/pictures/master/34.png)
    
    ![结算中心](https://raw.githubusercontent.com/Eeyhan/pictures/master/35.png)
    
    ![选择优惠券](https://raw.githubusercontent.com/Eeyhan/pictures/master/36.png)
    
    ![支付宝支付](https://raw.githubusercontent.com/Eeyhan/pictures/master/37.png)
    
    ![我的订单页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/38.png)
    
    ![学习中心部分，课程课时](https://raw.githubusercontent.com/Eeyhan/pictures/master/16.png)
    
    ![作业页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/17.png)
    
    + <font color="#dd0000">由于我的保利威测试账户有效期已过，所以无法正常显示视频</font><br /> 
    
    ![视频播放页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/18.png)

* 后端部分

    ![后台登录页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/19.png)
    
    ![后台首页](https://raw.githubusercontent.com/Eeyhan/pictures/master/20.png)
    
    ![菜单列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/21.png)
    
    ![权限批量分配页面](https://raw.githubusercontent.com/Eeyhan/pictures/master/22.png)
    
    ![账单列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/23.png)
    
    ![账单报表](https://raw.githubusercontent.com/Eeyhan/pictures/master/24.png)
    
    ![用户列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/25.png)
    
    + 富文本插件的使用
    
    ![资讯管理](https://raw.githubusercontent.com/Eeyhan/pictures/master/39.png)
    
    + datepicker的使用
    
    ![datepicker](https://raw.githubusercontent.com/Eeyhan/pictures/master/40.png)
    
    ![注册用户分析](https://raw.githubusercontent.com/Eeyhan/pictures/master/26.png)
    
    ![角色列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/27.png)
    
    ![角色功能分配](https://raw.githubusercontent.com/Eeyhan/pictures/master/28.png)
    
    ![学生列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/29.png)
    
    ![课程列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/30.png)
    
    ![课程详情列表](https://raw.githubusercontent.com/Eeyhan/pictures/master/31.png)
    
	
## 个人的技术文章请移步：[博客文章](https://www.cnblogs.com/Eeyhan/ "博客文章")
