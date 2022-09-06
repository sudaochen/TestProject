import json

from flask import Flask, escape, request
from flask import session
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/testcases?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
# app.secret_key = 'secretmethod'
#
#
# @app.route('/')
# def hello():
#     word = 'world'
#     print(word)
#     return f'Hello,{word}'
#
#
# @app.route('/login', methods=['post', 'get'])  # 标识需要监听的方法
# def login():
#     res = {
#         "method": request.method,
#         'url': request.path,
#         "args": request.args
#     }
#     session['username'] = request.args.get("name")
#     return res
#
#
# @app.route('/arg/<tmp>')
# def showtmp(tmp):
#     print(tmp)
#     return tmp


# 写一个类处理方式，定义各种访问方式对应的返回结果。添加到被Api封装的app里面作为resource，可以一次性写好api下各种访问方式的对应结果
# class HiWorld(Resource):
#     def get(self):
#         return {'Hi': 'world'}
#
#     def post(self):
#         return 'this is a post'
# api.add_resource(HiWorld, '/hi')  # 对app下/hi地址的get访问全部返回上面的结果
#
#
#
app.config['testcase'] = [{'the first testcase':'xxxxx'},{'the second testcase':'yyyyy'}]
caselist=app.config['testcase']

class TestcaseServer(Resource):
    def get(self):
        try:
            num=int(request.args.get('n'))
            if num>len(caselist):
                return f"out of  range! The total count of cases is {len(caselist)} "
            else:
                print(f'发送第{num}个测试用例')
                return app.config['testcase'][num - 1]
        except:
            return 'please send the request with necessary value'


    def post(self):
        # return request.json
        print(request.json)
        app.config['testcase'].append(request.json)  #flase每次改代码都会重置  所以必须用数据库实现存储
        return {"result":"ok","errcode":"0"}



api.add_resource(TestcaseServer, '/testcase') #对testcase地址下的所有访问执行上述逻辑

class cases(db.Model):
    __tablename__='cases'
    id = db.Column(db.Integer, primary_key=True)
    case_step = db.Column(db.String(80), unique=True, nullable=False)
def add_json_case(data):
#将传入的json格式内容传入cases表格内
    # print(data["id"],data["case_step"])
    db.session.add(cases(id=data["id"],case_step=data["case_step"]))
    db.session.commit()


class Testcasestore(Resource):
    def get(self):
        return 'code for get cases from mysql'
        # abort(404)#abort 返回不同的状态码和默认的错误页
    def post(self):
        #识别上传的json文件
        if "file" in request.files:
            f=request.files['file']
            f.save('./'+f.filename)
            c=open("./"+f.filename, "r")
            data=json.load(c)
            add_json_case(data)
            return "file saved successfully"
        #直接处理json格式数据
        elif "id" in request.json and "case_step" in request.json:
            add_json_case(request.json)


api.add_resource(Testcasestore,'/testcase_store')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 允许外网访问
