# op_inital  
op inital server  
运维用于初始化新的Centos服务器，并根据配置文件批量连接服务器部署一些基础应用  

目录结构:  
|op_inital                       
|&nbsp;&nbsp;---action  
|&nbsp;&nbsp;&nbsp;&nbsp;---action_cmd.py            linux shell集合（hostname，banner，iptables规则以及修改root密码需根据需求修改）  
|&nbsp;&nbsp;&nbsp;&nbsp;---install_app.py           部署主方法  
|&nbsp;&nbsp;&nbsp;&nbsp;---upload_path.py           配置源文件父路径，目标服务器上传文件路径  
|&nbsp;&nbsp;---common  
|&nbsp;&nbsp;&nbsp;&nbsp;---read_json.py  
|&nbsp;&nbsp;&nbsp;&nbsp;---sftp_connect.py          SFTP连接传输文件   
|&nbsp;&nbsp;&nbsp;&nbsp;---ssh_connetc.py           SSH连接输入指令    
|&nbsp;&nbsp;&nbsp;&nbsp;---ssh_ppt.py               SSH交互方式连接输入指令   
|&nbsp;&nbsp;---main.py  

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
配置文件详见install_conf中的json文件，可配置多个服务器进行批量执行     
mdisk字段判断是否有需要挂载的大储存磁盘，无不填，有填写linux路径   
zabbix1表示配置内网连接    
zabbix2表示配置外网连接   
mariadb1表示无挂载直接安装   
mariadb2表示数据存储到挂载盘安装    

运行：
python3 main.py -f json_filepath   
-h可获取帮助
