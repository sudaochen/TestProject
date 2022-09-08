import os

# from jenkinsapi.jenkins import  Jenkins
#
# url="http://127.0.0.1:8080/"
# name="admin"
# password="11315340e35e14f8e4cda4b7f699aa40d6"
# jc=Jenkins(url,name,password)
#
# print(jc.keys())

# jc['test_case_server'].invoke(build_params={"caseid":777})

#
#构建时执行cmd命令 pytest XXX.py -k  -v   --allure-dir "./xxx"    alllure server "./XXX"

os.system('curl http://127.0.0.1:5000/testcase_get?id=777')
