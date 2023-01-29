#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import win32gui, win32api

import win32com.client

window_names = [
    "BlueStacks App Player", 
]

dir = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')

# adb 连接地址
adb_address = "127.0.0.1:5555"
# adb 程序路径
adb = os.path.join(dir, "platform-tools/adb.exe").replace('\\', '/')


def connect_adb(connect_times: int=5):
    """
    连接adb
    :params
        connect_times: 连接次数
    :return
        是否连接成功: bool
    """
    connect_status = adb_connect_status()
    if connect_status:
        return connect_status
    
    print("连接adb中...")
    for i in range(connect_times):
        print(f"第{i+1}次.")
        os.system(f"{adb} connect {adb_address}")
        connect_status = adb_connect_status()
        if connect_status:
            break 
    
    return connect_status


def disconnect_adb(disconnect_times: int=5):
    """
    断开adb连接
    :params
        disconnect_times: 断开连接次数
    :return
        是否连接成功: bool
    """
    connect_status = not adb_connect_status()
    if connect_status:
        return connect_status
    
    for i in range(disconnect_times):
        os.system(f"{adb} disconnect {adb_address}")
        connect_status = not adb_connect_status()
        if connect_status:
            break 
    
    return connect_status


def adb_connect_status():
    """
    检测adb与指定设备的连接状态
    :params
    :return
        连接状态: bool
    """
    deviceInfo = [
        info.replace('\n', '').split('\t') 
        for i, info in enumerate(os.popen(f"{adb} devices").readlines()) 
        if i != 0 and info != '\n'
    ]
    
    return any([True if info[1] == 'device' and info[0] == adb_address else False 
                for info in deviceInfo])


def win_shot(
    img_path: str=os.path.join(dir, "shot.png")
):
    """
    根据窗口句柄后台截图
    :params
        img_path: 截图保存路径
    :return
        截图路径
    """
    img_path = img_path.replace('\\', '/')
    # os.system(f"{adb} exec-out screencap -p > {img_path}")
    os.system(f"{adb} -s {adb_address} shell screencap /sdcard/Download/shot.png")
    os.system(f"{adb} -s {adb_address} pull /sdcard/Download/shot.png {img_path}")
    os.system(f"{adb} -s {adb_address} shell rm /sdcard/Download/shot.png")
    
    return img_path


def adb_click(
    x, y
):
    """
    使用adb点击
    :params
    :return
    """
    os.system(f"{adb} -s {adb_address} shell input tap {x} {y}")
    
    return True


def start_getHwnd(path_emulator: str, delay_start: int=3):
    """
    启动程序并返回窗口句柄
    :params
        path_emulator: 模拟器地址
        delay_start: 启动时间
    :return
        句柄
    """
    # 后台执行
    win32api.ShellExecute(0, 'open', path_emulator, '', '', 0)
    time.sleep(delay_start)
    
    return find_window()


def get_realpath(path:str):
    """
    获取目标地址
    :params
        path: 地址
    :return
        真实地址
    """
    
    if path.endswith('.lnk'):
        # 快捷方式
        shell = win32com.client.Dispatch("WScript.Shell")
        realpath = shell.CreateShortCut(path).Targetpath
        
    else:
        realpath = path
    
    return realpath


def find_window():
    """
    寻找模拟器
    :params
    :return
        句柄
    """
    hwnds = []
    win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnds)
    
    rets = [hwnd for hwnd in hwnds 
            if any([name == win32gui.GetWindowText(hwnd) for name in window_names])]
    
    return rets[0] if rets else None

if __name__ == "__main__":
    ...
