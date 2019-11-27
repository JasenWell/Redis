
#下载地址  https://github.com/MicrosoftArchive/redis/releases


修改redis.windows.conf文件，设置maxmemory 大小    # redis.windows-service.conf 文件也需要修改(如果是安装在系统服务中)
maxmemory 1024*1024*100  # 100mb
requirepass 123456

cmd中进入redis安装路径输入命令 redis-server.exe redis.windows.conf
因为修改了配置文件，抛异常：creating server tcp listening socket 127.0.0.1:6379:bind:no error
输入命令： redis-cli -a 密码 后执行shutdown 后执行quit 重新执行redis-server.exe redis.windows.conf 成功
# 也可以输入 redis-cli -h 127.0.0.1 -p 6379 -a 密码 进入后可执行info replication 查看状态  info sentinel查看哨兵

将redis加入到windows的服务中
安装命令: redis-server.exe --service-install redis.windows.conf --loglevel verbose 使用命令，
因为前面已经加入服务，需要先卸载服务，执行命令redis-server --service-uninstall
重新执行命令 redis-server.exe --service-install redis.windows.conf --loglevel verbose  可以不执行前面的操作，直接执行这个??

将redis服务添加到windows服务中：redis-server --service-install redis.windows.conf --service-name redis6379 --loglevel verbose
指定服务名称为redis6379，这样就不会和之前的服务名称冲突，也可以在不删除之前的服务情况下，安装新的redis服务。

然后可以用下面的命令执行启动或停止
卸载服务：redis-server --service-uninstall
开启服务：redis-server --service-start
停止服务：redis-server --service-stop
重命名服务：redis-server --service-name name
重命名服务，需要写在前三个参数之后，例如：
The following would install and start three separate instances of Redis as a service:   
以下将会安装并启动三个不同的Redis实例作服务：

redis-server --service-install --service-name redisService1 --port 10001
redis-server --service-start --service-name redisService1

redis-server --service-install --service-name redisService2 --port 10002
redis-server --service-start --service-name redisService2

redis-server --service-install --service-name redisService3 --port 10003
redis-server --service-start --service-name redisService3


# https://www.cnblogs.com/javabg/p/9133206.html 参考
#  https://www.jianshu.com/p/6895384d2b9e redis desktop manager下载安装使用

python redis 操作参考 https://www.jianshu.com/p/b85c04bef5e7 https://www.php.cn/python-tutorials-356574.html
Python操作redis集群 https://www.jianshu.com/p/d38902ba5698 
集群参考:
 http://www.imooc.com/article/257706?block_id=tuijian_wz
 https://www.cnblogs.com/Yang2012/p/8078644.html
 https://blog.csdn.net/weixin_41846320/article/details/83753182  redis+sentinel
 https://blog.csdn.net/weixin_41846320/article/details/83753667  主从复制
 https://blog.csdn.net/weixin_41846320/article/details/83654766 redis+cluster
 https://www.cnblogs.com/guolianyu/p/10345387.html redis+cluster
 
 sentinel 集群：
 集群需要拷贝redis安装后的文件夹，可重命名slave_6380  slave_6381等
 集群从节点文件redis.windows-service.conf  需要开启 slaveof 127.0.0.1 6379 对应主节点的ip 和端口,主节点有密码的还需要开启masterauth 密码
 非系统服务方式启动sentinel命令 redis-server.exe sentinel.conf --sentinel 或者 redis-sentinel sentinel.conf
 sentinel.conf 文件必须ansi格式编码，utf-8会安装出错
 sentinel 集群：主节点也需要开启masterauth 密码,否则在节点机下线在重新上线时无法连接
 
 cluster 集群：不需要开启 slaveof 127.0.0.1 6379
1.集群需要拷贝redis安装后的文件夹，可重命名master_6379 slave_6380  slave_6381等,至少需要6个文件夹(即3主3从),
 修改各自redis.windows.conf对应端口号 ==>
 将以下注释打开,使能cluster集群
cluster-enabled yes
cluster-config-file nodes-6379.conf    # nodes-6379.conf 是为该节点的配置信息，这里使用 nodes-端口.conf命名方法。服务启动后会在目录生成该文件。
cluster-node-timeout 15000
appendonly yes

2.安装ruby 环境  https://rubyinstaller.org/downloads/  选择WITHOUT DEVKIT的64位版本 安装时选完配置
3.安装Redis的Ruby驱动redis-xxxx.gem   https://rubygems.org/pages/download
	下载zip并解压,切换到解压目录命令行执行  ruby setup.rb
	再用 GEM 安装 Redis ：切换到redis安装目录(我这里切换到master主目录)，需要在命令行中，执行 gem install redis
4.安装redis服务并启动(我这里安装到系统服务并启动,这里要注意缓存的slave写入可能会造成启动不了,需要删除)	
5.安装集群脚本redis-trib
	=>redis5.0以上  下载 https://raw.githubusercontent.com/antirez/redis/unstable/src/redis-trib.rb 
	打开该链接把里面的脚本保存为redis-trib.rb，这里放在了master_6379目录下面,也可以放其他下面
	redis-trib.rb集群的命令为 ==>进入目录执行

	redis-trib.rb create --replicas 1 127.0.0.1:6379 127.0.0.1:6380 127.0.0.1:6381 127.0.0.1:6382 127.0.0.1:6383 127.0.0.1:6384

	--replicas 1 表示每个主数据库拥有从数据库个数为1。master节点不能少于3个，所以我们用了6个redis

	=>redis5.0以下  ,进人master主目录，我使用此命令
	redis-cli -a 密码 --cluster create 192.168.250.129:7000 192.168.250.129:7001 192.168.250.130:7002 192.168.250.130:7003 192.168.250.131:7004 192.168.250.131:7005 --cluster-replicas 1
	其中 cluster-replicas 1  代表  一个master后有几个slave，1代表为1个slave节点
	只要服务未卸载就不用重复执行此命令？？
	
	错误：Unrecognized option or bad number of args for: ‘-–cluster’ 未解决,还不能创建
	
使用Redis客户端Redis-cli.exe来查看数据记录数，以及集群相关信息

命令 redis-cli –c –h ”地址” –p "端口号" ;  c 表示集群  需要密码 -a 密码
cluster nodes查看群节点

Redis集群数据分配策略：

采用一种叫做哈希槽 (hash slot)的方式来分配数据，redis cluster 默认分配了 16384 个slot，当我们set一个key 时，会用CRC16算法来取模得到所属的slot，然后将这个key分到哈希槽区间的节点上，具体算法就是：CRC16(key) % 16384

注意的是：必须要3个以上的主节点，否则在创建集群时会失败，三个节点分别承担的slot 区间是：

节点A覆盖0－5460;
节点B覆盖5461－10922;
节点C覆盖10923－16383.


