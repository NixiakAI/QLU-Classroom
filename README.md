# qlu-cr
 查询校内空教室
 欢迎捐赠服务器或自行根据现有代码搭建服务以提升用户体验，当前使用cloudflare tunnel内网穿透功能以使校内服务器可以被校外访问。

 所需参数我这边不提供
只需要如下两步：
1. 在```get_course_on_table.py```文件中修改开学时间（开学那周的周一）
```python
# <<<<<!!!定义开学那周的周一!!!>>>>>
year,month,day=2024,2,20
```
2.还是这个文件下，修改这个东西
```python
# <<<<<!!!需要使用代理，提供Cookie获取数据!!!>>>>>
Cookie = "抓取提供"
```
 
 以下是配置服务器的教程（本人服务器是centos系统、配合宝塔面板进行部署）：
  ```python
 #1、先在宝塔面板下配置一个静态网页。
 #2、在服务器文件中上传qlu-cr的文件（其中包含本项目所有的文件）。
 #3、打开服务器的/lib/systemd/system/的目录下，去创建一个qlu.service的文件。然后在其中写一些内容，如下：
[Unit]
Description=Empt
After=network.service
 
[Service]
WorkingDirectory=写项目运行的目录
Type=idle
ExecStart=/usr/local/bin/python3 /项目运行目录/run.py > /www/wwwroot/logs/classroom.log 2>&1 
 
[Install]
WantedBy=multi-user.target

#4、在服务器端敲入命令systemctl status qlu.service，出现绿色的activ（running）表示正常运行。
#5、接着敲入systemctl start qlu.service表示启动服务
#6、接着看一下run.py给的端口，默认是5000。
#7、打开宝塔面板，给你的静态网站配置一下代理，打开网站的站点，在下面配置以下内容：代理名称（随便写），代理目录写/api/，目标URL写http://127.0.0.1:5000/api。
#8、完成！！！！！！！
```
 谈一下项目概况：
 本项目是由某位王学长提供，后端经过我的优化，修改，算是三创了（hhhhhh）！
 二创是王学长，一创是一位隐藏大佬，他在他自己原来的项目下进行了给鼠鼠我留下了链接（万分感谢！）

 再来解释一下前端的详情，大部分都是王学长在写。我时间有点不充足（大一鼠鼠课好多啊！）
 我再来说明一下项目查询不太准确的原因，其原因我认为有三点：
 1、本人太懒了，更新课表不及时。
 2、老师临时调课，数据没有录入系统
 3、晚自习被占用这个也是不录入系统的，建议大家去教室的最后一排坐。

 最后强调一点：本人服务器今年11月到期，以后能不能再为爱发电就看大家能不能给鼠鼠两块电池了！！！

