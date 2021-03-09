# ansible

自动化运维工具,提供了大量的模块实现了大量的功能

## ansible 特性

1. 支持local,ssh,zeromq 三种连接方式被管理端,默认使用ssh
2. 被管理端无需安装agent
3. 对主机进行分类
4. 可以通过playbooks编辑剧本

## ansible 配置文件

/etc/ansible/ansible.cfg    # 主配置文件
/etc/ansible/hosts          # 主机清单
/etc/ansible/roles/         # 角色目录

## ansible 免密管理

1. 使用 ssh 生成密钥对

   ```bash
   ssh-keygen
   ```

2. 拷贝公钥到被管理的主机

   ```bash
   ssh-copy-id <hosts>
   ```

## ansible 命令

格式: ansible \<host-pattern> [-m module_name] [-a args]

例如: ansible all -m ping

常用选项:
|选项|描述|
|--|--|
|-m MOUDLE_NAME, --module-name=MODULE_NAME|选择模块,默认为command|
|-a MOUDLE_ARGS, --args=MOUDLE_ARGS|模块参数|
|-u REMOTE_USER, --user=REMOTE_USER|连接的用户名,默认为root,在ansible.cfg中配置|
|-k, --ask-pass|提示输入 ssh 登录密码|
|-U SUDO_USER, --sudo-user=SUDO_USER|sudo 的用户,默认为root|
|-K, --ask-sudo-pass|提示输入 sudo 密码|
|-B SECONDS, --background=SECONDS|异步执行,X秒后失败|
|-C, --check|测试,不真正执行|
|-c CONNECTION|连接类型|
|-f FORKS, --forks=FORKS|fork 多个进程并发处理,默认5|
|-o, --one-line|输出摘要|

## ansible 执行流程

1. 加载主配置文件/etc/ansible/ansible.cfg
2. 加载模块文件,如command
3. 通过ansible将命令生成对应的临时py文件,并传输至被管理主机$HOME/.ansible/tmp/ansible-tmp-\<n/xxx.py>
4. 给文件添加 x 权限, 执行
5. 返回结果
6. 删除临时py文件,sleep 0 退出

## ansible 常用模块

|模块|描述|
|ping|检查节点主机是否能连通|
|yum|包管理,red hat系|
|copy|文件复制|
|file|文件操作|
|service|服务管理|
|user|用户管理|
|group|用户组管理|
|cron|计划任务|
|template|模板|
|setup|主机配置|
|fetch|拉取文件|
|apt|包管理,debian系|
|command|执行命令,默认模块|
|shell|调用shell执行命令|
|script|本地脚本|
