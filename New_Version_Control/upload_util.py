# -*- coding:utf-8 -*-
import os
import utils
import shutil
from shutil import copytree, ignore_patterns
from optparse import OptionParser
import string
import time
import zipfile
import urllib2
from urllib2 import URLError
import threading
import json
import collections

bIsTest = False


def copyAssetBundle(source, dest, copyFiles):
    for fileName in os.listdir(source):
        file_path = os.path.join(source, fileName)
        dest_path = os.path.join(dest, fileName)
        if os.path.isdir(file_path):
            utils.create_dir_if_not_exists(dest_path)
            copyAssetBundle(file_path, dest_path, copyFiles)
        else:
            if not file_path.endswith("meta") and not file_path.endswith("manifest"):
                if not os.path.exists(dest_path):
                    shutil.copyfile(file_path, dest_path)
                    copyFiles.append(dest_path)


def generateDiffList(dest, comment, listPaths, zipNames):
    # svn_ci_look_diff_files(dest, None, comment, listPaths)
    if len(listPaths) == 0:
        utils.Print("无文件差异")
        return
    for i in range(len(listPaths)):
        path = listPaths[i].replace(dest, "").replace("\\", '/')
        if path[0] == '/':
            path = path[1:]
        listPaths[i] = path

    if len(listPaths) > 0:
        # 差异文件的zip压缩
        with utils.pushd(dest):
            zip_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            zipCount = 0
            zipIdx = 100
            zipIdxName = ""
            z = None
            for path in listPaths:
                if path.find(".zip") < 0 and path.find("global_info.json") < 0:  # global_info单独上传..
                    if not z:
                        zipIdxName = zip_name + "-" + str(zipIdx) + ".zip"
                        zipNames.append(zipIdxName)
                        z = zipfile.ZipFile(zipIdxName, 'a', zipfile.ZIP_DEFLATED)
                        zipIdx += 1
                    print("zip", path, zipIdxName)
                    z.write(path)
                    zipCount += 1
                    if zipCount > 100:
                        zipCount = 0
                        if z:
                            z.close()
                        z = None


def getAllZip(zipDir, zipNames):
    for fileName in os.listdir(zipDir):
        file_path = os.path.join(zipDir, fileName)
        if file_path.endswith("zip"):
            zipNames.append(fileName)


def getRemoteConsole():
    # global releaseFabricConsole
    if bIsTest:
        config_hosts_name = "10.10.142.236"
        config_user_name = "ubuntu"
        config_user_passwoard = "zp#14@SVR"
        remote_dir = "/home/ubuntu/gameres/parkour/"
        gateway = "wuqiang@xj.tiaoban.badam.mobi"
    else:
        config_hosts_name = "172.26.8.254"
        config_user_name = "ubuntu"
        config_user_passwoard = "zp#14@GAME"
        remote_dir = "/data/gameres/current/parkour/"
        gateway = "wuqiang@dg.tiaoban.badambiz.com"

    releaseFabricConsole = utils.FabricConsole(config_hosts_name,
                                               config_user_name,
                                               config_user_passwoard,
                                               remote_dir,
                                               gateway)
    return releaseFabricConsole


def upload_zip_to_server(platform, zipName, zipPath):
    # global releaseFabricConsole
    releaseFabricConsole = getRemoteConsole()
    serverPath = platform + "/assetbundle/" + zipName
    zipMd5 = utils.get_file_md5(zipPath)
    zipSize = os.path.getsize(zipPath)
    releaseFabricConsole.http_upload_file(zipPath, serverPath, zipMd5, zipSize)
    releaseFabricConsole.closeConsole()
    releaseFabricConsole.reconnectConsole()
    print("upload zip success ", zipName)
    releaseFabricConsole.http_unzip_file(serverPath)
    print("unzip success ", serverPath)
    releaseFabricConsole.closeConsole()


def unzip_in_server(platform, zipName):
    # global releaseFabricConsole
    releaseFabricConsole = getRemoteConsole()
    serverPath = platform + "/assetbundle/" + zipName
    releaseFabricConsole.http_unzip_file(serverPath)
    print("unzip success ", serverPath)
    releaseFabricConsole.closeConsole()


