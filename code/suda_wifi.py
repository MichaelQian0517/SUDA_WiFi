# ===============================================================
# SUDA_WiFi 校园网登录组件/SUDA_WiFi Campus Network Login Component
# 版本/Version: v0.1
# 最新更新/Last Updated: 2025.07.24
# 作者/Author: Michael Qian
# 邮箱/Email: michaelqian0517@gmail.com
# 项目主页/Project: https://github.com/MichaelQian0517/SUDA_WiFi
# 协议/License: Apache License 2.0
# Copyright (c) 2025 Michael Qian. All Rights Reserved.
# 
# 本软件为苏州大学 SUDA_WiFi Linux 登陆组件（Windows/MacOS 亦通用）。
# 仅供学习、研究或个人使用，严禁用于任何违法、违规活动。
# 详细许可信息请参见 LICENSE 文件。
# This software is a Linux login component for Soochow University's SUDA_WiFi (also compatible with Windows/MacOS).
# For learning, research, or personal use only. Strictly prohibited for any illegal or irregular activities.
# For detailed license information, see the LICENSE file.
# ===============================================================
# 中文版本 suda_wifi.py
import requests
import re
import socket
import time
from datetime import timedelta

# 运营商映射关系
CARRIER_MAP = {
    "@xyw": "校园网",
    "@zgyd": "中国移动",
    "@cucc": "中国联通",
    "@ctc": "中国电信"
}

CARRIER_SUFFIX = {
    "1": ("校园网", "@xyw"),
    "2": ("中国移动", "@zgyd"),
    "3": ("中国联通", "@cucc"),
    "4": ("中国电信", "@ctc")
}

