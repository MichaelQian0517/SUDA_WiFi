# SUDA_WiFi Linux 登陆组件 Login Component

> 版本号：v0.1
> 更新时间：2025.07.24

## 简介 Introduction

本软件为苏州大学SUDA_WiFi Linux登陆组件（Windows/MacOS亦通用）。部分Linux设备可能因各种原因，无法使用可视化界面，或可视化界面过于麻烦，导致进行SUDA_WiFi认证时存在困难。本软件在纯命令行界面下实现苏州大学WiFi登陆认证。

This software is a Linux login component for Soochow University's SUDA_WiFi (also compatible with Windows/MacOS). Some Linux devices may have difficulty authenticating with SUDA_WiFi due to various reasons, such as inability to use a visual interface or cumbersome visual interface operations. This software implements Soochow University WiFi login authentication in a pure command-line interface.

## 使用方法 Usage Instructions

### 快速开始 Quick Start

本软件仅提供Python源码，直接运行Python源码即可。

This software only provides Python source code, which can be run directly.

在 [`code`](./code) 文件夹中存在 [`suda_wifi.py`](./code/suda_wifi.py) 和 [`suda_wifi_en.py`](./code/suda_wifi_en.py) 两个Python文件，两者功能上没有任何差异，前者为中文版本，后者为英文版本，请按需使用。（如果您的Linux设备无法正常加载中文，请使用英文版本）。

There are two Python files in the [`code`](./code) folder: [`suda_wifi.py`](./code/suda_wifi.py) and [`suda_wifi_en.py`](./code/suda_wifi_en.py). They have identical functionality; the former is the Chinese version, and the latter is the English version. Please choose as needed. (If your Linux device cannot properly display Chinese, please use the English version.)

运行时，将文件下载至Linux设备中，直接使用Python运行 `.py` 文件即可，例如：

To run the software, download the file to your Linux device and run the `.py` file directly using Python, for example:

```bash
python "./code/suda_wifi.py"
```

运行前可能需要下载 `requests` 库，但此库在大多数情况下应该是已经被下载好的，无需再下载，如果提示缺少，请使用 `pip` 或 `conda` 安装，如： `pip install requests` 。

You may need to install the `requests` library before running, but this library is usually pre-installed and no additional installation is required. If you receive a missing library prompt, install it using `pip` or `conda` , such as:  `pip install requests`.

### 软件功能 Software Features

本软件提供以下功能：

1. 监测当前登陆状态
2. 登陆苏大WiFi账号
3. 退出（注销）苏大WiFi账号

This software provides the following features:

1. Check current login status
2. Log in to SUDA WiFi account
3. Log out (deregister) from SUDA WiFi account

### 功能使用 Using the Features

运行软件后，软件会自动监测当前登陆状态。

After running the software, it will automatically check the current login status.

如果已经登陆，会显示登陆信息，随后询问是否需要注销账号，输入 `y` 或 `n` 即可 “确认” 或 “取消” 。

If already logged in, it will display login information and then ask if you want to log out. Enter `y` or `n` to "confirm" or "cancel".

如果未登陆，即可登陆，请先选择运营商（ `1` 至 `4` 的数字），再输入账号密码，即可登陆。

If not logged in, you can log in by first selecting an operator (numbers `1` to `4`), then entering your account and password.

如果本软件有新版本，会有系统提示，您可以及时更新新版本。

If a new version of the software is available, a system prompt will appear, allowing you to update in a timely manner.

### 注意事项 Notes

请注意：

1. 登陆或注销后会自动检测登陆或注销是否成功，系统返回的等待时间为5秒，超过5秒后会返回登陆或注销失败，但并不意味着真的失败，超过5秒显示失败后登陆进程仍然会继续，可以重新运行软件查看登陆状态。

