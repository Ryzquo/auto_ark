#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import win32gui, win32api


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
    print("连接adb中...")
    connect_status = False
    for i in range(connect_times):
        subprocess.call(f"{adb} connect {adb_address}")
        connect_status = adb_connect_status()
        if connect_status:
            break 
    
    print("连接成功..." if connect_status else "连接失败...")
    
    return connect_status


def disconnect_adb(disconnect_times: int=5):
    """
    断开adb连接
    :params
        disconnect_times: 断开连接次数
    :return
        是否连接成功: bool
    """
    print("断开adb连接中...")
    connect_status = False
    for i in range(disconnect_times):
        subprocess.call(f"{adb} disconnect {adb_address}")
        connect_status = not adb_connect_status()
        if connect_status:
            break
    
    print("断开连接成功..." if connect_status else "断开连接失败...")
    
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
    adb截图
    :params
        img_path: 截图保存路径, 默认根目录下
    :return
        截图路径
    """
    img_path = img_path.replace('\\', '/')
    # subprocess.call(f"{adb} exec-out screencap -p > {img_path}")
    subprocess.call(f"{adb} -s {adb_address} shell screencap /sdcard/Download/shot.png")
    subprocess.call(f"{adb} -s {adb_address} pull /sdcard/Download/shot.png {img_path}")
    subprocess.call(f"{adb} -s {adb_address} shell rm /sdcard/Download/shot.png")
    
    return img_path


def adb_click(
    x, y
):
    """
    adb点击
    :params
        x, y: 坐标
    :return
    """
    subprocess.call(f"{adb} -s {adb_address} shell input tap {x} {y}")
    
    return True


def adb_swipe(pt1, pt2):
    """
    滑动
    :params
        pt1: (x, y) 起点
        pt2: (x, y) 终点
    :return
    """
    x1, y1, x2, y2 = *pt1, *pt2
    subprocess.call(f"{adb} -s {adb_address} shell input swipe {x1} {y1} {x2} {y2}")
    
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
        import win32com.client
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
