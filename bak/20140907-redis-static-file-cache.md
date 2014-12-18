Title: 用 Redis 缓存静态文件
Date: 2014-09-07 00:46
Slug: redis-static-file-cache
Tags: redis, cache

一般网站为了缓解服务器的资源消耗，会将一些包含动态内容并且访问量特别大的页面（比如首页），采用静态化的手段来进行优化。

最传统的做法就是通过定期执行的后台进程，将动态内容抓取出来，生成一个 html / inc 文件存放在文件系统中，然后在首页中用各种语言的 include 语法将静态的内容包含进去。

这种做法存在以下几个问题：

* include 静态文件，一旦文件不存在，页面往往会直接报错
* 随着网站的发展，这些生成的小文件可能会越来越多，同时旧的小文件也可以有些直接被废弃掉了，管理这些小文件难度大
* 当服务器不只一台的情况下，这些小文件还需要考虑实时同步的问题

### 解决方案

没错，还是利用 Redis，聪明的朋友可能一下子就能想到为什么了，不过还是让我详细再说明下吧。

1. 还是采用后台程序将动态的内容静态化，但是这次静态化的目标不是生成静态文件，而是将静态文件的内容保存在 Redis 中
2. 给生成的 Redis 内容加上一个合理的生存期，比如这个静态内容是每天生成的，可以设置生存期为5天，如果这个内容确实是活的话，那进程会一直保证这个内容是存在的，一旦进程被废弃掉了，内容在5天后也会自动被清理掉，无需人工干预
3. 页面中不再采用 include 的方式，而是直接读取对应 Redis 的内容并拼接在原页面内容中，当 Redis 的内容不存在时返回空字符串，这样页面最多只会留空没有内容的位置，而不会导致整个页面报错

当然这样直接就解决了服务器文件同步的问题了，并且由于是基于内存读取，比起读取文件IO的效率又进一步提升了。