2. 本软件仅提供登陆和身份认证功能，其本质和在 [a.suda.edu.cn](http://a.suda.edu.cn) 登陆没有任何区别。前提是您已经通过无线/有线方式将您的Linux设备连接到了苏大校园网内，可以访问局域网，但无法访问其他网络。验证方法可以 `ping a.suda.edu.cn` 尝试是否有响应，如果无响应说明没有成功连接无线网，本软件不可能起作用，您先需要连接该网络，再使用本软件进行登陆和身份认证。

Attention:

1. After logging in or logging out, the system will automatically check if the operation was successful. The system's waiting time is 5 seconds. If it exceeds 5 seconds, it will return a login or logout failure, but this does not necessarily mean actual failure. The login process will continue even after showing failure after 5 seconds. You can re-run the software to check the login status.

2. This software only provides login and identity authentication functions, which are essentially the same as logging in at [a.suda.edu.cn](http://a.suda.edu.cn). It assumes that you have already connected your Linux device to the SUDA campus network via wireless/wired connection, allowing access to the local area network but not other networks. To verify, you can try `ping a.suda.edu.cn` to see if there is a response. If there is no response, it means you have not successfully connected to the wireless network. This software will not work, and you need to connect to the network first before using this software for login and identity authentication.

## 版本要求说明 Version Requirement Description

Python版尽可能兼容老版本，需满足 Python 2.7/3.x 运行的系统调用需求，内核最低支持 Linux 2.6.32。

The Python version is compatible with older versions as much as possible and needs to meet the system call requirements of Python 2.7/3.x. The minimum kernel support is Linux 2.6.32.

- Python 2.7 兼容：CentOS 6（需手动安装 Python 2.7，默认 2.6）、Ubuntu 12.04 及以上。

- Python 2.7 compatibility: CentOS 6 (requires manual installation of Python 2.7, default is 2.6), Ubuntu 12.04 and above.

- Python 3.x 兼容：如 Ubuntu 14.04 + 、CentOS 7 + 等。

- Python 3.x compatibility: such as Ubuntu 14.04+, CentOS 7+, etc.


代码中除 `requests` 外所有库均为Python原生库。

All libraries in the code are Python native libraries except `requests`.

## 版权声明与许可协议 Copyright Statement and License Agreement

本项目采用 [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0) 开源。您可以在遵守该协议的前提下自由使用、复制、修改和分发本软件及其源代码。

This project is open source under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). You are free to use, copy, modify, and distribute this software and its source code under the terms of this agreement.

主要条款包括但不限于：

- 允许个人和商业用途；
- 允许修改和分发源代码；
- 必须在分发时附带原始许可证和版权声明；
- 本软件按“原样”提供，不附带任何明示或暗示的担保；
- 使用本软件造成的任何直接或间接损失，作者不承担任何责任。

Key terms include but are not limited to:

- Permits personal and commercial use;
- Permits modification and distribution of source code;
- Must include the original license and copyright notice when distributing;
- This software is provided "as is" without any express or implied warranties;
- The author shall not be liable for any direct or indirect damages caused by the use of this software.

### 特别声明 Special Statement

- 本软件仅供学习、研究或个人使用，严禁用于任何违法、违规活动。
- 作者保留随时更改开源协议的权利。
- 如您不确定您的行为是否符合许可协议，请通过邮箱与作者取得联系。

- This software is for learning, research, or personal use only. It is strictly prohibited for any illegal or irregular activities.
- The author reserves the right to change the open-source license at any time.
- If you are unsure whether your actions comply with the license agreement, please contact the author via email.

### 联系作者 Contact the Author

如您遇到任何问题，请通过邮箱联系作者：

If you encounter any problems, please contact the author via email:

michaelqian0517@gmail.com

如果您非苏大但您在您的学校或单位有相关类似需求，可以联系作者定制。

If you are not from Soochow University but have similar needs at your school or institution, you can contact the author for customization.

### 版权声明 Copyright Notice

Copyright (c) 2025 Michael Qian. All Rights Reserved.

本项目的详细许可信息请参见 [LICENSE](./LICENSE) 文件。

For detailed license information of this project, please refer to the [LICENSE](./LICENSE) file.