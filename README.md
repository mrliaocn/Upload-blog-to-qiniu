## Upload-blog-to-qiniu

因为想将自己的博客部署到七牛上，由于是静态的，所以需要在部署的时候保持文件结构不变。因此用Python写了一个用来上传的小工具。

使用的是PyQt5做的界面。还挺有意思的。

### Usage

#### For All System:

```
pip install qiniu, pyqt5

```

```
python qiniu_up.py
```


#### Only for Windows system:

1. install pywin32 from [HERE](https://sourceforge.net/projects/pywin32/files/pywin32/Build%20221/).

2. install pyinstaller

```
pip install pyinstaller
```

3. build

```
pyinstaller -F -w -i image.ico qiniu_up.py
```

4. ./dist/qiniu_up.exe

### Update

Fixed the bug that progress bar did not response with multi-thread.
