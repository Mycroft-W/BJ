
备份文件命令，讲一下内容写入bat 文件

```cmd 
Xcopy "E:\MyDrivers" "E:\%date:~5,2%月%date:~8,2%日\%time:~0,2%时%time:~3,2%分%time:~6,2%秒" /i /e /h /r /y "
```