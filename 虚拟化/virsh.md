# virsh

```bash
virsh list # 查看正在运行的vm
virsh list --all # 查看所有vm
virsh start vm_name # 运行vm
virsh shutdown vm_name # 关闭运行中的vm
virsh autostart vm_name # 在宿主机启动时，自动启动vm
virsh dumpxml vm_name # 查看vm详细设置，配合重定向导出到文件 >vm_name.xml
virsh edit vm_name # 编辑vm配置的xml文件
virsh domblklist vm_name # 查看vm的硬盘位置
```

## 迁移虚拟机

以下步骤中，1-4在要导出vm的宿主机1上操作，后面的操作在目标宿主机2上操作

1. 首先关闭正在运行中的虚拟机

    ```bash
    virsh shutdown vm_name
    ```

2. 查看vm挂载的硬盘

    ```bash
    virsh domblklist vm_name
    ```

3. 导出虚拟机配置

    ```bash
    virsh dumpxml vm_name > vm_name.xml
    ```

4. 复制要导出的硬盘和xml文件到目标宿主机

    ```bash
    scp vm_name.xml vm_name.img root@192.168.1.1:/home/kvm
    ```

5. 重新定义vm

    ```bash
    virsh define --file vm_name.xml
    ```

6. 启动并设置自启

    ```bash
    virsh start vm_name && virsh autostart vm_name
    ```

在迁移过程中，要注意前后的vm挂载硬盘位置相同，或者有需要可以在xml 文件中修改磁盘位置