def checkRemoteAssetBundleCorrect(platform):
    releaseFabricConsole = getRemoteConsole()
    releaseFabricConsole.check_remote_asset_bundle_correct(platform)


def upload_file_to_server(platform, fileName, filePath):
    releaseFabricConsole = getRemoteConsole()
    serverPath = platform + "/assetbundle/" + fileName
    fileMd5 = utils.get_file_md5(filePath)
    fileSize = os.path.getsize(filePath)
    releaseFabricConsole.http_upload_file(filePath, serverPath, fileMd5, fileSize)
    releaseFabricConsole.closeConsole()


def get_dic_from_http_file(platform, fileName):
    releaseFabricConsole = getRemoteConsole()
    serverPath = platform + "/assetbundle/" + fileName
    jsonContent = releaseFabricConsole.get_dic_from_http_file(serverPath)
    releaseFabricConsole.closeConsole()
    return jsonContent


def send_content_to_http_file(content, platform, fileName):
    releaseFabricConsole = getRemoteConsole()
    serverPath = platform + "/assetbundle/" + fileName
    releaseFabricConsole.send_content_to_http_file(content, serverPath)
    releaseFabricConsole.closeConsole()


def get_assetbundle_global_info(file, platform):
    global_info = json.loads(open(file).read(), object_pairs_hook=collections.OrderedDict)
    verify = ""
    asset = global_info['assetVersion']

    if platform == 'android':
        verify = global_info['android_default_vertify_version']
    elif platform == 'ios':
        verify = global_info['ios_vertify_version']

    assert verify and asset > 0

    return verify, asset


def modify_assetbundle_verify_version(file, platform, verify):
    global_obj = json.loads(open(file).read(), object_pairs_hook=collections.OrderedDict)
    if platform == 'android':
        global_obj['android_default_vertify_version'] = verify
    elif platform == 'ios':
        global_obj['ios_vertify_version'] = verify

    with open(file, 'w') as f:
        f.write(json.dumps(global_obj, indent=4))


def modify_local_asset_verify_version(dest, platform, asset, verify):
    app_config = os.path.join(dest, 'build_app_config.json')
    channel_config = os.path.join(dest, 'build_channel_config.json')

    app_config_obj = json.loads(open(app_config).read(), object_pairs_hook=collections.OrderedDict)
    channel_config_obj = json.loads(open(channel_config).read(), object_pairs_hook=collections.OrderedDict)

    if app_config_obj['assetVersion'][platform]['version'] < asset:
        app_config_obj['assetVersion'][platform]['version'] = asset

    if platform == 'android':
        app_config_obj['vertify']['android_default_vertify_version'] = verify

        for cfg in channel_config_obj[platform]:
            if cfg['channel'] == 'channel_default_ar':
                cfg['build_android_info']['versionName'] = verify
                cfg['build_android_info']['versionCode'] = cfg['build_android_info']['versionCode'] + 1
    elif platform == 'ios':
        app_config_obj['vertify']['ios_vertify_version'] = verify
        for cfg in channel_config_obj[platform]:
            if cfg['channel'] == 'appStore_ar_hdf':
                cfg['build_ios_info']['CFBundleShortVersionString'] = verify

    with open(app_config, 'w') as f:
        f.write(json.dumps(app_config_obj, indent=4))
    with open(channel_config, 'w') as f:
        f.write(json.dumps(channel_config_obj, indent=4))


def get_auto_add_version(version):
    first, last = version.rsplit('.', 1)
    return first + '.' + str(int(last) + 1)


# python upload_util.py --platform=IOS --action=upload_to_svn
# python upload_util.py --platform=IOS --action=upload_to_remote
# python upload_util.py --platform=IOS --action=upload_global_info_temp
# python upload_util.py --platform=IOS --action=upload_global_info
# python upload_util.py --platform=IOS --action=upgrade_verify_version


