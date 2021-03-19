# SQL语句

## 用户管理

|SQL 语句| 描述|
|--|--|
|GRANT ALL ON *.* TO 'user'@'host' IDENTIFIED BY 'password'|创建用户并授权|
|REVOKE ALL ON *.* FROM 'user'@'host'|取消对用户的授权|
|SHOW GRANTS FOR 'user'@'host'|查看用户权限|
|FLUSH PRIVILEGES|刷新权限|

## 库管理

|SQL 语句|描述|
|--|--|
|CREATE DATABASE \<DATABASE>|创建数据库[指定字符集]|
|DROP DATABASE \<DATABASE>|删除库|
|USE \<DATABASE> | 使用数据库,后续操作默认以之为目标|
|SHOW \<DATABASES>|列出所有库|

## 表管理

|SQL语句|描述|
|--|--|
|SHOW \<TABLES>|列出库中所有表|
|SHOW COLUMNS FROM \<TABLE>\| DESCRIBE \<TABLE>| 显示数据表的列信息|
|SHOW INDEX FROM \<TABLE>|显示表的索引信息|
|SHOW TABLE STATUS|输出表的统计信息|
|CREATE TABLE \<TABLE> (column_name column_type,...)|创建表及列名和属性|
|DROP TABLE \<TABLE>|删除表|
|ALTER TABLE \<old_name> RENAME TO \<new_name>|修改表名|

## 表中数据管理

|SQL语句|描述|
|--|--|
|INSERT INTO \<TABLE> (field1,...) VALUES (value1,...)|插入数据|
|SELECT \<column_name>,... FROM \<TABLE>|查询数据|
|UPDATE \<TABLE> SET field1=newvalue1,...| 修改数据|
|DELETE FROM \<TABLE> WHERE \<Clause>| 删除符合条件的数据|
|ALTER TABLE \<TABLE> [DROP \| ADD] \<column_name>|删除\|添加字段|
|ALTER TABLE \<TABEL> MODIFY \<column_name> \<new_column_type>|修改字段类型|
|ALTER TABEL \<TABLE> CHANGE \<column_name> \<new_column_name> \<column_type>|修改字段名同时修改类型|

## SQL子句

|SQL子句|描述|
|--|--|
|WHERE \<CLAUSE>|表示判断后跟条件|
|LIKE \<string>|模糊匹配字符串;可以使用%相当于通配符,_代表单个字符,[]匹配其中的一个字符,[^]匹配不在其中的|
|REGEXP \<string>|正则表达式匹配|

## SQL 操作符

|SQL 操作符|描述|
|--|--|
|UNION [DISTINCT \| ALL]|联合显示查询结果,ALL表示显示重复的|
|ORDER BY \<column_name>,... [ASC \| DESC]|对结果排序,DESC 降序|
|GROUP BY \|<column_name>|按条件分组|
|INNER JOIN|内连接,或等值连接,获取两个表中字段匹配关系的记录|
|LEFT JOIN|左连接,获取左表所有记录,即使右表没有对应匹配的记录|
|RIGHT JOIN|右连接,与 LEFT JOIN 相反,用于获取右表所有记录,即使左表没有对应匹配的记录|
