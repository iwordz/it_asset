

IT资产管理系统使用说明

1.本系统需要使用Python Django、Python MySQL-db、Bootstrap3、Jquery等模块支持

2.支持原生Django部署且同时也支持Nginx+Wsgi方式部署

3.模块安装：

git clone https://github.com/iwordz/it_asset

cd it_asset

导入 it_asset.sql mysql数据库文件

下面开始安装Django类库:

pip install django==1.7

pip install MySQL-Python(如果执行上面命令出现找不到"EnvironmentError: mysql_config not found"等字样，则需要执行export PATH=$PATH:/path/mysql/bin 注意path是你mysql安装的实际目录。)

4.本系统已经在Mac OSX和Centos上进行过测试

5.部分功能界面预览

5.1仪表盘功能

![image](https://github.com/iwordz/it_asset/blob/master/static/images/3.jpg)

5.2机柜分布图

![image](https://github.com/iwordz/it_asset/blob/master/static/images/4.jpg)

5.3配置项管理

![image](https://github.com/iwordz/it_asset/blob/master/static/images/5.jpg)

5.4用户管理

![image](https://github.com/iwordz/it_asset/blob/master/static/images/6.jpg)


6.正式发布

打开setting.py设置如下参数：
DEBUG=False
ALLOWED_HOSTS = ["*"]

7.本系统部分使用了开源系统，如有侵犯您的版本，请联系我删除，谢谢合作！


8.本系统仅仅是一个实验性的演示系统，不作为正式环境产品。感谢您的参与。如果在测试过程中遇到任何问题，请与我联系。（email:fanghouguo@protonmail.com）


