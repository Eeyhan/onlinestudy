# onlinestudy


利用django结合restful规范开发的一个在线视频教育平台，可播放，播放调用保利威加密视频，可购买，购买调用支付宝接口。
另内含一个后台管理平台，基于角色等级的控制，根据不同的角色有不同的菜单功能显示

## 开发环境

* 后端：
    + django 2+
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
    + 造了一个轮子 —— [django-startX](https://github.com/yang-va/django-startX "django-startX") 快速实现后台权限管理
    + 造了一个轮子 —— [django-rbac](https://github.com/yang-va/django-rbac "django-startX") 快速完成根据角色不同做不同的功能权限限制
    + 利用matplotlab模块，对注册用户、账单进行数据分析形成趋势图

## 账户相关
* 所有测试用户的密码都是123
* django的超级用户账户：root/123456

	
## 程序流程图

* http://naotu.baidu.com/file/c064fd111c5aac470d067f0c58942617

## 启动项目之前

* 后端部分请按照根目录的requirements.txt文件安装必须的第三方依赖
    + 安装命令
    
    ``pip install -r requirements.txt``
     
* 前端部分请进入根目录，运行如下命令安装必须的第三方依赖  
    
    
    ``npm install``
    
    + 前提请自行安装node.js
    

## 启动项目

### 后端部分：
    进入后端根目录onlinestudy
    python manage.py runserver 127.0.0.1:8000 (启动地址随意)

### 自动转化代码为PEP8规范
    进入后端根目录onlinestudy
    
    ``autopep8 --in-place --aggressive --aggressive onlinestudy ``

### 前端部分：
    进入前端端根目录onlinestudy
    
    开发环境：npm run dev
    生产环境：npm run bulid

## 启动之后的界面展示

### 由于数据来源后端动态显示，所以无法在线展示，以下是图片展示

* 前端部分
    
    ![首页](https://raw.githubusercontent.com/yang-va/pictures/master/1.png)
    
    ![首页](https://raw.githubusercontent.com/yang-va/pictures/master/2.png)
    
    ![底部](https://raw.githubusercontent.com/yang-va/pictures/master/3.png)
    
    ![课程](https://raw.githubusercontent.com/yang-va/pictures/master/4.png)
    
    + 并且课程支持按标签，按热度，价格高低筛选
    
    ![课程部分](https://raw.githubusercontent.com/yang-va/pictures/master/5.png)
    
    + 滑到中下部自动出现购物车和回顶部的悬浮按钮
    
    ![高级课程](https://raw.githubusercontent.com/yang-va/pictures/master/6.png)
    
    ![课程详情部分](https://raw.githubusercontent.com/yang-va/pictures/master/7.png)
    
    ![课程详情部分](https://raw.githubusercontent.com/yang-va/pictures/master/8.png)
    
    ![购买部分](https://raw.githubusercontent.com/yang-va/pictures/master/33.png)
    
    + 如果未登录就会跳到登录页面
    
    ![登录页面](https://raw.githubusercontent.com/yang-va/pictures/master/10.png)
    
    ![注册页面](https://raw.githubusercontent.com/yang-va/pictures/master/32.png)
    
    ![登录之后进入首页](https://raw.githubusercontent.com/yang-va/pictures/master/11.png)
    
    ![购物车](https://raw.githubusercontent.com/yang-va/pictures/master/34.png)
    
    ![结算中心](https://raw.githubusercontent.com/yang-va/pictures/master/35.png)
    
    ![选择优惠券](https://raw.githubusercontent.com/yang-va/pictures/master/36.png)
    
    ![支付宝支付](https://raw.githubusercontent.com/yang-va/pictures/master/37.png)
    
    ![我的订单页面](https://raw.githubusercontent.com/yang-va/pictures/master/38.png)
    
    ![学习中心部分，课程课时](https://raw.githubusercontent.com/yang-va/pictures/master/16.png)
    
    ![作业页面](https://raw.githubusercontent.com/yang-va/pictures/master/17.png)
    
    + <font color="#dd0000">由于我的保利威测试账户有效期已过，所以无法正常显示视频</font><br /> 
    
    ![视频播放页面](https://raw.githubusercontent.com/yang-va/pictures/master/18.png)

* 后端部分

    ![后台登录页面](https://raw.githubusercontent.com/yang-va/pictures/master/19.png)
    
    ![后台首页](https://raw.githubusercontent.com/yang-va/pictures/master/20.png)
    
    ![菜单列表](https://raw.githubusercontent.com/yang-va/pictures/master/21.png)
    
    ![权限批量分配页面](https://raw.githubusercontent.com/yang-va/pictures/master/22.png)
    
    ![账单列表](https://raw.githubusercontent.com/yang-va/pictures/master/23.png)
    
    ![账单报表](https://raw.githubusercontent.com/yang-va/pictures/master/24.png)
    
    ![用户列表](https://raw.githubusercontent.com/yang-va/pictures/master/25.png)
    
    + 富文本插件的使用
    
    ![资讯管理](https://raw.githubusercontent.com/yang-va/pictures/master/39.png)
    
    + datepicker的使用
    
    ![datepicker](https://raw.githubusercontent.com/yang-va/pictures/master/40.png)
    
    ![注册用户分析](https://raw.githubusercontent.com/yang-va/pictures/master/26.png)
    
    ![角色列表](https://raw.githubusercontent.com/yang-va/pictures/master/27.png)
    
    ![角色功能分配](https://raw.githubusercontent.com/yang-va/pictures/master/28.png)
    
    ![学生列表](https://raw.githubusercontent.com/yang-va/pictures/master/29.png)
    
    ![课程列表](https://raw.githubusercontent.com/yang-va/pictures/master/30.png)
    
    ![课程详情列表](https://raw.githubusercontent.com/yang-va/pictures/master/31.png)
    
	
