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
# English Version suda_wifi_en.py
import requests
import re
import socket
import time
from datetime import timedelta

# Carrier mapping
CARRIER_MAP = {
    "@xyw": "Campus Network",
    "@zgyd": "China Mobile",
    "@cucc": "China Unicom",
    "@ctc": "China Telecom"
}

CARRIER_SUFFIX = {
    "1": ("Campus Network", "@xyw"),
    "2": ("China Mobile", "@zgyd"),
    "3": ("China Unicom", "@cucc"),
    "4": ("China Telecom", "@ctc")
}

def get_local_ip():
    """Get current device IP"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except:
        return "Unknown IP"

def parse_login_status(html_content):
    """Parse login status"""
    status = {
        "current_ip": "Unknown",
        "login_account": "",
        "carrier": "",
        "online_time": "0s",
        "is_login": False,
        "is_login_page": "Login Page" in html_content
    }
    
    # Extract IP
    ip_match = re.search(r'(v4ip=\'|ss5=")([\d.]+)', html_content)
    if ip_match:
        status["current_ip"] = ip_match.group(2)
    
    # Extract account and carrier
    uid_match = re.search(r'uid=\'([^\']+)\'', html_content)
    if uid_match:
        full_account = uid_match.group(1)
        for suffix, name in CARRIER_MAP.items():
            if full_account.endswith(suffix):
                status["login_account"] = full_account.replace(suffix, "")
                status["carrier"] = name
                status["is_login"] = True
                break
    
    # Extract online time
    oltime_match = re.search(r'oltime=(\d+)', html_content)
    if oltime_match and status["is_login"]:
        try:
            status["online_time"] = str(timedelta(seconds=int(oltime_match.group(1))))
        except:
            pass
    
    # Login page check
    if status["is_login_page"]:
        status["is_login"] = False
    
    return status

def check_login_status(session):
    """Check login status"""
    try:
        response = session.get("http://10.9.1.3", timeout=10)
        return parse_login_status(response.text)
    except:
        return {"is_login": False, "is_login_page": True}

def logout(session, current_ip, account_with_suffix):
    """Perform logout"""
    try:
        # Unbind MAC
        unbind_url = "http://10.9.1.3:801/eportal/"
        unbind_params = {
            "c": "Portal", "a": "unbind_mac", "callback": "dr1003",
            "user_account": account_with_suffix, "wlan_user_mac": "000000000000",
            "wlan_user_ip": current_ip, "jsVersion": "3.3.3"
        }
        session.get(unbind_url, params=unbind_params, timeout=10)
        
        # Perform logout
        logout_url = "http://10.9.1.3:801/eportal/"
        logout_params = {
            "c": "Portal", "a": "logout", "callback": "dr1004",
            "login_method": "1", "user_account": "drcom", "user_password": "123",
            "ac_logout": "1", "wlan_user_ip": current_ip, "wlan_user_mac": "000000000000",
            "jsVersion": "3.3.3"
        }
        session.get(logout_url, params=logout_params, timeout=10)
        
        # Clear session and verify
        session.cookies.clear()
        # Wait for logout status change, up to 5 seconds
        start_time = time.time()
        while True:
            status = check_login_status(session)
            # After logout, should be login page
            if status.get("is_login_page", False):
                return True
            if time.time() - start_time > 5:
                return False
            time.sleep(0.3)
    except:
        return False

def login(session, account, carrier_suffix, current_ip, password):
    """Perform login"""
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
        # Wait for login status change, up to 5 seconds
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
    print("===== SUDA_WiFi Campus Network Login v0.1 =====")
    session = requests.Session()
    
    # Check login status
    print("\nChecking current login status...")
    status = check_login_status(session)
    
    # Already logged in
    if status["is_login"]:
        print("\nAlready logged in:")
        print("Current IP: {}".format(status['current_ip']))
        print("Login Account: {}".format(status['login_account']))
        print("Carrier: {}".format(status['carrier']))
        
        # Logout confirmation
        account_suffix = [k for k, v in CARRIER_MAP.items() if v == status["carrier"]][0]
        account_with_suffix = "{}{}".format(status['login_account'], account_suffix)
        
        logout_choice = input("\nDo you want to logout? (y/n): ").strip().lower()
        if logout_choice == "y":
            print("Logging out...")
            if logout(session, status["current_ip"], account_with_suffix):
                print("✅ Logout successful!")
            else:
                print("❌ Logout failed, please try again")
        else:
            print("Logout cancelled")
        return
    
    # Not logged in
    print("\nNot logged in, entering login process")
    
    # Select carrier
    print("\nPlease select carrier:")
    print("1. Campus Network")
    print("2. China Mobile")
    print("3. China Unicom")
    print("4. China Telecom")
    carrier_choice = input("Please enter your choice (1-4): ").strip()
    while carrier_choice not in CARRIER_SUFFIX:
        carrier_choice = input("Invalid input, please select again (1-4): ").strip()
    carrier_name, carrier_suffix = CARRIER_SUFFIX[carrier_choice]
    
    # Enter account and password
    account = input("\nPlease enter account: ").strip()
    password = input("Please enter password: ").strip()
    
    # Get IP
    current_ip = get_local_ip()
    print("\nCurrent device IP: {}".format(current_ip))
    if current_ip == "Unknown IP":
        current_ip = input("Please enter IP manually: ").strip()
    
    # Perform login
    print("\nLogging in...")
    login_status = login(session, account, carrier_suffix, current_ip, password)
    
    # Login result
    if login_status:
        print("\n===== Login Successful =====")
        print("Current IP: {}".format(login_status['current_ip']))
        print("Login Account: {}".format(login_status['login_account']))
        print("Carrier: {}".format(login_status['carrier']))
        # print("Online Time: {}".format(login_status['online_time']))
    else:
        print("\n❌ Login failed, please check your account, password, or carrier")


import threading

_version_check_result = {"has_update": False}

def version_check_async(VERSION, result_dict):
    """
    Asynchronously check for new version, write result to result_dict
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
        print("\n===== New Version Notice =====\nA new version is available! Please visit to update:\nhttps://github.com/MichaelQian0517/SUDA_WiFi")

def end():
    print("===== SUDA_WiFi Campus Network Login v0.1 =====")
    print()

if __name__ == "__main__":
    # Start version check thread
    version_thread = threading.Thread(target=version_check_async, args=(1, _version_check_result))
    version_thread.start()
    main()
    # Wait for version check to complete
    version_thread.join()
    print_version_update_notice()
    end()