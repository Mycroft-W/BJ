# Apache 服务

HTML:超文本标记语言

HTTP协议:超文本传输协议

URL:统一资源定位符

*拓展*: URI,统一资源标志符

## Apache 详解

### 概述

Apache 是最流行的 Web 服务器端软件之一,可通过简单 API 扩充,调用 Perl/Python/PHP 等编译器;Apache 以进程为基础结构,消耗资源较多

### 工作模式

Apache 共有3中稳定的 MPM 模式(MPM: 多进程处理模块): prefork, worker, event

* prefork
  在启动初,就预先 fork 一些子进程,然后等待请求;减少创建和销毁进程的开销,但每个子进程都是单线程的,只能处理一个请求
* worker
  使用了多进程和多线程的混合模式,也预先 fork 子进程(少量),但每个子进程会有多个工作线程和一个监听线程,使用线程来处理请求;同时使用 keep-alive 保持线程的存在
* event
  和 worker 模式相似,但 event 模式下每个子进程都有一个管理线程来管理 keep-alive 的线程,在不服务时释放线程,提高了高并发场景下的请求处理能力

|模式|优点|缺点|
|---|---|---|
|prefork|成熟稳定,兼容所有新老模块|资源占用高,不擅长处理高并发请求|
|worker|资源占用少,高并发表现优秀|需要考虑线程安全|
|event|对资源使用进一步优化|需要考虑线程安全|

查看方式:

```bash
httpd -V |grep -i "server mpm"
```

在编译时,通过`--with-mpm=`选项指定

### 相关文件位置