# python upload_util.py --platform=Android --action=upload_to_svn
# python upload_util.py --platform=Android --action=upload_to_remote
# python upload_util.py --platform=Android --action=upload_global_info_temp
# python upload_util.py --platform=Android --action=upload_global_info
# python upload_util.py --platform=Android --action=upgrade_verify_version
if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--platform", action="store", dest="platform", default='IOS')
    parser.add_option("--action", action="store", dest="action", default='upload_to_svn')
    parser.add_option("--comment", action="store", dest="comment", default='patch')
    parser.add_option("--zipName", action="store", dest="zipName", default='')
    parser.add_option("--source", action="store", dest="source", default="cmd")
    (opts, args) = parser.parse_args()

    svnRoot = "svn://local.svn.badam.mobi/NinjaMustDie/"

    src = os.path.abspath(
        os.path.join(os.getcwd(), '..', '..', 'ParkourUnityProject_release', 'AssetBundles', opts.platform + "_Patch"))
    dest = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'AssetBundle', opts.platform))
    destInfoPath = os.path.join(dest, "global_info.json")

    print("upload action: ", opts.action, opts.platform)

    platform = opts.platform.lower()

    if opts.platform == "Android" or opts.platform == "IOS":
        if opts.action == 'upload_to_svn':
            print(opts.source + "\n")
            svnPath = svnRoot + "AssetBundle/" + opts.platform
            utils.svn_checkout_or_update(dest, svnPath)
            print("svn revert and checkout finish")

            copyFiles = []
            copyAssetBundle(src, dest, copyFiles)
            print("diff files ", copyFiles)
            shutil.copyfile(os.path.join(src, "global_info.json"), destInfoPath)
            if copyFiles:
                zipNames = []
                generateDiffList(dest, opts.comment, copyFiles, zipNames)
                print(zipNames)
                if opts.source == "cmd":
                    utils.svn_ci(dest, None, opts.comment)
                else:
                    print("当前平台为web，需要继续2号指令")
        elif opts.action == "upload_to_svn_2":
            print("执行了2号SVN命令")
            print(opts.source + "\n")
            utils.svn_ci_web(dest, None, opts.comment)

        elif opts.action == 'upload_to_remote':
            print(opts.source + "\n")
            zipNames = []
            getAllZip(dest, zipNames)
            unreachableZips = []
            for zipName in zipNames:
                if bIsTest:
                    url = "http://res-test-cdn.nmd.badambiz.com/gameres/" + platform + "/assetbundle/" + zipName
                else:
                    url = "http://ghnmd-sau-res.badambiz.com/gameres/" + platform + "/assetbundle/" + zipName
                isUrlValid = False
                try:
                    response = urllib2.urlopen(url)
                except Exception as e:
                    print("error", e)
                else:
                    response.close()
                    isUrlValid = True
                    print(url, "is valid")
                if not isUrlValid:
                    unreachableZips.append(zipName)
                    print("url is not valid  ", url)
            print("need upload zip:  ", unreachableZips)
            if unreachableZips:
                if opts.source == "cmd":
                    utils.Warning('开始同步?')
                for zipName in unreachableZips:
                    upload_zip_to_server(platform, zipName, dest + "/" + zipName)
                else:
                    print("当前平台为web，需要执行2号指令")
        elif opts.action == "upload_to_remote_2":
            print(opts.source + "\n")
            print("现在执行上传远程的2号指令")
            zipNames = []
            getAllZip(dest, zipNames)
            unreachableZips = []
            for zipName in zipNames:
                if bIsTest:
                    url = "http://res-test-cdn.nmd.badambiz.com/gameres/" + platform + "/assetbundle/" + zipName
                else:
                    url = "http://ghnmd-sau-res.badambiz.com/gameres/" + platform + "/assetbundle/" + zipName
                isUrlValid = False
                try:
                    response = urllib2.urlopen(url)
                except Exception as e:
                    print("error", e)
                else:
                    response.close()
                    isUrlValid = True
                    print(url, "is valid")
                if not isUrlValid:
                    unreachableZips.append(zipName)
                    print("url is not valid  ", url)
            # print("need upload zip:  ", unreachableZips)
            if unreachableZips:
                for zipName in unreachableZips:
                    upload_zip_to_server(platform, zipName, dest + "/" + zipName)

        elif opts.action == "upload_global_info_temp":
            global_online = get_dic_from_http_file(platform, "global_info_temp.json")

            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, json.loads(open(destInfoPath).read()))
            if opts.source == "cmd":
                utils.Warning("确定更新 global_info_temp 吗?")

                upload_file_to_server(platform, "global_info_temp.json", destInfoPath)
                checkRemoteAssetBundleCorrect(platform)
            else:
                print("当前平台为web，需要执行二号指令")
        elif opts.action == "upload_global_info_temp_2":
            print("执行上传temp的2号指令")
            global_online = get_dic_from_http_file(platform, "global_info_temp.json")

            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, json.loads(open(destInfoPath).read()))
            upload_file_to_server(platform, "global_info_temp.json", destInfoPath)
            checkRemoteAssetBundleCorrect(platform)


        elif opts.action == "upload_global_info":
            print(opts.source + "\n")
            global_online = get_dic_from_http_file(platform, "global_info.json")

            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, json.loads(open(destInfoPath).read()))
            if opts.source == "cmd":
                utils.Warning("确定更新 global_info 吗?")

                upload_file_to_server(platform, "global_info.json", destInfoPath)
                checkRemoteAssetBundleCorrect(platform)
            else:
                print("当前平台为web，需要执行2号指令")

        elif opts.action == "upload_global_info_2":
            global_online = get_dic_from_http_file(platform, "global_info.json")
            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, json.loads(open(destInfoPath).read()))
            upload_file_to_server(platform, "global_info.json", destInfoPath)
            checkRemoteAssetBundleCorrect(platform)

        elif opts.action == 'asset_check':
            print(opts.source + "\n")
            checkRemoteAssetBundleCorrect(platform)

        elif opts.action == 'unzip':
            print(opts.source + "\n")
            unzip_in_server(platform, opts.zipName)

        elif opts.action == 'close_maintain':
            global_online = get_dic_from_http_file(platform, "global_info.json")
            global_new = global_online.copy()
            global_new["is_in_maintain"] = 0

            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, global_new)
            utils.Warning("确定关闭维护?")

            send_content_to_http_file(global_new, platform, "global_info.json")

        elif opts.action == 'open_maintain':
            global_online = get_dic_from_http_file(platform, "global_info.json")
            global_new = global_online.copy()
            global_new["is_in_maintain"] = 1

            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, global_new)
            if opts.source == "cmd":
                utils.Warning("确定开启维护?")
                send_content_to_http_file(global_new, platform, "global_info.json")
            else:
                print("当前平台为web,需要执行2号指令")

        elif opts.action == "open_maintain_2":
            global_online = get_dic_from_http_file(platform, "global_info.json")
            global_new = global_online.copy()
            global_new["is_in_maintain"] = 1

            utils.Print("变更内容：")
            utils.PrintJsonDiff(global_online, global_new)
            send_content_to_http_file(global_new, platform, "global_info.json")


        elif opts.action == 'upgrade_verify_version':
            svnPath = svnRoot + "AssetBundle/" + opts.platform
            utils.svn_checkout_or_update(dest, svnPath)

            # read version
            verify, asset = get_assetbundle_global_info(destInfoPath, platform)
            verify_new = get_auto_add_version(verify)
            asset_new = asset + 1

            # modify trunk
            svnBuildConfigPath = svnRoot + 'ParkourUnityProject/Assets/Editor/Scripts/Build/Config'
            buildDest = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'ParkourUnityProject', 'Assets', 'Editor',
                                                     'Scripts', 'Build', 'Config'))
            utils.svn_checkout_or_update(buildDest, svnBuildConfigPath)

            modify_local_asset_verify_version(buildDest, platform, asset_new, verify_new)
            utils.svn_ci(buildDest, 'M', 'auto upgrade ' + platform + ' verify version', True)

            # modify assetbundle
            modify_assetbundle_verify_version(destInfoPath, platform, verify_new)
            utils.svn_ci(dest, 'M', 'auto upgrade ' + platform + ' verify version', True)

            # deploy global_info.json
            global_online = get_dic_from_http_file(platform, "global_info.json")
            global_local = json.loads(open(destInfoPath).read())

            utils.Print("变更内容")
            utils.PrintJsonDiff(global_online, global_local)
            utils.Warning("确定更新 global_info 吗?")

            upload_file_to_server(platform, "global_info.json", destInfoPath)
            checkRemoteAssetBundleCorrect(platform)
