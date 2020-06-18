from action.action_cmd import *
from action.upload_path import *
from common.ssh_connect import ssh_conn
from common.sftp_connect import sftp_conn
from common.ssh_ppt import ppt
import os

def appinstall(**kwargs):
    host = kwargs["host"]
    port = kwargs["port"]
    username = kwargs["username"]
    password = kwargs["password"]
    hostname = kwargs["hostname"]
    mdisk = kwargs["mdisk"]
    install_app = kwargs["install"]
    # curpath = os.path.dirname(os.path.realpath(__file__))
    # curpath = curpath.replace('action', 'source_pkg')
    ssh_client = ssh_conn.conn(host,port,username,password)
    sftp_client = sftp_conn.conn(host,port,username,password)

    # 服务器初始化更新
    ssh_conn.cmd(ssh_client,os_init,host,"服务器初始化更新")

    # 更新hostname
    host_name = up_hostname(hostname)
    ssh_conn.cmd(ssh_client,host_name,host,"更新hostname")

    #更新banner
    ssh_conn.cmd(ssh_client,banner,host,"更新Banner")

    # zabbix
    if "zabbix1" in install_app or "zabbix2" in install_app:
        # 上传zabbix文件
        zabbix_localfile = os.path.join(jenkins_pkg_path, 'zabbix-agent-5.0.1-1.el7.x86_64.rpm')
        sftp_conn.put_file(sftp_client, zabbix_localfile, zabbix_upload_path)
        # 安装zabbix
        ssh_conn.cmd(ssh_client,install_zabbix,host,"安装Zabbix-agent")
        #配置内网连接
        if "zabbix1" in install_app:
            ssh_conn.cmd(ssh_client,zabbix_intranet_conf,host,"Zabbix-agent配置内网")
        elif "zabbix2" in install_app:
            ssh_conn.cmd(ssh_client,zabbix_extranet_conf,host,"Zabbix-agent配置外网")
        # zabbix修改主机名
        zabbix_hname = up_zhostname(hostname)
        ssh_conn.cmd(ssh_client,zabbix_hname,host,"Zabbix-agent更新主机名")
        # 启动zabbix
        ssh_conn.cmd(ssh_client,zabbix_start,host,"Zabbix-agent启用")

    # jdk
    if "jdk" in install_app:
        # 上传jdk文件
        jdk_localfile = os.path.join(jenkins_pkg_path, 'jdk-8u251-linux-x64.rpm')
        sftp_conn.put_file(sftp_client, jdk_localfile, jdk_upload_path)
        # 安装jdk
        ssh_conn.cmd(ssh_client,install_jdk,host,"安装JDK")

    # nginx
    if "nginx" in install_app:
        # 安装nginx
        ssh_conn.cmd(ssh_client,install_nginx,host,"安装Nginx")

    # 交互方式连接
    pptconn = ppt(host, username, password, port)
    client = pptconn.ppt_conn()


    # redis
    if "redis" in install_app:
        # 上传redis文件
        redis_localfile = os.path.join(jenkins_pkg_path, 'redis-5.0.8.tar.gz')
        sftp_conn.put_file(sftp_client, redis_localfile, redis_upload_path)
        # 安装redis
        ssh_conn.cmd(ssh_client,install_redis,host,"安装Redis")
        # redis服务化
        pptconn.ppt_action(client,redis_service,host,"redis服务化")

    # 挂载磁盘
    if len(mdisk) != 0 and "mariadb2" in install_app:
        mount_before = ssh_conn.cmd_echo(ssh_client, get_devlist(mdisk), host, "获取挂载前文件")
        pptconn.ppt_action(client, partition_disk(mdisk), host, "划分新磁盘")
        mount_after = ssh_conn.cmd_echo(ssh_client, get_devlist(mdisk), host, "获取挂载后文件")
        dev_name = set(mount_after).difference(set(mount_before)).pop()
        ssh_conn.cmd(ssh_client, mount_disk(dev_name), host, "挂载磁盘")
        disk_uuid = ssh_conn.cmd_echo(ssh_client, getuuid(dev_name), host, "获取磁盘UUID")[0].split('"')[1]
        ssh_conn.cmd(ssh_client, opmount(disk_uuid), host, "启动自挂载")
        # 更新系统日志配置
        ssh_conn.cmd(ssh_client,up_sysconf,host,"更新系统日志挂载配置")
        ssh_conn.cmd(ssh_client,sysconf_source,host,"系统日志生效")


    # 安装mariadb
    if "mariadb1" in install_app or "mariadb2" in install_app:
        ssh_conn.cmd(ssh_client, mariadb_repo, host, "配置mariadb镜像源")
        if "mariadb1" in install_app:
            ssh_conn.cmd(ssh_client,install_mariadb1,host,"无挂载盘安装mariadb")
        if "mariadb2" in install_app:
            ssh_conn.cmd(ssh_client,install_mariadb2,host,"挂载盘安装mariadb")
            for i in upsql_path:
                ssh_conn.cmd(ssh_client,i,host,"更新储存路径")
            ssh_conn.cmd(ssh_client,slow_sql,host,"新增慢sql文件并启动")
        pptconn.ppt_action(client,source_mariadb,host,"安全配置mariadb")

    # 安装iptables
    if "iptables" in install_app:
        ssh_conn.cmd(ssh_client,install_iptables,host,"安装iptables")
        ssh_conn.cmd(ssh_client,iptables_rule,host,"设置iptables规则")
        ssh_conn.cmd(ssh_client,up_iptables,host,"启动iptables")

    # 更新root密码
    ssh_conn.cmd(ssh_client,up_rootpw,host,"更新root密码并重启")

    # 断开连接
    sftp_conn.down(sftp_client)
    pptconn.ppt_close(client)
    ssh_conn.down(ssh_client)

