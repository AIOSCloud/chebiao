# -*- coding: utf-8 -*-
# @Author   : 王翔
# @微信号   : King_Uranus
# @公众号    : 清风Python
# @GitHub   : https://github.com/BreezePython
# @Date     : 2019/12/15 20:27
# @Software : PyCharm
# @version  ：Python 3.7.3
# @File     : show.py

import sqlite3

db = sqlite3.connect('Car.db')
cur = db.cursor()
cur.execute("CREATE TABLE if not exists image_save (image BLOB);")

with open('Audi.jpg', 'rb') as f:
    cur.execute("insert into image_save values(?)", (sqlite3.Binary(f.read()),))
    db.commit()

cur.execute('select image from image_save limit 1')
b = cur.fetchone()[0]

with open('1.jpg', 'wb') as f:
    f.write(b)
