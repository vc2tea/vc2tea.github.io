---
layout: post
title: Django 项目维护记
category: 技术
tags: [django, python, uwsgi, nginx, pip, virtualenv, pillow]
---

近来由于工作需要，所以需要接手几个用 [Django](https://www.djangoproject.com) 编写的网站项目，虽然一直对 [Python](https://www.python.org/) 有好感，但毕竟作为工作上的项目还是真正的第一次接触，其中遇到了一些问题总算花了几天的时间搞清楚了，在此分享一下

### pip 和 virtualenv

[pip](https://pip.pypa.io/en/latest/) 已经作为 Python 的标准包管理工具了，安装自不用说，这里说一下全局配置中的 download cache，创建 `~/.pip/pip.conf` 文件，内容为

	[global]
	download-cache=~/.pip/cache

这样就能在使用 `pip install` 的时候将下载回来的文件缓存起来了，由于我维护的多个系统使用类似的包，这样就省得每次创建新环境的时候重新去下载了

[virtualenv](http://virtualenv.readthedocs.org/en/latest/) 也是大名鼎鼎的虚拟环境工具了，在同一台机器上运行多个环境，为了避免第三方包的冲突，将第三方包的环境隔离出来管理更方便，用处基本上是这几个

	~/.virtualenvs/virtualenv env_name
	source ~/.virtualenvs/env_name/bin/activate
	deactivate


### Pillow

项目中用到的 [Pillow](https://pillow.readthedocs.org/en/latest/) 是替代 PIL 的图片处理工具，在使用过程中发现2个问题

* 我在使用的 debian 7.4 安装 Pillow 过程中遇到 `compile error` 的问题，需要在安装前保证 `sudo apt-get install python-dev python-imaging`

* Pillow 在实际运行中如果无法正常处理 JPEG 图片，后台会报 `decode JPEG` 之类的错误提示，需要先将 Pillow 删除掉，安装 `sudo apt-get install libjpeg8-dev` 后再重新 install Pillow

### nginx + uwsgi

正式环境上的 Django 肯定是不能用 manage.py runserver 的方法去运行的，所以通过通用接口部署到主流的 web server 中是比较合理的方法，本来按照原项目是用 fastcgi + lighttpd 的模式，但折腾了好久都没成，最后用 nginx + uwsgi 的模式终于弄好了

目前用的 uwsgi.ini 文件内容如下，由于目前维护的项目代码不是很规范的 Django 项目结构，也没有 wsgi.py 文件，所以 module 中设置为 django 默认的设置，利用了 /tmp/proj.sock 创建 socket 接口提供给 nginx 调用

最后一个 pythonpath 是发现通过 uwsgi 模式运行起来后居然部分包无法识别，通过打开 debug，最后发现 pythonpath 中缺少这个目录导致的，于是在 uwsgi 配置文件中将这个 pythonpath 手动指定一下，所以建议各位在运行成功前还是打开 debug 模式，以便确实跟踪问题所在

	[uwsgi]
	project-name=proj
	
	chdir=~/projects/%(project-name)/code
	env=DJANGO_SETTINGS_MODULE=%(project-name).settings
	virtualenv=~/.virtualenvs/%(project-name)
	module=django.core.handlers.wsgi:WSGIHandler()
	master=True
	pidfile=/tmp/%(project-name).pid
	socket=/tmp/%(project-name).sock
	vacuum=True
	max-requests=100
	daemonize=/tmp/%(project-name).log
	pythonpath=~/projects/%(project-name)/code/%(project-name)


运行的方法是 `uwsgi --ini uwsgi.ini`

而 nginx 的配置就比较简单了，在 uwsgi_pass 中设置为刚才指定的 sock 文件就可以了

	server {
	    listen   80;
	    server_name www.example.com;
	
	    location / {
	        uwsgi_pass unix:///tmp/proj.sock;
	        include /etc/nginx/uwsgi_params;
	    }
	    
	    # 还有其他的一些 static 的配置
	}

### 静态文件无法加载

部署上 nginx 后，关闭 settings 中的 debug，部分样式脚本等静态文件可能会无法加载，这个时候要注意2点

* debug 关闭后，静态文件是通过 nginx 读取的，关闭前是直接重定向到 python 的第三方包中，所以需要用 `python manage.py collectstatic` 将使用到的第三方静态文件自动拷贝下来，当然为了效率 nginx 上也要做相应的配置
* 生成的 static 目录是否有读取权限？由于设置给 nginx 代理静态文件，所以起码 nginx 用户需要有对 static 及子目录有读取权限，chmod 处理一下

### 网站无法打开

这也是第一次处理 Django 没有注意到的地方，正式部署后只能通过 settings 中 `ALLOWED_HOSTS` 配置的域名才能访问，修改一下配置或在要访问的客户机中在调整一下 hosts 即可