# -*- coding: utf-8 -*-
import pymysql 

#每日数据抓取的连接配置,不用修改
def db_conn():
    conn = pymysql.connect(
        host = "databro.cn",
        user = "root",
        passwd = "capcom",
        charset = "utf8",
        use_unicode = False
    )
    return conn

#微站的数据库连接配置
def web_conn():
    conn = pymysql.connect(
        host = "databro.cn",
        user = "root",
        passwd = "capcom",
        charset = "utf8",
        use_unicode = False
    )
    return conn