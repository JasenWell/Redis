rem start work!
:: 不会显示的注释  rem注释会回显
:: master_6379为脚本同目录对应的redis文件夹名
::cd master_6379
::add_to_windows_service.bat 
@echo off
start /D "D:\Service\Redis\master_6379" add_to_windows_service.bat
start /D "D:\Service\Redis\master_6479" add_to_windows_service.bat
start /D "D:\Service\Redis\master_6579" add_to_windows_service.bat
start /D "D:\Service\Redis\slave_6380" add_to_windows_service.bat
start /D "D:\Service\Redis\slave_6381" add_to_windows_service.bat
start /D "D:\Service\Redis\slave_6480" add_to_windows_service.bat
start /D "D:\Service\Redis\slave_6580" add_to_windows_service.bat

