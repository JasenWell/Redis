rem start work!
:: 不会显示的注释  rem注释会回显
:: master_6379为脚本同目录对应的redis文件夹名
title master_6379
:: redisService2为服务名,服务名对应安装在系统服务时的名字
redis-server --service-start --service-name redisService2