def get_local_ip():
    """获取当前设备IP"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "未知IP"

def parse_login_status(html_content):
    """解析登录状态"""
    status = {
        "current_ip": "未知",
        "login_account": "",
        "carrier": "",
        "online_time": "0秒",
        "is_login": False,
        "is_login_page": "登录页" in html_content
    }
    
    # 提取IP
    ip_match = re.search(r'(v4ip=\'|ss5=")([\d.]+)', html_content)
    if ip_match:
        status["current_ip"] = ip_match.group(2)
    
    # 提取账号和运营商
    uid_match = re.search(r'uid=\'([^\']+)\'', html_content)
    if uid_match:
        full_account = uid_match.group(1)
        for suffix, name in CARRIER_MAP.items():
            if full_account.endswith(suffix):
                status["login_account"] = full_account.replace(suffix, "")
                status["carrier"] = name
                status["is_login"] = True
                break
    
    # 提取在线时长
    oltime_match = re.search(r'oltime=(\d+)', html_content)
    if oltime_match and status["is_login"]:
        try:
            status["online_time"] = str(timedelta(seconds=int(oltime_match.group(1))))
        except:
            pass
    
    # 登录页判断
    if status["is_login_page"]:
        status["is_login"] = False
    
    return status

def check_login_status(session):
    """检查登录状态"""
    try:
        response = session.get("http://10.9.1.3", timeout=10)
        return parse_login_status(response.text)
    except:
        return {"is_login": False, "is_login_page": True}

def logout(session, current_ip, account_with_suffix):
    """执行注销"""
    try:
        # 解绑MAC
        unbind_url = "http://10.9.1.3:801/eportal/"
        unbind_params = {
            "c": "Portal", "a": "unbind_mac", "callback": "dr1003",
            "user_account": account_with_suffix, "wlan_user_mac": "000000000000",
            "wlan_user_ip": current_ip, "jsVersion": "3.3.3"
        }
        session.get(unbind_url, params=unbind_params, timeout=10)
        
        # 执行注销
        logout_url = "http://10.9.1.3:801/eportal/"
        logout_params = {
            "c": "Portal", "a": "logout", "callback": "dr1004",
            "login_method": "1", "user_account": "drcom", "user_password": "123",
            "ac_logout": "1", "wlan_user_ip": current_ip, "wlan_user_mac": "000000000000",
            "jsVersion": "3.3.3"
        }
        session.get(logout_url, params=logout_params, timeout=10)
        
        # 清理会话并验证
        session.cookies.clear()
        # 等待注销状态改变，最多5秒
        start_time = time.time()
        while True:
            status = check_login_status(session)
            # 注销后应为登录页
            if status.get("is_login_page", False):
                return True
            if time.time() - start_time > 5:
                return False
            time.sleep(0.3)
    except:
        return False

def login(session, account, carrier_suffix, current_ip, password):
    """执行登录"""
    try:
        full_account = "{}{}".format(account, carrier_suffix)
        login_url = "http://10.9.1.3:801/eportal/?c=ACSetting&a=Login"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "http://10.9.1.3/",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "DDDDD": full_account, "upass": password,
            "R1": "0", "R2": "0", "R3": "0", "R6": "0",
            "para": "00", "0MKKey": "123456", "ISP_select": carrier_suffix,
            "redirect_url": "", "v6ip": "", "wlanuserip": current_ip
        }
        session.post(login_url, headers=headers, data=data, timeout=10)
        # 等待登录状态改变，最多5秒
        start_time = time.time()
        while True:
            status = check_login_status(session)
            if status.get("is_login", False):
                return status
            if time.time() - start_time > 5:
                return None
            time.sleep(0.3)
    except:
        return None

def main():
    print("===== SUDA_WiFi 校园网登录 v0.1 =====")
    session = requests.Session()
    
    # 检查登录状态
    print("\n正在检查当前登录状态...")
    status = check_login_status(session)
    
    # 已登录处理
    if status["is_login"]:
        print("\n检测到已登录状态：")
        print("当前IP：{}".format(status['current_ip']))
        print("登录账号：{}".format(status['login_account']))
        print("运营商：{}".format(status['carrier']))
        
        # 注销确认
        account_suffix = [k for k, v in CARRIER_MAP.items() if v == status["carrier"]][0]
        account_with_suffix = "{}{}".format(status['login_account'], account_suffix)
        
        logout_choice = input("\n是否需要注销？(y/n)：").strip().lower()
        if logout_choice == "y":
            print("正在执行注销...")
            if logout(session, status["current_ip"], account_with_suffix):
                print("✅ 注销成功！")
            else:
                print("❌ 注销失败，请重试")
        else:
            print("已取消注销操作")
        return
    
    # 未登录处理
    print("\n当前未登录，进入登录流程")
    
    # 选择运营商
    print("\n请选择运营商：")
    print("1. 校园网")
    print("2. 中国移动")
    print("3. 中国联通")
    print("4. 中国电信")
    carrier_choice = input("请输入选项(1-4)：").strip()
    while carrier_choice not in CARRIER_SUFFIX:
        carrier_choice = input("输入无效，请重新选择(1-4)：").strip()
    carrier_name, carrier_suffix = CARRIER_SUFFIX[carrier_choice]
    
    # 输入账号密码
    account = input("\n请输入账号：").strip()
    password = input("请输入密码：").strip()
    
    # 获取IP
    current_ip = get_local_ip()
    print("\n当前设备IP：{}".format(current_ip))
    if current_ip == "未知IP":
        current_ip = input("请手动输入IP：").strip()
    
    # 执行登录
    print("\n正在登录...")
    login_status = login(session, account, carrier_suffix, current_ip, password)
    
    # 登录结果
    if login_status:
        print("\n===== 登录成功 =====")
        print("当前IP：{}".format(login_status['current_ip']))
        print("登录账号：{}".format(login_status['login_account']))
        print("运营商：{}".format(login_status['carrier']))
        # print("在线时长：{}".format(login_status['online_time']))
    else:
        print("\n❌ 登录失败，请检查账号密码或运营商")


import threading

_version_check_result = {"has_update": False}

def version_check_async(VERSION, result_dict):
    """
    异步检查是否有新版本，结果写入result_dict
    """
    url = "https://raw.githubusercontent.com/MichaelQian0517/SUDA_WiFi/refs/heads/main/.version_check"
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                if line.startswith("sudawifilinuxpython:"):
                    try:
                        remote_version = int(line.split(":", 1)[1].strip())
                        if remote_version > VERSION:
                            result_dict["has_update"] = True
                    except Exception:
                        pass
    except Exception:
        pass

def print_version_update_notice():
    if _version_check_result.get("has_update"):
        print("\n===== 新版本提醒 =====\n检测到新版本！请访问以更新：\nhttps://github.com/MichaelQian0517/SUDA_WiFi")

def end():
    print("===== SUDA_WiFi 校园网登录 v0.1 =====")
    print()

if __name__ == "__main__":
    # 启动版本检查线程
    version_thread = threading.Thread(target=version_check_async, args=(1, _version_check_result))
    version_thread.start()
    main()
    # 等待版本检查完成
    version_thread.join()
    print_version_update_notice()
    end()