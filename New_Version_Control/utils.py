# -*- coding:utf-8 -*-
import os
import shutil
import re
import hashlib
import sys
import json
import socket
import uuid
import traceback
import requests
import gzip
import string
import subprocess
from contextlib import contextmanager
from sys import version_info

import ssl
context = ssl._create_unverified_context()


def isPython3():
    return version_info.major == 3


def os_is_mac():
    return sys.platform == 'darwin'


def os_is_linux():
    return 'linux' in sys.platform


def os_is_win32():
    return sys.platform == 'win32'


def remove_dir_if_exists(d):
    if os.path.isdir(d):
        try:
            shutil.rmtree(d)
        except Exception as e:
            if os_is_win32():
                raise Exception('remove folder [%s] failed' % d)
            elif os_is_mac():
                print('use sudo rm -rf %s' % d)
                os.system('sudo rm -rf %s' % d)

        assert not os.path.isdir(d)


def empty_dir(d):
    remove_dir_if_exists(d)
    create_dir_if_not_exists(d)


def remove_file_if_exists(f):
    if os.path.isfile(f):
        os.remove(f)


def create_dir_if_not_exists(d):
    def _mkdir(dd):
        if os.path.isdir(dd):
            return True
        else:
            d1, d2 = os.path.split(dd)
            if d1 and d2:
                _mkdir(d1)
                os.makedirs(dd)
            else:
                raise Exception('dir error')

    try:
        _mkdir(os.path.abspath(d))
        assert os.path.isdir(d)
    except Exception as e:
        print(e)
        raise Exception('create_dir_if_not_exists [%s] failed' % str(d))


def clear_dir(d):
    assert os.path.isdir(d)
    shutil.rmtree(d)
    os.makedirs(d)


def copy_file_to_base_relative_path(filePath, destBasePath, destRelativePath):
    assert os.path.isfile(filePath)
    assert os.path.isdir(destBasePath)
    listPath = []
    curPath, fileName = os.path.split(destRelativePath)
    while curPath:
        curPath, n = os.path.split(curPath)
        listPath.insert(0, n)

    for d in listPath:
        destBasePath = os.path.join(destBasePath, d)
        create_dir_if_not_exists(destBasePath)

    destFilePath = os.path.join(destBasePath, fileName)
    shutil.copyfile(filePath, destFilePath)
    assert os.path.isfile(destFilePath)
    return destFilePath


def get_cur_file_dir(file=None):
    if file is None:
        if os.path.isfile(__file__):
            file = __file__
        else:
            return os.getcwd()

    assert os.path.isfile(file)
    curDir = os.path.dirname(file)
    return os.path.abspath(curDir)

_tempFileIndex = 0
def get_temp_file_name():
    global _tempFileIndex
    ++_tempFileIndex
    tempFolder = os.path.join(get_cur_file_dir(), 'temp_folder')
    create_dir_if_not_exists(tempFolder)
    return os.path.join(tempFolder, 'temp_file_%d' % _tempFileIndex)


#获取文件 md5 码
def get_file_md5(filePath):
    hashobj = hashlib.md5()
    with open(filePath, 'rb') as f:
        hashobj.update(f.read())
    md5_str = hashobj.hexdigest()
    return md5_str


def get_str_md5(s):
    hashobj = hashlib.md5()
    hashobj.update(s)
    md5_str = hashobj.hexdigest()
    return md5_str


def exec_cmd(cmd, cwd=None):
    if cwd is None:
        cwd = os.getcwd()

    print('\nexec_cmd pwd[%s]:\n%s\n' % (cwd, cmd))

    return subprocess.call(cmd, shell=True, cwd=cwd)


