## 环境配置,安装python组件

```bash
pip install scrapy
pip install pymysql
pip install Pillow
```

## 获取程序代码

```bash
git clone git@github.com:codetin/bcy_img.git
cd bcy_img
```



## 修改下载路径配置

```bash
vi scrapy_test/settings.py
```

将  IMAGES_STORE = '/data/pic' 修改为微站的Uploads目录的上一级目录



## 修改数据库配置

```bash
vi scrapy_test/db.py
```

其中conn为抓取程序所用的数据库连接
其中web_conn为微站的数据库连接



## 执行抓取

```bash
scrapy crawl bcy_img
```



## 每日抓取更新数据

```bash
./create_cron.sh
```



## 后续更新时避免覆盖配置文件

```bash
git update-index --skip-worktree  scrapy_test/db.py
git update-index --skip-worktree  scrapy_test/settings.py
```


