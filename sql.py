import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/testcases?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

#创建表结构
class cases(db.Model):
    __tablename__='cases'
    id = db.Column(db.Integer, primary_key=True)
    case_step = db.Column(db.String(80), unique=True, nullable=False)

def test_sqlalchemy():
    db.drop_all() #仅删除上面创建的表
    db.create_all()  # 创建表 一个类就是一个表

    db.session.add(cases(id=333,case_step='goto  next'))
    db.session.commit()
    sqlres=cases.query.filter(cases.id==333).first()
    print(sqlres.case_step)
    sqlres.case_step='here we go'
    db.session.commit()
    sqlress=cases.query.filter(cases.id==333).first()
    print(sqlress.case_step)
def add_json_case(content):
    data=json.load(content)
    print(data["id"],data["case_step"])
    db.session.add(cases(id=data["id"],case_step=data["case_step"]))
    db.session.commit()
