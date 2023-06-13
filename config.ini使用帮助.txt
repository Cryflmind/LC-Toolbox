本程序允许使用config.ini文件对程序进行个性化
当前提供的参数如下：
[musicLoadingAddress]：背景音乐的存储路径，程序将在启动时进行预加载，可以使用相对路径或绝对路径
格式：
[musicLoadingAddress]=存储音乐文件的文件夹路径，其中音乐请使用mp3格式，否则无法识别
默认：
[musicLoadingAddress]=.\datas\example music

注：如果因为错误修改导致config.ini文件出现问题，导致程序出错，请使用程序文件夹中附带的configMaker.exe进行修复，该程序将会在开始菜单中自动添加