# execute command, and return the output
def execCmd(cmd):
    if os_is_mac() or os_is_linux():
        cmd = string.split(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (result, error) = p.communicate()
    print(result)
    print(error)
    # retcode = p.returncode

    # print result, error
    return result.decode('utf8', 'ignore')


@contextmanager
def pushd(newDir):
    assert os.path.isdir(newDir)

    previousDir = os.getcwd()
    os.chdir(newDir)
    yield
    os.chdir(previousDir)


def Print(s):
    try:
        if isPython3():
            print(s)
        else:
            print(s.decode('utf-8', "ignore"))
    except Exception as e:
        pass
    else:
        pass
    finally:
        pass


def PrintJsonDiff(old_dict, new_dict):
    for key, old_value in old_dict.items():
        new_value = new_dict.get(key, '')
        if old_value != new_value:
            print('\t[' + str(key) + '] ' + str(old_value) + ' --> ' + str(new_value))


def RawInput():
    if isPython3():
        return input()
    else:
        return raw_input()


def Notice(s):
    print('\n\n')
    Print(s)
    print('\n\n')
    Print('按任意键继续')
    RawInput()


def Warning(s):
    print('\n\n')
    Print(s)
    print('\n\n')
    Print('输入 yes 继续')
    result = RawInput()
    if result != 'yes':
        raise Exception('warning not enter yes')


def Alert(msg):
    print('\n\n\n\n\n----------------------------------------------------------------')
    print(msg)
    print('----------------------------------------------------------------\n\n\n\n\n')


def pcall(fun, *args):
    try:
        return fun(*args)
    except Exception as e:
        print(e)
        traceback.print_exc()
    else:
        pass
    finally:
        pass


def match(strList, name):
    for i in strList:
        if re.search(i, name):
            return True


# 将文件夹复制到制定目录下
def copytree(src, dst, filterList=None, ignorList=None, bOnlyFiles=False, bLog = True):
    def _copy(src, dst):
        copyCnt = 0
        # print 'copytree', src, dst
        if not os.path.exists(dst):
            os.makedirs(dst)

        for name in os.listdir(src):
            if filterList is not None:
                if not match(filterList, name):
                    continue
            if ignorList is not None:
                if match(ignorList, name):
                    continue

            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)
            if os.path.isdir(srcname):
                if bOnlyFiles:
                    continue
                copyCnt = copyCnt + _copy(srcname, dstname)
            elif os.path.isfile(srcname):
                if bLog:
                    Print("copy file: %s" % srcname)
                shutil.copy(srcname, dstname)
                copyCnt = copyCnt + 1
        return copyCnt

    return _copy(src, dst)


def copy_file_and_create_dir_if_not_exists(srcBasePath, destBasePath, srcPath):
    srcPath = srcPath.replace('\\', '/')
    srcFilePath = os.path.join(srcBasePath, srcPath)
    assert os.path.isfile(srcFilePath)
    assert os.path.isdir(destBasePath)

    listName = srcPath.split('/')
    for i, fname in enumerate(listName):
        destBasePath = os.path.join(destBasePath, fname)
        if i == len(listName) - 1:
            shutil.copyfile(srcFilePath, destBasePath)
            return srcFilePath, destBasePath
        else:
            create_dir_if_not_exists(destBasePath)


def get_file_md5(filePath):
    hashobj = hashlib.md5()
    with open(filePath, 'rb') as f:
        hashobj.update(f.read())
    md5_str = hashobj.hexdigest()
    return md5_str


config_svn_ci_glags = ('M', '?', '!', 'A', 'D', '~')
def svn_ci(folderPath, flags, comment, diff=False):
    assert os.path.isdir(folderPath)
    assert comment.find('"') == -1, 'comment [%s] not valid' % comment
    assert comment.find("'") == -1, 'comment [%s] not valid' % comment
    if isinstance(flags, str):
        flags = [flags, ]
    elif flags is None:
        flags = config_svn_ci_glags

    for flag in flags:
        assert flag in config_svn_ci_glags

    with pushd(folderPath):
        # os.system('svn up')
        listChanged = []
        svnResult = execCmd('svn status')
        splitResult = None
        if svnResult.find("\r\n") >= 0:
            splitResult = svnResult.split('\r\n')
        elif svnResult.find("\n") >= 0:
            splitResult = svnResult.split('\n')

        if diff:
            execCmd('svn diff -x -U0')

        if splitResult and len(splitResult) > 0:
            for line in splitResult:
                # print line
                if len(line) == 0:
                    continue

                flag = line[0]
                if flag in flags:
                    name = line[8:]
                    if os.path.isfile(name):
                        listChanged.append(name)
                        if flag == '?':
                            os.system('svn add "%s"' % name)
                    elif os.path.isdir(name):
                        listChanged.append(name)
                        if flag == '?':
                            os.system('svn add "%s"' % name)
                    elif flag == '!':
                        listChanged.append(name)
                        os.system('svn delete "%s"' % name)
                    elif flag == '~':
                        listChanged.append(name)
                        os.system('svn revert "%s"' % name)
                        os.system('svn delete "%s"' % name)

        if listChanged:
            for i in range(len(listChanged)):
                path = listChanged[i]
                listChanged[i] = '"' + path + '"'
            cmd = " "
            if isPython3():
                cmd = cmd.join(listChanged)
                cmd = 'svn ci %s -m "%s"' % (cmd, comment)
            else:
                cmd = 'svn ci %s -m "%s"' % (string.join(listChanged, ' '), comment)
            print(cmd)
            Warning("确定提交到svn吗?")
            os.system(cmd)
