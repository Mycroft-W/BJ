virsh llist --all  # 查看虚拟机
virsh shutdown vm_name # 关闭vm
virsh domblklist vm_name	查看磁盘位置
virsh dumpxml vm_name > vm_name.xml 导出配置文件

scp 复制到目标服务器    # 复制xml文件和vd


virsh define --file vm_name.xml # 从文件生成vm
virsh start vm_name && virsh autostart vm_name # 启动并设置自启


mount -o username=JZadmin,password=Jingzhi2021 //192.168.30.38/JZshare /nas
