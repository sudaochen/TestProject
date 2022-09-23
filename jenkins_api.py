import os
import subprocess
# from jenkinsapi.jenkins import  Jenkins
# 
# url="http://127.0.0.1:8080/"
# name="admin"
# password="11315340e35e14f8e4cda4b7f699aa40d6"
# jc=Jenkins(url,name,password)
#
# print(jc.keys())
# 
# jc['test_case_server'].invoke(build_params={"caseid":777})  #参数化发送请求以调起jenkins连接的其他服务

#
#构建时执行cmd命令 pytest XXX.py -k  -v   --allure-dir "./xxx"    alllure server "./XXX" 即可直接通过jenkins启动后续服务

# os.system('curl http://127.0.0.1:5000/testcase_get?id=777')


script="python double_balls.py"


# subprocess.check_call(script,cwd="D:\Myproject\\reward")


s=os.popen(f"cd D:\Myproject\\reward && {script}")
print(s.read().encode(encoding='gbk').decode())