def svn_ci_web(folderPath, flags, comment, diff=False):
    assert os.path.isdir(folderPath)
    assert comment.find('"') == -1, 'comment [%s] not valid' % comment
    assert comment.find("'") == -1, 'comment [%s] not valid' % comment
    if isinstance(flags, str):
        flags = [flags, ]
    elif flags is None:
        flags = config_svn_ci_glags

    for flag in flags:
        assert flag in config_svn_ci_glags

    with pushd(folderPath):
        # os.system('svn up')
        listChanged = []
        svnResult = execCmd('svn status')
        splitResult = None
        if svnResult.find("\r\n") >= 0:
            splitResult = svnResult.split('\r\n')
        elif svnResult.find("\n") >= 0:
            splitResult = svnResult.split('\n')

        if diff:
            execCmd('svn diff -x -U0')

        if splitResult and len(splitResult) > 0:
            for line in splitResult:
                # print line
                if len(line) == 0:
                    continue

                flag = line[0]
                if flag in flags:
                    name = line[8:]
                    if os.path.isfile(name):
                        listChanged.append(name)
                        if flag == '?':
                            os.system('svn add "%s"' % name)
                    elif os.path.isdir(name):
                        listChanged.append(name)
                        if flag == '?':
                            os.system('svn add "%s"' % name)
                    elif flag == '!':
                        listChanged.append(name)
                        os.system('svn delete "%s"' % name)
                    elif flag == '~':
                        listChanged.append(name)
                        os.system('svn revert "%s"' % name)
                        os.system('svn delete "%s"' % name)

        if listChanged:
            for i in range(len(listChanged)):
                path = listChanged[i]
                listChanged[i] = '"' + path + '"'
            cmd = " "
            if isPython3():
                cmd = cmd.join(listChanged)
                cmd = 'svn ci %s -m "%s"' % (cmd, comment)
            else:
                cmd = 'svn ci %s -m "%s"' % (string.join(listChanged, ' '), comment)
            print(cmd)
            print("提交到svn")
            os.system(cmd)


def svn_checkout_or_update(folderPath, svnPath):
    if os.path.isdir(folderPath):
        cmd = 'svn up'
        with pushd(folderPath):
            os.system(cmd)
    else:
        cmd = 'svn checkout %s %s' % (svnPath, folderPath)
        if isinstance(svnPath, unicode):
            if os_is_win32():
                cmd = cmd.encode('gbk')
            else:
                cmd = cmd.encode('utf8')
        else:
            if os_is_win32() and isinstance(svnPath, str):
                cmd = cmd.decode('utf8').encode('gbk')

        os.system(cmd)


def svn_get_svn_path(folderPath):
    if os.path.isdir(folderPath):
        with pushd(folderPath):
            print(execCmd('svn info'))
            listoutput = execCmd('svn info').split('\n')
            print(listoutput)
            for line in listoutput:
                m = re.match('^URL: (.+)$', line)
                if m:
                    return m.group(1).replace('\r', '')
                    break


def svn_revert_and_update(folderPath):
    assert os.path.isdir(folderPath)
    print(folderPath)
    with pushd(folderPath):
        for line in execCmd('svn status').split('\n'):
            # print line
            if line.startswith('M') or line.startswith('!') or line.startswith('D'):
                name = line[8:]
                exec_cmd('svn revert %s' % name)
            elif line.startswith('A'):
                name = line[8:]
                assert os.path.isfile(name)
                exec_cmd('svn revert %s' % name)
                os.remove(name)
            elif line.startswith('?'):
                name = line[8:]
                if os.path.isfile(name):
                    os.remove(name)
                elif os.path.isdir(name):
                    shutil.rmtree(name)
                else:
                    raise Exception('svn_revert_and_update failed!:%s' % name)


        exec_cmd('svn up')
        assert execCmd('svn status') == ''


def svn_force_revert_or_checkout_update(folderPath, svnPath):
    if svn_get_svn_path(folderPath) == svnPath:
        svn_revert_and_update(folderPath)
    else:
        remove_dir_if_exists(folderPath)
        svn_checkout_or_update(folderPath, svnPath)


