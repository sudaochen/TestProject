from jenkinsapi.jenkins import  Jenkins

url=""
name=""
password=""
jenkins_connect=Jenkins(url,name,password)

job=jenkins_connect.get_job("")
job.invoke()
print(job.get_last_build())