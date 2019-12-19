# -*- coding: utf-8 -*-
# @Author   : xuchang
# @GitHub   : https://github.com/BreezePython
# @Date     : 2019/12/15 20:27
# @Software : PyCharm
# @version  ：Python 3.7.3
# @File     : db_maker.py
import requests
from string import ascii_uppercase as au
from bs4 import BeautifulSoup
from db_maker import DB_Maker


class Data_Maker:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.create_table_sql = """create table car_info (
                        [id]            integer PRIMARY KEY autoincrement,
                        [name]         varchar (10),
                        [image]      varchar (30),
                        [founded]      varchar (30),
                        [models]      varchar (30),
                        [website]      varchar (30)
                    )"""
        self.insert_sql = "insert into car_info(name,image,founded,models,website) values(?,?,?,?,?)"
        self.query_sql = "SELECT * FROM car_info LIMIT 10"
        pass

    def create_table(self):
        db = DB_Maker()
        sql = """create table car_info (
                                [id]            integer PRIMARY KEY autoincrement,
                                [name]         varchar (10),
                                [image]      varchar (30),
                                [founded]      varchar (30),
                                [models]      varchar (30),
                                [website]      varchar (30)
                            )"""
        print(sql)
        db.create_table_by_sql(sql=sql)

    def query_data(self):
        db = DB_Maker()
        print(db.fetch_one(self.query_sql))

    def make_data(self):
        db = DB_Maker()
        for uppercase in au:
            url = "http://www.chebiaow.com/logo/{}.html".format(uppercase)
            response = requests.get(url=url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            items = soup.select("li .zq")
            for item in items:
                url2 = "http://www.chebiaow.com{}".format(item.attrs['href'])
                response2 = requests.get(url2, headers=self.headers)
                soup2 = BeautifulSoup(response2.content, 'html.parser')
                image = soup2.select(".xq-left>.img>img")[0].get("src")
                name = soup2.select(".xq-right>li>a")[0].get_text()
                founded = soup2.select(".xq-right>li>span")[2].get_text()
                models = soup2.select(".xq-right>li>span")[4].get_text()
                website = soup2.select(".xq-right>li>span")[6].get_text()
                db.insert(self.insert_sql, (name, image, founded, models, website))
        pass
