# Mysql 时区设置

```sql
SET GLOBAL time_zone = '+8:00';
SET time_zone = '+8:00';
FLUSH PRIVILEGES;
```

查看当前时间

```sql
SELECT curtime();
SELECT now();
show varialbes like "%time_zone%";
```
