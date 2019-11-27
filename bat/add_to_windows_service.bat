rem start work!
:: 不会显示的注释  rem注释会回显
:: master_6379为脚本同目录对应的redis文件夹名
title master_6379
:: redisService2为服务名,启动和停止需要使用
redis-server --service-install redis.windows.conf --service-name mymaster --loglevel verbose
exit