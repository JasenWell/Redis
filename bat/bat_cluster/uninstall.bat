﻿rem start work!
:: 不会显示的注释  rem注释会回显
:: master_6379为脚本同目录对应的redis文件夹名
::cd master_6379
::uninstall.bat

start /D "D:\Service\Redis\master_6379" uninstall.bat
start /D "D:\Service\Redis\master_6479" uninstall.bat
start /D "D:\Service\Redis\master_6579" uninstall.bat
start /D "D:\Service\Redis\slave_6380" uninstall.bat
start /D "D:\Service\Redis\slave_6381" uninstall.bat
start /D "D:\Service\Redis\slave_6480" uninstall.bat
start /D "D:\Service\Redis\slave_6580" uninstall.bat
