# -*- coding: utf-8 -*-
import pymysql 

def db_conn():
    conn = pymysql.connect(
        host = "databro.cn",
        user = "root",
        passwd = "capcom",
        charset = "utf8",
        use_unicode = False
    )
    return conn
