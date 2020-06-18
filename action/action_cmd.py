# 服务器初始化
os_init = 'yum -y update;' \
          'yum install -y vim nmap lrzsz epel-release htop unzip gcc gcc-c++ tcl tcl-devel wget ntpdate'

# 修改服务器名称
def up_hostname(hostname):
    return f'echo {hostname} >/etc/hostname'

# 修改Banner
banner = """echo '*****************************************************************
*                   写字楼里写字间，写字间里程序员；            *
*                   程序人员写程序，又拿程序换酒钱。            *
*                   酒醒只在网上坐，酒醉还来网下眠；            *
*                   酒醉酒醒日复日，网上网下年复年。            *
*****************************************************************'>/etc/motd"""

# 安装JDK
install_jdk = 'rpm -ivh /usr/local/src/jdk-8u251-linux-x64.rpm'

# 安装nginx
install_nginx = 'yum install -y nginx;systemctl enable nginx;systemctl start nginx'

# 安装zabbix
install_zabbix = 'rpm -ivh /usr/local/src/zabbix-agent-5.0.1-1.el7.x86_64.rpm;' \
# zabbix1内网连接
zabbix_intranet_conf = 'sed -i "s/Server=127.0.0.1/Server=127.0.0.1/g" /etc/zabbix/zabbix_agentd.conf;' \
                       'sed -i "s/ServerActive=127.0.0.1/ServerActive=127.0.0.1/g" /etc/zabbix/zabbix_agentd.conf'
# zabbix2外网连接
zabbix_extranet_conf = 'sed -i "s/Server=127.0.0.1/Server=127.0.0.1/g" /etc/zabbix/zabbix_agentd.conf;' \
		               'sed -i "s/ServerActive=127.0.0.1/ServerActive=127.0.0.1/g" /etc/zabbix/zabbix_agentd.conf'
# zabbix修改主机名
def up_zhostname(hostname):
    return f'sed -i "s/Hostname=Zabbix server/Hostname={hostname}/" /etc/zabbix/zabbix_agentd.conf'
# zabbix启动
zabbix_start = 'systemctl enable zabbix-agent;systemctl start zabbix-agent'


# 安装redis
install_redis = 'tar -xvf /usr/local/src/redis-5.0.8.tar.gz -C /usr/local/src/;' \
                'cd /usr/local/src/redis-5.0.8/src;make&&make install'
# 服务化redis
redis_service = ["/usr/local/src/redis-5.0.8/utils/install_server.sh","\r","\r","\r"]

# 安装mariadb
# 配置镜像源
mariadb_repo = """cat << "EOF" > /etc/yum.repos.d/MariaDB.repo
[MariaDB]
name = MariaDB
baseurl = http://mirrors.ustc.edu.cn/mariadb/yum/10.4/centos7-amd64/
gpgkey=http://mirrors.ustc.edu.cn/mariadb/yum/RPM-GPG-KEY-MariaDB
gpgcheck=1
EOF"""

# 获取磁盘文件
def get_devlist(mdisk):
    mdisk = mdisk[:-1] + '*'
    return f'ls {mdisk}'
# 划分新磁盘
def partition_disk(mdisk):
    return [f'fdisk {mdisk}','g','n','\r','\r','w']
# 磁盘挂载
def mount_disk(newdisk):
    return f"mkdir /vdb1;" \
           f"mkfs.xfs {newdisk};" \
           f"mount {newdisk} /vdb1"
# 获取磁盘UUID
def getuuid(newdisk):
    return "blkid %s|awk '{print $2}'" % newdisk
# 启动挂载
def opmount(UUID):
    return f'echo "UUID={UUID} /vdb1 xfs defaults 0 0" >> /etc/fstab'


# 无挂载安装mariadb
install_mariadb1 = "yum install  -y MariaDB-server MariaDB-client MariaDB-common;" \
                   "systemctl enable mariadb;" \
                   "systemctl start mariadb"
# 挂载安装mariadb
install_mariadb2 = "yum install  -y MariaDB-server MariaDB-client MariaDB-common;" \
                   "systemctl enable mariadb;" \
                   "systemctl start mariadb;" \
                   "systemctl stop mariadb;" \
                   "cp -a /var/lib/mysql /vdb1/mysql"
# 更新储存路径
upsql_path = ['sed -i "/\[mysqld\]/ainnodb_file_per_table=YES" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/aserver-id=1" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/alog-bin=mysql-bin" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/along_query_time=2" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/aslow_query_log_file=\/vdb1\/mysql\/slow_query_log\.log" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/aslow_query_log=on" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/acharacter-set-client-handshake=FALSE" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/askip-character-set-client-handshake=true" /etc/my.cnf.d/server.cnf',
"""sed -i "/\[mysqld\]/ainit_connect='SET NAMES utf8mb4'" /etc/my.cnf.d/server.cnf""",
'sed -i "/\[mysqld\]/acollation-server=utf8mb4_unicode_ci" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/acharacter_set_server=utf8mb4" /etc/my.cnf.d/server.cnf',
'sed -i "/\[mysqld\]/adatadir=\/vdb1\/mysql\/" /etc/my.cnf.d/server.cnf']
# 新增慢sql文件
slow_sql = "echo '' > /vdb1/mysql/slow_query_log.log;" \
           "chown mysql:mysql /vdb1/mysql/slow_query_log.log;" \
           "systemctl start mariadb"
# 安全配置mariadb
source_mariadb = ["mysql_secure_installation",'','n','n','y','y','y','y']


# 安装iptables
install_iptables = "systemctl stop firewalld.service;" \
                   "systemctl disable firewalld.service;" \
                   "yum install -y iptables-services"
# 设置规则
iptables_rule = """cat >/etc/sysconfig/iptables<<EOF
*filter
:INPUT ACCEPT [0:0]
# :FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [35:2716]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -j DROP
COMMIT
EOF"""
# 启动iptables
up_iptables = "systemctl enable iptables;" \
              "systemctl start iptables;"

# 更新系统日志配置
up_sysconf = """cat >>  /etc/profile  << "EOF"
if [ ! -d /vdb1/log/ ]; then
mkdir -p /vdb1/log/
chmod 777 -R /vdb1/log/
fi
if [ ! -d /vdb1/log/${LOGNAME} ]; then
mkdir -p /vdb1/log/${LOGNAME}
chmod 777 -R /vdb1/log/${LOGNAME}
fi
if [ $UID -ge 1000 ]; then
exec /usr/bin/script -t 2> /vdb1/log/${LOGNAME}/`date +%Y%m%d%H%M`.time -qaf /vdb1/log/${LOGNAME}/`date +%Y%m%d%H%M`.log
fi
EOF"""
sysconf_source = "source /etc/profile"

# 更新root密码
up_rootpw = 'echo "Z#H68fm1#S6NH&a%" | passwd --stdin root | history -c;reboot'