class FabricConsole(object):
    index = 1

    def __init__(self, hosts_name, user_name, password, remoteCurDir, gateWay=""):
        super(FabricConsole, self).__init__()
        self._gateWay = gateWay
        self._hostsName = hosts_name
        self._userName = user_name
        self._password = password
        self._remoteCurDir = remoteCurDir
        self._genFabFile()

    def log(self, content):
        print('ssh [%s]:%s' % (self._hostsName, \
            self._fabFilePath and content.replace(self._fabFilePath, 'fab_path') or content))

    def _genFabFile(self):
        self._fabFilePath = '%s_%d.py' % (get_temp_file_name(), FabricConsole.index)
        FabricConsole.index += 1

        print('\n************************************************************************************')
        print('new fabric console')
        print('gate way:[%s]' % self._gateWay)
        print('host name:[%s]' % self._hostsName)
        print('username:[%s]' % self._userName)
        print('remote pwd:[%s]' % self._remoteCurDir)
        print('create temp fabric file:%s' % self._fabFilePath)
        print(os.path.isfile(self._fabFilePath))
        print('************************************************************************************\n')

        templateContent = """#-*- coding: utf-8 -*-
from fabric.api import *
from fabric.context_managers import *
# from fabric.contrib.console import confirm

gatWay = "__GATE_WAY__"
if gatWay:
    env.gateway = gatWay

env.hosts = "__HOST__"
env.user = "__USER__"
env.password = "__PASSWD__"

@task
def upload_file(nativePath, remotePath):
    put(nativePath, remotePath)

@task
def download_file(remotePath, nativePath):
    get(remotePath, nativePath)


@task
def run_unzip_cmd(zipPath, unzipDir):
    run("unzip -o %s -d %s" % (zipPath, unzipDir))


@task
def run_cmd(cmd):
    run(cmd)

@task 
def run_python_cmd(cmd):
    run("python3 %s" % (cmd))"""

        # with open(os.path.join(get_cur_file_dir(), 'fabric_template_file.py'), 'r') as f:
            # templateContent = f.read()
        templateContent = templateContent.replace('__GATE_WAY__', self._gateWay)
        templateContent = templateContent.replace('__HOST__', self._hostsName)
        templateContent = templateContent.replace('__USER__', self._userName)
        templateContent = templateContent.replace('__PASSWD__', self._password)

        with open(self._fabFilePath, 'w+') as f:
            f.write(templateContent)

        assert os.path.isfile(self._fabFilePath)

    def closeConsole(self):
        remove_file_if_exists(self._fabFilePath)

    def reconnectConsole(self):
        self._genFabFile()

    def http_upload_file(self, nativePath, remoteFilePath, md5=None, size=None):
        assert os.path.isfile(self._fabFilePath)
        assert os.path.isfile(nativePath)

        self.log('upload_file [%s]--->[%s]' % (nativePath, remoteFilePath))
        cmd = 'fab -f %s upload_file:%s,%s' % (self._fabFilePath, nativePath, self._remoteCurDir + remoteFilePath)
        if self._isOutPutAborted(execCmd(cmd)):
            return self._retryOP(self.http_upload_file, nativePath, remoteFilePath, md5, size)

        # validate
        if md5 and size:
            tmpF = get_temp_file_name()
            self.http_download_file(remoteFilePath, tmpF, md5, size)
            remove_file_if_exists(tmpF)


    def send_content_to_http_file(self, content, remoteFilePath):
        tempFilePath = get_temp_file_name()
        with open(tempFilePath, 'w') as f:
            f.write(content)
        self.http_upload_file(tempFilePath, remoteFilePath)
        remove_file_if_exists(tempFilePath)

    def send_dic_to_http_file(self, dic, remoteFilePath):
        assert isinstance(dic, dict)
        return self.send_content_to_http_file(json.dumps(dic, indent = 4, sort_keys = True), remoteFilePath)

    def http_download_file(self, remoteFilePath, nativePath, md5=None, size=None, bForce=True):
        assert os.path.isfile(self._fabFilePath)
        remove_file_if_exists(nativePath)

        self.log('download_file [%s]--->[%s]' % (remoteFilePath, nativePath))
        cmd = 'fab -f %s download_file:%s,%s' % (self._fabFilePath, self._remoteCurDir + remoteFilePath, nativePath)
        if self._isOutPutAborted(execCmd(cmd)) and bForce:
            return self._retryOP(self.http_download_file, remoteFilePath, nativePath, md5, size, bForce)

        # validate
        assert os.path.isfile(nativePath), 'http_download_file[%s] failed' % remoteFilePath
        if md5 and size:
            print(get_file_md5(nativePath), md5)
            assert get_file_md5(nativePath) == md5
            assert os.path.getsize(nativePath) == size

    def get_content_from_http_file(self, remoteFilePath, bForce=True):
        try:
            temFilePath = get_temp_file_name()
            self.http_download_file(remoteFilePath, temFilePath, None, None, bForce)
            with open(temFilePath, 'r') as f:
                ret = f.read()
            os.remove(temFilePath)
        except Exception as e:
            ret = None

        return ret

    def get_dic_from_http_file(self, remoteFilePath, bForce=True):
        try:
            return json.loads(self.get_content_from_http_file(remoteFilePath, bForce))
        except Exception as e:
            return None

    @staticmethod
    def _isOutPutAborted(output):
        return len(output) > 9 and output[-9:] == 'Aborting.'

    def _retryOP(fun, args):
        self.log('op failed retry')
        return fun(*args)

    # run op
    def http_create_dir(self, remoteDirPath):
        self.log('fab create dir:[%s]' % remoteDirPath)
        cmd = 'fab -f %s run_cmd:"mkdir -p %s"' % (self._fabFilePath, self._remoteCurDir + remoteDirPath)
        print(cmd)
        if self._isOutPutAborted(execCmd(cmd)):
            return self._retryOP(self.http_create_dir, remoteDirPath)

    def http_rm_dir(self, remoteDirPath):
        self.log('fab rm dir:[%s]' % remoteDirPath)
        cmd = 'fab -f %s run_cmd:"rm -r %s"' % (self._fabFilePath, self._remoteCurDir + remoteDirPath)
        output = execCmd(cmd)
        print("fab output  ", output)
        if self._isOutPutAborted(output):
            return self._retryOP(self.http_rm_dir, remoteDirPath)

    def http_rm_file(self, remoteFilePath):
        self.log('fab rm file:[%s]' % remoteFilePath)
        cmd = 'fab -f %s run_cmd:"rm %s"' % (self._fabFilePath, self._remoteCurDir + remoteFilePath)
        if self._isOutPutAborted(execCmd(cmd)):
            return self._retryOP(self.http_rm_file, remoteFilePath)

    def http_unzip_file(self, remoteFilePath):
        self.log('fab unzip file:[%s]' % remoteFilePath)
        unzipDir = os.path.dirname(self._remoteCurDir + remoteFilePath)
        cmd = 'fab -f %s run_unzip_cmd:%s,%s' % (self._fabFilePath, self._remoteCurDir + remoteFilePath, unzipDir)
        print(cmd)
        if self._isOutPutAborted(execCmd(cmd)):
            return self._retryOP(self.http_unzip_file, remoteFilePath)
        return True

    def check_remote_asset_bundle_correct(self, platform):
        self.log('fab check file compelete')
        script_path = self._remoteCurDir + platform + "/assetbundle/check_file_list_compelete.py"
        cmd = 'fab -f %s run_python_cmd:%s' % (self._fabFilePath, script_path)
        outputResult = execCmd(cmd)
        return outputResult


# if __name__ == "__main__":
#     print("main")
#     global releaseFabricConsole

#     config_hosts_name = "10.10.142.236"
#     config_user_name = "ubuntu"
#     config_user_passwoard = "zp#14@SVR"
#     remote_dir = "/home/ubuntu/gameres/parkour/"
#     gateway = "wuqiang@xj.tiaoban.badam.mobi"

#     releaseFabricConsole = FabricConsole(config_hosts_name, 
#                                         config_user_name, 
#                                         config_user_passwoard, 
#                                         remote_dir,
#                                         gateway)
#     releaseFabricConsole.http_check_file_exist("test_dir/temp_folder.zip")
#     # releaseFabricConsole.http_create_dir("test_dir")
#     # local_file = os.path.join(get_cur_file_dir(), 'temp_folder.zip')
#     # releaseFabricConsole.http_upload_file(local_file, "test_dir/temp_folder.zip")
#     # releaseFabricConsole.send_content_to_http_file("------------", "test_dir/temp_folder/hehe.txt")
#     # releaseFabricConsole.http_unzip_file("test_dir/temp_folder.zip")
#     # 
#     # releaseFabricConsole.http_rm_dir("test_dir")