# time : 2022/10/22
# name :Auto_CC
# Created by: stricks and Fate_yo
#
import json
import requests
import time
import keyboard
from plyer import notification
import socket
import webbrowser
from tkinter import *
import os
import sys

import newUI
from DEScrypto import Encrypt

user = {}
flag = True

login = {
    "DoWhat": "Login",
    "password": "",
    "remember": "false",
    "username": ""
}

url = "http://1.1.1.1/Auth.ashx"
session = requests.session()


def resource_path(filaeName):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filaeName)
    return os.path.join(filaeName)


def init():
    with open('user.txt', 'a+', encoding='utf-8') as f:
        f.seek(0)
        if f.read() == "":
            p = Tk()
            newUI.CreateWindow(p)
        for line in f:
            try:
                s = str(line).split()
                user[s[0]] = s[1]
            except Exception:
                clear_login()
                notification.notify(
                    title="连接CC通知",
                    message="文件错误，请重新输入账号和密码",
                    app_icon=resource_path("favicon.ico"),
                    timeout=3
                )
                return init()
    login['username'] = user['username']
    crypt = Encrypt()
    login['password'] = crypt.aes_encrypt(user['username'], user['password'])


def connection():
    init()
    result = session.post(url=url, data=json.dumps(login))
    if json.loads(result.text)['Message'] == "用户名或密码不正确！":
        notification.notify(
            title="连接CC通知",
            message="连接失败，用户名或密码不正确！",
            app_icon=resource_path("favicon.ico"),
            timeout=3
        )
        clear_login()
        connection()
        return
    session.post(url=url, data=json.dumps({"DoWhat": "GetInfo"}))
    result = session.post(url=url, data=json.dumps({"DoWhat": "OpenNet", "Package": f"学生-{user['package']}-100M"}))
    if not json.loads(result.text)["Result"] and not check_login():
        notification.notify(
            title="连接CC通知",
            message="连接失败，需要打电话，请手动连接",
            app_icon=resource_path("favicon.ico"),
            timeout=3
        )
        webbrowser.open('https://cc.nsu.edu.cn', new=1)
        return
    notification.notify(
        title="连接CC通知",
        message="连接成功，按ctrl+q退出登录",
        app_icon=resource_path("favicon.ico"),
        timeout=3
    )


def check_login():
    result = session.post(url=url, data=json.dumps({"DoWhat": "Check"}))
    if json.loads(result.text)['Result'] == "needLogin":
        return False
    return True


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


def clear_login():
    with open('user.txt', 'w') as f:
        f.truncate()
    global user
    user = {}


def quit():
    global flag
    flag = not flag
    clear_login()
    session.post(url=url, data=json.dumps({"DoWhat": "CloseNet", "IP": f"{extract_ip()}"}))
    session.post(url=url, data=json.dumps({"DoWhat": "Logout"}))
    if flag:
        notification.notify(
            title="连接CC通知",
            message="已退出连接，已唤醒连接窗，按ctrl+q关闭",
            app_icon=resource_path("favicon.ico"),
            timeout=3
        )
    else:
        notification.notify(
            title="连接CC通知",
            message="已退出连接，已关闭连接窗，按ctrl+q唤醒",
            app_icon=resource_path("favicon.ico"),
            timeout=3
        )


if __name__ == '__main__':
    keyboard.add_hotkey('ctrl+q', quit)
    while True:
        try:
            if flag and requests.get('https://cc.nsu.edu.cn', timeout=3).status_code == 200:
                if not check_login():
                    connection()
        except Exception:
            pass
        finally:
            time.sleep(5)
