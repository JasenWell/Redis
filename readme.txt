
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
 
 集群需要拷贝redis安装后的文件夹，可重命名slave_6380  slave_6381等
 集群从节点文件redis.windows-service.conf  需要开启 slaveof 127.0.0.1 6379 对应主节点的ip 和端口,主节点有密码的还需要开启masterauth 密码
 非系统服务方式启动sentinel命令 redis-server.exe sentinel.conf --sentinel 或者 redis-sentinel sentinel.conf
 sentinel.conf 文件必须ansi格式编码，utf-8会安装出错
