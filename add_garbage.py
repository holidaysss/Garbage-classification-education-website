import re
from models import Garbage
from extra import db
from flask import Flask, render_template, request, redirect, url_for, session
import config


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

if __name__ == '__main__':
    text = ' 报纸 纸箱 书本 纸袋 塑料瓶 玩具 油桶 ' \
           '乳液罐 食品保鲜盒 衣架 酒瓶 玻璃杯 易拉罐 锅 螺丝刀 皮鞋 衣物 包 毛绒玩具 电路板 砧板 插座 '
    result = re.findall(r' (.*?) ', text)
    print(result)
    for i in result:
        garbage = Garbage(name=i, code_id=1, code_name='可回收物')
        db.session.add(garbage)
    db.session.commit()