* 配置文件:

  源码安装: PREFIX/etc/httpd.conf(主配置文件)   PREFIX/etc/extra/*.conf(子配置文件)

  rpm 安装: /etc/httpd/conf/httpd.conf
* 网页文件位置:

  源码安装: PREFIX/htdocs/

  rpm 安装: /var/www/html/
* 日志文件位置:

  源码安装: PREFIX/logs/

  rpm 安装: /var/log/httpd/

### 配置文件详解

**注意**: apache 配置文件严格区分大小写

主机环境的基本配置参数:

```txt
ServerRoot /usr/local/apache2                   # apache 主目录
Listen :80                                      # 监听端口
LoadModule php7                                 # 加载的相关模块
User                                            # 用户
Group                                           # 用户组
ServerAdmin                                     # 管理员邮箱
ServerName                                      # 服务器名
ErrorLog "logs/error_log"                       # 服务器错误日志
CustomLog "logs/access_log" common              # 访问记录日志
DirectoryIndex index.html index.php             # 默认网页文件名
Include etc/extra/httpd-vhosts.conf             # 子配置文件
```

主页目录及权限

```txt
DocumentRoot "/usr/local/apache2/htdocs"        # 网页文件存放目录(默认)
<Directory "/usr/local/apache2/htdocs">         # 定义指定目录的权限
    Option Indexes FollowSymLinks               # 设置权限
      # 可使用关键词
      # None 没有任何额外权限
      # ALL 所有权限(除 MultiViews 外)
      # Indexes 浏览权限(没有默认网页文件时,显示目录)
      # FollowSymLinks 允7许软连接到其他目录
      # MultiViews 允许文件名泛匹配(需要手动开启 negotiation 模块)
    AllowOverride None                          # 定义是否允许目录下 .htaccess 文件中的权限生效
      # None 不生效
      # All 所有都生效
      # AuthConfig 只有网页认证的权限生效
    Require all granted (denied)                # 访问控制列表
</Directory>
<IfModule dir_module>                           # 指定访问指定目录时加载页面文件
    DirectoryIndex index.html index.php
<IfModule>
```

## 实验

实验环境: 在搭建好的 LAMP 环境中进行

### Apache 的目录别名

当 apache 接受请求时,在默认的情况下会将 DocumentRoot 目录中的文件发送到客户端,如果想将某一个不在 DocumentRoot 目录中的文件共享到网站上,并希望将它们留在本来位置而不需要进行移动的话,可以通过建立别名的方式将 URL 指向特定的目录

1. 编辑主配置文件

   ```txt
   Include etc/extra/httpd-autoindex.conf            # 开启调用子配置文件
   ```

2. 编辑子配置文件

   ```txt
   # 别名格式: alias 别名 目录(要有/,否则认为是文件)
   alias /icons/ "/usr/local/apache2/icons/"
   <Directory "/usr/local/apache2/icons">
     Options Indexes FollowSymLinks
     AllowOverride None
     Require all granted
   </Directory>
   ```

### Apache 用户认证

Apache 提供了一个对目录进行保护的认证方法

1. 编辑主配置文件

   ```txt
   <Directory "/usr/local/apache2/htdocs/tyepcho/admin>  # 声明要保护的目录
     Options Indexes FollowSymLinks
     AllowOverride All                                   # 开启权限认证文件 .htaccess
     Require all granted
   </Directory>
   ```

2. 在指定的目录下创建权限文件 .htaccess

   ```txt
   AuthName "Welcome to kernel"                          # 提示信息
   AuthType basic                                        # 加密类型
   AuthUserFile /usr/local/apache2/htdocs/typecho/admin/apache.passwd  # 密码文件,文件名自定义(使用绝对路径)
   require valid-user                                    # 允许密码文件中的所有用户访问
   ```

3. 创建密码文件,加入允许访问的用户

   使用 httpd 附带的命令 htpasswd 来创建文件和用户(使用路径调用命令)

   ```bash
   htpasswd -c /usr/local/apache2/htdocs/typecho/admin/apache.passwd test1       # -c 建立密码文件
   htpasswd -m /usr/local/apache2/htdocs/typecho/admin/apache.passwd test2       # -m 添加用户
   ```

4. 重启 apache 服务

   ```bash
   /usr/local/apache2/bin/apachectl -t               # 检查配置文件
   /usr/local/apache2/bin/apachectl stop
   /usr/local/apache2/bin/apachectl start
   ```

### 虚拟主机

虚拟机主机,也叫"网站空间",用一台物理服务器为多个网站提供资源

分类:

* 基于IP的虚拟主机: 使用不同 IP 提供访问接口
* 基于端口的虚拟主机: 使用不同端口提供访问接口
* 基于域名的虚拟主机: 使用不同域名提供访问

1. 域名解析:使用不同域名
2. 网站主页目录规划

   在/hostdocs/ 目录下分别创建目录,并在目录中创建 index.html 文件(写入不同内容)

3. 修改主配置文件

   ```txt
   Include etc/extra/httpd-vhosts.conf               # 开启虚拟主机
   ```

4. 编辑子配置文件,编写虚拟主机标签

   ```txt
   <Directory "/usr/local/apache2/htdocs/sina">
     Options Indexes FollowSymLinks
     AllowOverride None
     Require all granted
   </Directory>
   <VirtualHost 192.168.88.10:80>                    # 虚拟主机标签
     ServerAdmin webmaster@sina.com                  # 管理员邮箱
     DocumentRoot "/usr/local/apache2/htdocs/sina"   # 网站主目录
     ServerName www.sina.com                         # 完整域名
     ErrorLog "logs/sina-error_log"                  # 错误日志
     CustomLog "logs/sina-access_log" common         # 访问日志
   </VirtualHost>
   ```

5. 重启服务,验证结果

   通过不同域名访问网站,查看结果

### 域名跳转

当访问一个域名时,将访问的目标强制换成另一个域名,称为域名跳转

1. 编辑主配置文件加载重写模块

   ```txt
   LoadModule rewrite_module module/mod_rewrite.so       # 加载重写模块
   ```

2. 修改虚拟主机配置文件

   ```txt
   <Directory "/usr/local/apache2/htdocs/DIR">
     Options Indexes FollowSymLinks
     AllowOverride All
     Require all granted
   </Directory>
   ```

3. 创建规则匹配文件

   在指定的网站目录下创建文件 .htaccess,并添加以下内容

   ```txt
   RewriteEngine on                                          # 开启重写功能
   RewriteCond %{HTTP_HOST} ^www.old.com                     # 重写匹配
   RewriteRule ^(.*)$ http://www.new.com/$1 [R=permanent,L]  # 重写目标
   ```

4. 重启服务器并测试

### Apache+openssl 实现 https

超文本传输安全协议(Hypertext Transfer Protocol Secure, HTTPS),即 HTTP 加上 SSL 层,用于安全的 HTTP 数据传输

1. 准备工作

   检查 Apache 是否支持 SSL,存放位置 /usr/local/apache2/modules;检查是否启用

   ```bash
   apachectl -M
   ```

2. CA 证书申请

   ```bash
   openssl genrsa -out ca.key 1024                           # 生成CA私钥
   openssl req -new -key ca.key -out kernel.csr              # 生成待签证书
   openssl x509 -req -days 365 -sha256 -in kernel.csr -signkey ca.key -out kernel.crt        # 对证书进行签名
   ```

3. 修改配置文件

    修改主配置文件

   ```txt
   LoadModule ssl_module modules/mod_ssl.so              # 加载 ssl 模块
   Include etc/extra/httpd-ssl.conf                      # 调用子配置文件
   ```

   修改 httpd-ssl.conf 文件, 调用证书等文件

   ```txt
   SSLProtocol all -SSLv2 -SSLv3                                                   # 支持的 ssl 类型
   SSLCipherSuite HIGH:!RC4:!MD5:!aNULL:!eNULL:!NULL:!DH:!EDH:!EXP:+MEDIUM         # 支持的加密类型
   SSLHonorCipherOrder on                                                          # 开启证书认证
   SSLCertificateFile cert/kernel.crt                                              # 证书位置
   SSLCertificateKeyFile cert/ca.key                                               # 证书私钥
   ```

   添加虚拟主机

   ```txt
   <VirtualHost _default_:443>
     DocumentRoot "/usr/local/apache2/htdocs"
     ServerName local host:443
     SSLCertificateFile cert/kernel.crt
     SSLCertificateKeyFile cert/ca.key
     SSLCertificateChainFile cert/kernel.crt
   </VirtualHost>
   ```

4. 重启,结果验证

   在重启时会报错:"AH00526: Syntax error on line 78 of /usr/local/apache2/etc/extra/httpd-ssl.conf:SSLSessionCache: 'shmcb' session cache not supported (known names: ). Maybe you need to load the appropriate socache module (mod_socache_shmcb?)"

   在主配置文件中加载模块即可

5. 强制跳转 https

   在目录标签中添加跳转信息即可

   ```txt
   <Directory "/usr/local/apache2/htdocs">
     RewriteEngine on
     RewriteCond %{SERVER_PORT} !^443$
     RewriteRule ^(.*)?$ https://%{SERVER_NAME}/$1 [R=301,L]
   </Directory>
   ```

### Apache 日志切割

Apache 自带了一个日志切割工具

1. 设置日志的路径名称

   在主配置文件中添加以下内容

   ```txt
   ErrorLog "logs/error.log"                                                           # 错误日志
   CustomLog "logs/access.log" combined                                                # 访问日志
   LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined   # 日志格式
   LogFormat "%h %l %u %t \"%r\" %>s %b" common                                        # 日志格式
   ```

2. 设置 apache 日志分割

   在主配置文件添加

   ```txt
   ErrorLog "|/usr/local/apache2/bin/rotatelogs -l /usr/local/apache2/logs/error_%Y%m%d.log 86400"             # 错误日志轮替;每天轮替一次
   CustomLog "|/usr/local/apache2/bin/rotatelogs -l /usr/local/apache2/logs/access_%Y%m%d.log 86400" combined  # 访问日志轮替;每天一次
   ```

### 不记录指定文件类型的日志

忽略记录一些图片,js,css等静态对象的访问记录

1. 配置日志文件不记录图片的访问

   在主配置文件添加

   ```txt
   SetEnvIf Request_URI ".*\.gif$" image-request
   SetEnvIf Request_URI ".*\.jpg$" image-request
   SetEnvIf Request_URI ".*\.png$" image-request
   SetEnvIf Request_URI ".*\.bmp$" image-request
   SetEnvIf Request_URI ".*\.swf$" image-request
   SetEnvIf Request_URI ".*\.js$"  image-request
   SetEnvIf Request_URI ".*\.css$" image-request            # 定义图片格式变量
   CustomLog "|/usr/local ... _%Y%m%d.log 86400" combined env=!image-request           # 不记录含有变量的记录
   ```

### Apache 配置静态缓存

让客户端缓存一些静态资源,加速访问

1. 配置静态缓存

   调用静态缓存模块,编写缓存规则

   ```txt
   <IfModule mod_expires.c>
     ExpiresActive on
     ExpiresByType image/gif "access plus 1 days"
     ExpiresByType image/jpeg "access plus 24 hours"
     ExpiresByType image/png "access plus 24 hours"
     ExpiresByType text/css "now plus 2 hours"
     ExpiresByType application/x-javascript "now plus 2 hours"
     ExpiresByType application/javascript "now plus 2 hours"
     ExpiresByType application/x-shockwave-flash "now plus 2 hours"
     ExpiresDefault "now plus 0 min"
   </IfModule>
   ```

   或者,使用 mod_headers 模块也可实现

   ```txt
   <IfModule mod_headers.c>
     # htm,html,txt 类的文件缓存一个小时
     <filesmatch "\.(html|htm|txt)$">
         header set cache-control "max-age=3600"
     </filesmatch>
    
     # css, js, swf 类的文件缓存一个星期
     <filesmatch "\.(css|js|swf)$">
         header set cache-control "max-age=604800"
     </filesmatch>
    
     # jpg,gif,jpeg,png,ico,flv,pdf 等文件缓存一年
     <filesmatch "\.(ico|gif|jpg|jpeg|png|flv|pdf)$">
         header set cache-control "max-age=29030400"
     </filesmatch>
   </IfModule>
   ```

2. 重启服务并验证

   ```bash
   curl -x127.0.0.1:80 'http://www.test.com/image/a.jpg' -I
   ```

### 禁止解析 PHP

对于某些目录设置禁止解析 PHP 文件,防止用户上传有害文件

```txt
<Directory /usr/local/apache2/htdocs/data>
    php_admin_flag engine off 
    <filesmatch "(.*)php">
        Order deny,allow
        Deny from all 
    </filesmatch>
</Directory>
```

## 实验总结

**问题**: 无法通过域名访问

**原因**: 没有进行域名解析

**解决方案**: 在 DNS 服务器中添加记录即可;在实验中如果没有搭建 DNS 服务器,可以将解析记录写在 hosts 文件中
