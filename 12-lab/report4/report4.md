
# lab11: 网络防火墙与入侵检测技术
- 配置 Windows 防火墙的安全策略并进行验证, 要求多次变更安全策略, 分析比较不同安全策略下的防护效果
- 将相关配置及验证结果界面截图并写入实验报告中

## 11.1 Windows 内置防火墙配置实验
- 通过出站规则禁止某程序(chrome.exe), 使得其无法联网/工作
- 通过出站规则禁止某协议(ICMPv4), 观察其影响
- 通过出站规则禁止 tcp 某端口号(port 25), 来观察其影响

### 禁止应用
选择 msedge.exe
![forbid](https://i.imgur.com/7ZkV5lI.png)

限制连接(注意要设置出站, 因为浏览器这里作为客户端)
![forbid](https://i.imgur.com/Jo5t5kg.png)
![forbid](https://i.imgur.com/3h1Ktg3.png)

可以看到浏览器无法访问baidu (注意这里可能要关闭全局代理)
![fail](https://i.imgur.com/jZTsLCZ.png)

修改规则为允许
```
![allow](https://i.imgur.com/HlUwpLf.png)
```

此时可以访问
![ok](https://i.imgur.com/WQpGCRL.png)

### 禁止 ICMPv4
通过阻止 ICMPv4 报文出站, 从而阻止本机 ping 通其他机器
![ping](https://i.imgur.com/BDZ5mjk.png)

此时 ping 的结果是
![fail-ping](https://i.imgur.com/kOzSthk.png)

改回来
![back](https://i.imgur.com/C4ijqru.png)

### 禁止 tcp 端口

![tcp25](https://i.imgur.com/7ikTuWs.png)

尝试连接
![try-smtp](https://i.imgur.com/WDppTqk.png)

删除规则,  能够连接
![back](https://i.imgur.com/1TnKvdJ.png)

## 11.2 snort 的安装与使用

- 安装 WinPcap 软件.
- 安装 snort 软件.
- 完善 snort 配置文件  snort.conf, 包括: 设置  snort  的内, 外网检测范围; 设置监测包含的规则.
- 配置 snort 规则.
- 尝试一些简单攻击, 使用控制台查看检测结果.
- 将每种攻击的攻击界面, snort  检测结果截图写入实验报告中.

<!-- TODO -->
![fail](https://i.imgur.com/aeDWiYU.png)

# lab12 文件安全

## 12.1 任意文件读取漏洞以及演示

点编辑然后抓包
![img](https://i.imgur.com/rmRhp8y.png)


D 盘搞一个文件)
![d](https://i.imgur.com/tgbWKBQ.png)
<!-- ![d](https://i.imgur.com/PVRFtHX.png) -->


不停回溯父级目录就能访问到这个文件
![a](https://i.imgur.com/FLC99oN.png)
![b](https://i.imgur.com/j1GbdxJ.png)

从而实现任意的文件读取

## 12.2 任意文件删除漏洞以及演示

假装进行一个代码审计发现了
```php
public function delbackdb(){
    //  接收filename GET 参数
    $filename = trim($_GET['filename']);
    //判断值真假
    if(!$filename){
            //如果没有
            rewrite::js_back('备份文件不存在');
    }
    //进入delOne
    $this->delOne($filename);
    addlog('删除数据库备份文件');
    rewrite::succ('删除成功');
}
```

那么就可以构造一个链接, 直接能删除文件
```
http://www.delredfile.com/admin.php?m=backdb&a=delbackdb&filename=../../../../../../1.txt
```

深藏功与名
![delete](https://i.imgur.com/uA1NlUH.png)
![none](https://i.imgur.com/wNw05WT.png)


第二个案例类似, 构造链接如下
```
http://www.74cms.com/admin/admin_article.php?act=del_img&id=1&img=../../../../../../../1.txt
```

结果
![delete](https://i.imgur.com/b2dMQHw.png)
![none](https://i.imgur.com/wNw05WT.png)

## 12.3 文件包含漏洞原理以及演示


梅开三度,写一个文件
![a](https://i.imgur.com/Hvr2gfC.png)

尝试执行其中的代码
```
<?php phpinfo();?>
```

然后通过相对目录访问文件
![dir](https://i.imgur.com/oit2Av9.png)

可以看到不断加 ../ 最终到达了 D 盘根目录, 成功把 1.txt 里面的内容包含进来执行, 看到了 php 的一些信息
![php](https://i.imgur.com/ISofxVq.png)


另外, 到 D:\phpstudy_pro\WWW\www.wailian2.com 这个目录新建一个 1.txt, 通过访问 wailian2.com 能读取文件内容
![read](https://i.imgur.com/3iAr8gO.png)


然后回到 dvwa 直接重定向 url 也能执行
![url](https://i.imgur.com/hdQJOjE.png)


## 12.4 任意文件上传漏洞原理以及演示

### low 难度

桌面搞一个 1.php
![php](https://i.imgur.com/89aPXKj.png)

然后直接上传
![uplaod](https://i.imgur.com/ylDuBpe.png)
![upload](https://i.imgur.com/wqAbVnw.png)

然后访问链接就能执行
![exec](https://i.imgur.com/YLvHdOf.png)

### medium 难度


burpsuite 抓包, 修改 Content-type
![con-type](https://i.imgur.com/lq3LbhV.png)

改成 image/jpeg,  然后就能上传成功

![ok](https://i.imgur.com/o32Vn8S.png)
说明服务端没有判断文件后缀, 而是判断文件类型

# lab13 高阶网络攻防练习

## 13.1 spring boot Actuator 常见漏洞

配好环境, 运行项目


env 和 trace 都造成的信息泄露
<!-- TODO: 8080 没开 -->


可以直接用 python 开一个 web 服务器
![py](https://i.imgur.com/wgzNQnL.png)
<!-- ![pyweb](https://i.imgur.com/lwO9EeZ.png) -->

## 13.2 外链安全风险漏洞原理以及演示

寻找外链
![link](https://i.imgur.com/ewgBEKc.png)


对应路径处放一个一个 js 脚本
![js](https://i.imgur.com/NPGkLNq.png)

当有用户访问时就会执行, 可替换为其他恶意代码进行攻击
![alert](https://i.imgur.com/BHPl4Lt.png)




## 13.3 第三方安全漏洞原理以及演示

### fastjson 反序列化漏洞

执行某 bat 脚本
![bat](https://i.imgur.com/YSsrPhh.png)


<!-- TODO -->


打开靶场
![fastbar](https://i.imgur.com/DKN7lN0.png)

```java
import java.lang.Runtime; 
import java.lang.Process; 
 
public class test { 
    static { 
        try { 
                Runtime rt = Runtime.getRuntime(); 
                String[] commands = {"notepad.exe"}; 
                Process pc = rt.exec(commands); 
                pc.waitFor(); 
        } catch (Exception e) { 
                // do nothing 
        } 
    } 
}
```


### shiro 反序列化漏洞
