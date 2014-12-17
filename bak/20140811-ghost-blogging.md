Title: Ghost Blogging
Date: 2014-08-11 18:28
Slug: ghost-blogging
Tags: ghost, nginx, nodejs

[Ghost](http://docs.ghost.org/) 是基于 [Node.js](http://nodejs.org/) 的博客系统，这个博客就是利用 Ghost 搭建的，详细的介绍就不写了，下面记录下相关的流程，算是备忘

首先肯定是安装 Node.js 环境，由于我用的是 debian 7.5，所以将 Node.js 的 source list 加进来并安装，当然还有 sqlite 3
```
curl -sL https://deb.nodesource.com/setup | sudo bash -
apt-get install nodejs
apt-get install sqlite3
```

接下来就是从 ghost 官网下载最新的压缩包并解压，通过 `npm install --production` 来安装了，但是这个过程中遇到 debian 的 `glib` 版本问题，通过安装 tesing 的 `libc6-dev` 解决
```
echo 'deb http://ftp.debian.org/debian testing main' | sudo tee -a /etc/apt/sources.list
sudo apt-get update
sudo apt-get -t testing install libc6-dev
```

这个时候基本就完工了，修改下 `config.js` 就可以用 `npm start --production` 来启动了

当然如果是需要作为 deamon 来运行的，要用 `forever` 或 `pm2` 这样的工具来执行，我用的是 `pm2` ，安装 `npm install -g pm2` ，运行的话使用 `NODE_ENV=production pm2 start index.js --name ghost` ，这样就可以在 daemon 的情况下启动了

我们一般还习惯用 `nginx` 来做反向代理的，所以安装一下，我默认安装的版本是 1.6.0 ，当然 其他版本的配置也是大同小异，在 `/etc/nginx/conf.d/` 下面创建一个 `ghost.conf` 文件之类的，加上反向代理的配置就可以了，最简单的配置类似这样的
```
server {
    listen       80;
    server_name  vc2tea.com; #这里是域名设置

    location / {
        proxy_pass   http://127.0.0.1:10000; #改成 ghost 的端口号

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}
```

Then , enjoy yourself !