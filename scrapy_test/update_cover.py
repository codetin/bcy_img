#!/usr/bin/env python
#coding=utf-8
# -*- coding: utf-8 -*-
import os,sys

from db import db_conn
from db import web_conn

#更新相册封面
cp666_conn = web_conn()
cursor_cp666 = cp666_conn.cursor()
cursor_cp666.execute("USE cosplay")
try:
    sql = "UPDATE ct_gallery a, ( SELECT gallery_id, pic FROM ct_gallery_detail b   GROUP BY gallery_id) AS b SET a.cover = b.pic WHERE a.id = b.gallery_id"
    result = cursor_cp666.execute(sql)
    cursor_cp666.connection.commit()
    print(result)
except BaseException as e:
    print("mysql daily error>>>>>>>>>>>>>",e,"<<<<<<<<<<<<<error message")
    cp666_conn.rollback()
