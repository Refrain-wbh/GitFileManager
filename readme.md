目前来说，分成这样几步来实现：
1. 首先实现服务器端的某个路径下的文件在前端的表格显示，上传下载等。上传暗流和列表在一起，做到文件夹的上传。
2. 其次，实现git的基本存储（实现到commit为止），在前端提供commit选项，进行基本的提交（提交应该是单独的框，因为涉及到写入作者，信息等等。



select控件 似乎是一个很好的东西

路径问题非常关键！目前看起来系统的当前目录是和manage同一级的


目前来说不做分支合并，所以Commit树就是树状的。
每个仓库起始有分支，有默认Commit，
这个网站有很多很好的前端，https://codepen.io/search/pens?q=File+list
有一个非常好看的删除增加的前端：https://codepen.io/NullPointerException/pen/QWwEaq

![image-20220418094757791](C:\Users\HP\AppData\Roaming\Typora\typora-user-images\image-20220418094757791.png)

我们来构思一下写的方式，整体结构就上面这样，然后结合上面的增加删除前端。然后左侧是整个项目的一个目录结构，不动。只是为了展示，右侧是文件和文件夹的详细信息，可以上传下载什么的。

![image-20220418095012529](C:\Users\HP\AppData\Roaming\Typora\typora-user-images\image-20220418095012529.png)

这个东西可以放到靠下的位置，或者没有？因为左侧已经有了充分的目录显示了。

然后在上端设置一个select控件，最好带有删除按钮，就是用来管理和切换branch的。（这个是放在上面的，三个控件？选择分支，删除当前分支，查看history）

然后设置一个目录，可以用来同步本地和远程。  然后再来一个commit按钮表示提交。这些按钮可以放到和

![image-20220418100021497](C:\Users\HP\AppData\Roaming\Typora\typora-user-images\image-20220418100021497.png)

平行。因为他属于这个目录的东西。

在查看历史commit 的时候，以列表的形式展示，然后每个列表有commit的一些细节，然后有两个按钮，一个是回退版本，另一个是增新建分支。新建分支就直接跳转到这个分支了。

注意到大部分函数都要传递store参数，所以可以根据User是否拥有Store来决定