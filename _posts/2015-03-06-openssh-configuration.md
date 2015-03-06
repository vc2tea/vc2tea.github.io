---
layout: post
title: OpenSSH 安全配置备忘
category: 运维
tags: [openssh, sa]
---

下面是基于 Ubuntu Server 14.04 的 OpenSSH 配置说明，其他发行版的应该是类似的


默认 ubuntu 是没有安装 openssh-server 的，首先安装 `sudo apt-get install openssh-server` 

安装好以后就自动启动了，此时默认运行的端口在 22，简单的话通过 `ssh {user}@{host}` 的方法就能远程访问了，当然为了保证安全性，建议做两件事，一是将默认端口改掉，二是只允许通过密钥连接，禁止输入用户名密码直接登录

在服务器修改上面2点的配置以前，我们可以先在客户端执行 `ssh-keygen`，根据具体的提示生成 RSA 的密钥对，最简单的就是一路回车

将生成的公钥 `id_rsa.pub` 放到服务器需要登录的用户验证文件中，一般为 `/home/{user}/.ssh/authorized_keys`，可以将内容 `cat id_rsa.pub >> authorized_keys`，或者直接在客户端中执行 `ssh-copy-id -i id_rsa.pub {user}@{host}`，在默认的配置下客户端自动在服务器上生成相应的文件，记得客户端保留好私钥

完成上面这步以后，可以修改服务器上的 `/etc/ssh/sshd_config` 文件了，重要的部分设置如下

	Port 1022 #端口设置变更 **重要**
	
	PermitRootLogin no #禁止用root进行登录
	RSAAuthentication yes
	PubkeyAuthentication yes
	
	ChallengeResponseAuthentication no
	PasswordAuthentication no #不允许通过密码登录 **重要**
	UsePAM no
		
重启服务 `sudo service ssh restart`

Done！至此就可以在客户端直接通过私钥进行访问了