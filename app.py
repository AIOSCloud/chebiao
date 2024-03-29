from flask import Flask, render_template, g
from data_maker import Data_Maker
import sqlite3
import random
import base64

app = Flask(__name__)
DATABASE = 'static/db/database.db'
app.secret_key = 'Breeze Python'


# 数据初始化
def init_db():
    print("数据初始化------")
    data_maker = Data_Maker()
    data_maker.create_table()
    data_maker.make_data()
    data_maker.query_data()
    pass


def connect_db():
    return sqlite3.connect(DATABASE)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def query_db(query, args=()):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    if not query.startswith('select'):
        g.db.commit()
    return rv[0] if rv else None


@app.route('/car')
@app.route('/')
def index():
    id = random.randint(1, 141)
    car_info = query_db('select name,image,founded,models,website from car_info where id={}'.format(id))
    car_info['image'] = car_info['image']
    print(car_info)
    return render_template('index.html', car=car_info)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='127.0.0.1', port=7000)
