# -*- coding: utf-8 -*-
# @Author   : 王翔
# @微信号   : King_Uranus
# @公众号    : 清风Python
# @GitHub   : https://github.com/BreezePython
# @Date     : 2019/12/15 20:27
# @Software : PyCharm
# @version  ：Python 3.7.3
# @File     : db_maker.py


import sqlite3
from DBUtils.PooledDB import PooledDB


class DB_Maker:
    def __init__(self):
        self.POOL = PooledDB(
            check_same_thread=False,
            creator=sqlite3,  # 使用链接数据库的模块
            maxconnections=10,
            mincached=2,
            maxcached=5,
            blocking=True,
            maxusage=None,
            ping=0,
            database='database.db',
        )
        self.check_db()

    def check_db(self):
        sql = "SELECT name FROM sqlite_master where name=?"
        if not self.fetch_one(sql, ('idiom',)):
            self.create_table()

    def create_table(self):
        print("create table ...")
        sql = """create table idiom (
                        [id]            integer PRIMARY KEY autoincrement,
                        [name]         varchar (10),
                        [speak]      varchar (30),
                        [meaning]      varchar (100),
                        [source]      varchar (100),
                        [example]      varchar (100),
                        [hot]      int(10)
                    )"""
        self.fetch_one(sql)

    def create_table_by_sql(self, sql):
        self.fetch_one(sql)

    def db_conn(self):
        conn = self.POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def db_close(conn, cursor):
        cursor.close()
        conn.close()

    def fetch_one(self, sql, args=None):
        conn, cursor = self.db_conn()
        if not args:
            cursor.execute(sql)
        else:
            cursor.execute(sql, args)
        record = cursor.fetchone()
        self.db_close(conn, cursor)
        return record

    def fetch_all(self, sql, args):
        conn, cursor = self.db_conn()
        cursor.execute(sql)
        record_list = cursor.fetchall()
        self.db_close(conn, cursor)
        return record_list

    def insert(self, sql, args):
        conn, cursor = self.db_conn()
        row = cursor.execute(sql, args)
        conn.commit()
        self.db_close(conn, cursor)