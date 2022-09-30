import json
import os
import random

from flask import Flask, escape, request, send_from_directory
from flask import session
from flask_cors import *

from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/testcases?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

api = Api(app)  # 如果需要从接口返回字符串等内容，尽量使用原始的路由  这种封装的路由会对内容做二次处理影响使用


# app.secret_key = 'secretmethod'
#
#

@app.route('/welcome')
def firstpage():
    return "WELCOME    TO   ZIIPIN   TEST-CENTER"


@app.route('/login', methods=['post'])
@cross_origin()
def login():
    data = request.get_json()
    print(data)
    user = data["username"]
    pwd = data["password"]
    if user == "admin" and pwd == "123456":
        return "ok"
    else:
        return "no"


@app.route('/op', methods=['get'])
def op():
    return send_from_directory('./', 'train.json', as_attachment=True)


def get_client_ip(request):
    ip = request.remote_addr
    print(ip)
    return ip


@app.route("/ipconfig")
def getip():
    if get_client_ip(request) != "127.0.0.1":
        return "Your ip is not allowed for this url! Please use developer's ip"
    return get_client_ip(request)

    # word = 'world'
    # print(word)
    # gets=request.args
    # if "n" in gets:
    #     print(gets)
    #     return 'OK'
    #
    # else:
    #     return  'false'
    # return f'Hello,{word}'


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
class HiWorld(Resource):
    def get(self):
        return {'Hi': 'world'}

    def post(self):
        return 'this is a post'


api.add_resource(HiWorld, '/hi')  # 对app下/hi地址的get访问全部返回上面的结果,调试基本功能

app.config['testcase'] = [{'the first testcase': 'xxxxx'}, {'the second testcase': 'yyyyy'}]
caselist = app.config['testcase']


# 使用上述基本配置调试基本功能
class TestcaseServer(Resource):
    def get(self):
        try:
            num = int(request.args.get('n'))
            if num > len(caselist):
                return f"out of  range! The total count of cases is {len(caselist)} "
            else:
                print(f'发送第{num}个测试用例')
                return app.config['testcase'][num - 1]
        except:
            return 'please send the request with necessary value'

    def post(self):
        # return request.json
        print(request.json)
        app.config['testcase'].append(request.json)  # flask每次改代码都会重置  所以必须用数据库实现存储
        return {"result": "ok", "errcode": "0"}


api.add_resource(TestcaseServer, '/testcase')  # 对testcase地址下的所有访问执行上述逻辑


# 创建数据库表的模板
class cases(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_step = db.Column(db.String(80), unique=True, nullable=False)


# 将json格式的测试用例传入上面的表
def add_json_case(data):
    # 将传入的json格式内容传入cases表格内
    # print(data["id"],data["case_step"])
    db.session.add(cases(id=data["id"], case_step=data["case_step"]))
    db.session.commit()
#根据主键删除对应数据
def del_json_case(data):
    db.session.delete(cases.query.get(data["id"]))
    db.session.commit()


# 存储用例进入数据库，限定为json文件或者json格式数据
class Testcasestore(Resource):
    def get(self):
        return 'code for get cases from mysql，turn to testcaserun'
        # abort(404)#abort 返回不同的状态码和默认的错误页

    def post(self):
        # 识别上传的json文件  可以使用限制文件名后缀来避免跨站攻击 文件上传漏洞问题
        if "file" in request.files:
            f = request.files['file']
            f.save('./' + f.filename)
            c = open("./" + f.filename, "r")
            data = json.load(c)
            add_json_case(data)  # 也可以直接将文件d f.read()作为data的case_step使用
            return "file saved successfully"
        # 直接处理json格式数据
        elif "id" in request.json and "case_step" in request.json:
            print(request.json)
            if request.json["id"]!='' and request.json["case_step"]!='':
                add_json_case(request.json)
                return "ok"
            else:
                return "No"


# 拉取数据库里面的测试用例

class Testcaseget(Resource):
    @cross_origin()
    def get(self):
        id=request.args.get('id')
        if id=='':
            return 'No'
        else:
            sid=int(request.args.get("id"))
            print(sid)
        if sid==0:
            caseall = cases.query.all()
            # print(caseall[0].case_step)
            caselist=[]
            for item in caseall:
                t = {"id":str(item.id),"case_step":str(item.case_step),"name":"测试数据"}
                caselist.append(t)
            # abort(500)
            print(caselist)
            return caselist
        else:
            try:
                case = cases.query.filter_by(id=sid).first()
                # print(case)
                return [{"id":case.id, "case_step":case.case_step}]
            except:
                # abort(404)
                return "id  doesn't exist"

            # abort(404)
            # return "id must be an integer!"
@cross_origin()
@app.route('/testcase_delete',methods=['post'])
def delete_case():
    pass



@cross_origin()
@app.route('/double_balls',methods=['get'])
def lucky():
    #0代表运势一般，1代表幸运
    value=random.randint(0,1)
    print(value)
    if value==1:
        script = "python double_balls.py"
        s=os.popen(f"cd D:\Myproject\\reward && {script}")
        ss=s.read().encode(encoding='gbk').decode()
        print(ss)
        return ss
    else:
        print('next time')
        return '下次再买彩票吧！'

api.add_resource(Testcasestore, '/testcase_store')  # 通过post传送数据进入数据库
api.add_resource(Testcaseget, '/testcase_get')  # 通过post拉取指定数据
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 允许外网访问
