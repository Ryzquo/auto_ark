#!/user/bin/env python
# -*- coding: utf-8 -*-

import win_tools
import cv_tools

import os
import time
import json


# 代理关卡
cur_level = "WB-9"
# 是否开始游戏
start_game_flag = True

# 当前文件所在目录
dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

def start_ark(path_emulator: str):
    """
    启动
    """
    print("开始...")
    
    # 获取窗口句柄
    hwnd = win_tools.find_window()
    
    # 如果未找到窗口句柄, 启动窗口并再次获取句柄
    if not hwnd:
        print("启动模拟器中...")
        # 对地址进行处理
        path_emulator = win_tools.get_realpath(
            "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/BlueStacks 5.lnk"
        )
        # 启动
        hwnd = win_tools.start_getHwnd(path_emulator)
        
    
    # 仍未找到窗口句柄
    if not hwnd:
        print("未启动模拟器.")
        return
    
    # 连接abd
    if not win_tools.connect_adb():
        print("adb连接失败...")
        return
    print("adb连接成功...")
    
    # if start_game_flag:
    #     startup()
        
    # clear_san(cur_level)
    
    # # 进入代理循环
    # while hwnd:
    #     # 检测句柄, 不存在则结束代理
    #     hwnd = win_tools.find_window()
    #     if not hwnd:
    #         print("窗口已关闭")
    #         return
        
    #     print(1)
    #     # 清理智
    #     # clear_san(cur_level)
        
    #     # 睡
    #     time.sleep(3)
     
    
def stop_ark():
    """
    结束
    """
    if win_tools.disconnect_adb():
        print(
            "adb连接已断开...\n"
            "结束..."
        )
        return

    print("断开adb连接失败...")
    
    
def startup():
    """
    启动游戏
    """
    targets = get_json_data("startup")
    jump_to(targets)
    time.sleep(15)
    
    
def clear_san(level: str):
    """
    清理智
    :params
        level: 关卡名
    :return
    """
    print(f"开始清理智...")
    
    # 从json中获取关卡对应图像所在地址
    # 进入关卡开始页
    print("正在进入关卡页...")
    jump_to(get_json_data(level))
    
    # 开始->进入循环, 理智不够停止
    # 检测花费理智与剩余理智
    print("检测理智...")
    cost_san_text, remain_san_text = get_every(
                                      cv_tools.text_match(win_tools.win_shot(), 
                                                          re_rule=[
                                                              r"^-\d{1,2}$", 
                                                              r"^\d{1,3}/\d{2,3}$"
                                                          ])["re_rule"])
    while (not cost_san_text) or (not remain_san_text):
        cost_san_text, remain_san_text = get_every(
                                          cv_tools.text_match(win_tools.win_shot(), 
                                                              re_rule=[
                                                                  r"^-\d{1,2}$", 
                                                                  r"^\d{1,3}/\d{2,3}$"
                                                              ])["re_rule"])
    cost_san = int(cost_san_text[1].replace('-', ''))
    remain_san = int(remain_san_text[1].split('/')[0])
    
    XD_count = 1
    while cost_san <= remain_san:
        print(f"开始行动 - {level}: 第{XD_count}次")
        XD_count += 1
        # 开始行动
        jump_to(get_json_data("startXD"))
        
        # 待机至检测到 '行动结束'
        pos = get_every(cv_tools.text_match(win_tools.win_shot(), 
                                            text="行动结束")["text"])
        print(pos)
        while not pos:
            pos = get_every(cv_tools.text_match(win_tools.win_shot(), 
                                                text="行动结束")["text"])
            time.sleep(5)
        x, y, w, h = pos[0]
        
        # 对结算物资进行统计, 并进入关卡开始页
        win_tools.adb_click(int(x+w/2), int(y+h/2))
        time.sleep(3)
        # 检测剩余理智, 准备进入下一轮循环
        remain_san_text = get_every(cv_tools.text_match(win_tools.win_shot(), 
                                              re_rule=r"^\d{1,3}/\d{2,3}$")["re_rule"])
        while not remain_san_text:
            remain_san_text = get_every(cv_tools.text_match(win_tools.win_shot(), 
                                                  re_rule=r"^\d{1,3}/\d{2,3}$")["re_rule"])
        remain_san = int(remain_san_text[1].split('/')[0])
        
    # 返回主页
    print("回到主页...")
    back_home()
        
    print("理智已清完...")
    
        
def jump_to(targets: list, delay_jump: int=3):
    """
    根据传入的路径跳转到对应界面
    :params
        targets: 路径列表
        adb: adb程序路径
        adb_address: adb 连接地址
        delay_jump: 界面间的切换时间
    :return
    """
    for tar in targets:
        # 截图路径
        shot_path = win_tools.win_shot()
        
        ope, val = tar
        if ope == "cv":
            # 模板匹配
            # 模板路径
            temp_path = os.path.join(dir, val)
            # 获取位置信息
            pos = get_every(cv_tools.img_match(shot_path, temp_path))
            while not pos:
                pos = get_every(cv_tools.img_match(win_tools.win_shot(), temp_path))
                time.sleep(2)
            
            x, y, w, h = pos
            
        elif ope == "ocr":
            # 文本匹配
            ope2, rule = val
            if ope2 == "text":
                pos = get_every(cv_tools.text_match(shot_path, text=rule)[ope2])
                while not pos:
                    pos = get_every(cv_tools.text_match(win_tools.win_shot(), 
                                                        text=rule)[ope2])
                    time.sleep(2)
            elif ope2 == "rule":
                pos = get_every(cv_tools.text_match(shot_path, re_rule=rule)[ope2])
                while not pos:
                    pos = get_every(cv_tools.text_match(win_tools.win_shot(), 
                                                        re_rule=rule)[ope2])
                    time.sleep(2)
            
            x, y, w, h = pos[0]
        
        # 点击
        win_tools.adb_click(x=x+w/2, y=y+h/2)
        
        # 跳转到对应界面的时间
        time.sleep(delay_jump)
        

def back_home():
    """
    返回主页
    """
    jump_to(get_json_data("backHome"), delay_jump=2)
        

def get_every(result):
    """
    获取每一项
    :params
        result: 结果
    return
        处理后的结果
    """
    res = [res[0] for res in result if res]
    return res[0] if len(res) == 1 else res

    
def get_json_data(id: str):
    """
    从json中获取图片地址
    :params
        id: 操作
    :return
        图片路径: [path, path, ...]
    """
    # 从json中获取图片地址
    with open(os.path.join(dir, 'json/level.json'), 'r', encoding='utf-8') as f_json:
        level_data = json.load(f_json)
    return level_data[id]

    
if __name__ == "__main__":
    ...
