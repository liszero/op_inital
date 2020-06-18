# op_inital
op inital server
运维用于初始化新的Centos服务器，并根据配置文件批量连接服务器部署一些基础应用

目录结构:
|op_inital                     
|  ---action
|      ---action_cmd.py            linux shell集合（hostname，banner以及修改root密码需根据需求修改）
|      ---install_app.py           部署主方法
|      ---upload_path.py           配置源文件路径，目标服务器上传文件路径
|  ---common
|      ---read_json.py
|      ---sftp_connect.py
|      ---ssh_connetc.py
|      ---ssh_ppt.py
|  main.py

需提供安装包的基础应用：
jdk-8u251-linux-x64.rpm
zabbix-agent-5.0.1-1.el7.x86_64.rpm
redis-5.0.8.tar.gz
  
支持部署应用：
JDK1.8
nginx
zabbix-agent
redis-5.0.8
mariadb-10.4
iptables

配置文件：
配置文件详见
