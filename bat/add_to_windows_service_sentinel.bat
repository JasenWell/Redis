rem start work!
:: 不会显示的注释  rem注释会回显
:: master_6379为脚本同目录对应的redis文件夹名
title master_6379
:: sentinel_mymaster为服务名,启动和停止需要使用
redis-server --service-install sentinel.conf --sentinel --service-name sentinel_mymaster --port 26379
::redis-server --service-install sentinel.conf --loglevel verbose  --service-name sentinel_mymaster --sentinel
exit