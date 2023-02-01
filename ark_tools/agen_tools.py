#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import json

sys.path.append(os.path.dirname(__file__).replace('\\', '/'))
import win_tools
from cv_tools import CvTools


# 代理关卡
cur_level = "LS-6"

class AgenTools():
    def __init__(self) -> None:
        # 当前文件所在目录
        self.dir = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')

        # json
        self.level_json = os.path.join(self.dir, "json/level.json").replace('\\', '/')
        self.se_json = os.path.join(self.dir, "json/se.json").replace('\\', '/')
        
        self.taskFlags = {
            # 启动模拟器
            "START_EMULATOR": False, 
            "startEmulator_time": 20,
            # 启动游戏 
            "START_GAME": False, 
            # 清理智
            "CLEAR_SAN": False, 
            # 领取日常/周常奖励
            "RECEIVE_AWARD": False
        }

    def start_ark(self, path_emulator: str):
        """
        启动
        """
        # 图像
        self.cvTools = CvTools()
        
        print("开始...")
        
        # 启动模拟器
        if self.taskFlags['START_EMULATOR']:
            # 对地址进行处理
            path_emulator = win_tools.get_realpath(path_emulator)
            # 启动
            hwnd = win_tools.start_getHwnd(path_emulator, 
                                           delay_start=self.startEmulator_time)
        else:
            # 获取窗口句柄
            hwnd = win_tools.find_window() 
        
        # 仍未找到窗口句柄
        if not hwnd:
            print("未启动模拟器.")
            return
        
        # 连接abd
        if not win_tools.connect_adb():
            return
        
        # 启动游戏
        if self.taskFlags['START_GAME']:
            self.startup()
        
        # 清理智
        if self.taskFlags['CLEAR_SAN']:
            self.clear_san(cur_level)
        
        # 领取奖励
        if self.taskFlags['RECEIVE_AWARD']:
            self.receive_award()
        
        
    def stop_ark(self):
        """
        结束
        """
        if win_tools.disconnect_adb():
            print("结束...")
            return
        
        
    def startup(self, start_time: int=15):
        """
        启动游戏
        """
        print("启动游戏中...")
        targets = AgenTools.get_json_data(self.se_json, "startup")
        self.jump_to(targets)
        time.sleep(start_time)
        
        # 关闭公告
        if self.cvTools.text_match(win_tools.win_shot(), text="公告")[0]:
            print("检测到公告页, 关闭中...")
            x, y, w, h = AgenTools.get_every_first(
                self.cvTools.img_match(win_tools.win_shot(), 
                                os.path.join(self.dir, 'images/start/close_gg.jpg'))
            )
            win_tools.adb_click(int(x+w/2), int(y+h/2))
        
        
    def clear_san(self, level: str):
        """
        清理智
        :params
            level: 关卡名
        :return
        """
        # 不在主页就返回主页
        if not AgenTools.get_every_first(self.cvTools.text_match(win_tools.win_shot(), 
                                                                 text="基建")):
            print("返回主页...")
            self.back_home()
        
        print(f"开始清理智...")
        
        # 从json中获取关卡对应图像所在地址
        # 进入关卡开始页
        print("正在进入关卡页...")
        if not self.jump_to(AgenTools.get_json_data(self.level_json, level)):
            print("进入关卡页失败...")
            return
        
        # 开始->进入循环, 理智不够停止
        # 检测花费理智与剩余理智
        print("检测理智...")
        cost_san_text, remain_san_text = AgenTools.get_every_first(
                                        self.cvTools.text_match(win_tools.win_shot(), 
                                                            text=[
                                                                r"$^-\d{1,2}$", 
                                                                r"$^\d{1,3}/\d{2,3}$"
                                                            ], x1=20))
        while (not cost_san_text) or (not remain_san_text):
            cost_san_text, remain_san_text = AgenTools.get_every_first(
                                            self.cvTools.text_match(win_tools.win_shot(), 
                                                                text=[
                                                                    r"$^-\d{1,2}$", 
                                                                    r"$^\d{1,3}/\d{2,3}$"
                                                                ], x1=20))
        cost_san = int(cost_san_text[1].replace('-', ''))
        remain_san = int(remain_san_text[1].split('/')[0])
        
        XD_count = 1
        while cost_san <= remain_san:
            print(f"开始行动 - {level}: 第{XD_count}次")
            XD_count += 1
            # 开始行动
            self.jump_to(AgenTools.get_json_data(self.se_json, "startXD"))
            
            # 待机至检测到 '行动结束'
            pos = AgenTools.get_every_first(self.cvTools.text_match(win_tools.win_shot(), 
                                                text="行动结束"))
            while not pos:
                pos = AgenTools.get_every_first(self.cvTools.text_match(win_tools.win_shot(), 
                                                    text="行动结束"))
                time.sleep(5)
            x, y, w, h = pos[0]
            
            # 对结算物资进行统计, 并进入关卡开始页
            win_tools.adb_click(int(x+w/2), int(y+h/2))
            time.sleep(3)
            # 检测剩余理智, 准备进入下一轮循环
            remain_san_text = AgenTools.get_every_first(self.cvTools.text_match(
                win_tools.win_shot(), text=r"$^\d{1,3}/\d{2,3}$", x1=20))
            while not remain_san_text:
                remain_san_text = AgenTools.get_every_first(self.cvTools.text_match(
                    win_tools.win_shot(), text=r"$^\d{1,3}/\d{2,3}$", x1=20))
            remain_san = int(remain_san_text[1].split('/')[0])
            
        # 返回主页
        print("返回主页...")
        self.back_home()
            
        print("理智已清完...")
        
        
    def receive_award(
        self, 
        level: str=None, 
        delay_time: int=2
    ):
        """
        领取奖励
        """
        # 回到主页
        if not AgenTools.get_every_first(self.cvTools.text_match(
            win_tools.win_shot(), text="基建")):
            print("返回主页...")
            self.back_home()
        
        print("领取日常/周常奖励...")
        if not level:
            for i in ["任务", "周常任务"]:
                pos = AgenTools.get_every_first(self.cvTools.text_match(
                    win_tools.win_shot(), text=i))
                if pos:
                    x, y, w, h = pos[0]
                    win_tools.adb_click(int(x+w/2), int(y+h/2))
                    time.sleep(delay_time)
                    pos = AgenTools.get_every_first(self.cvTools.text_match(
                        win_tools.win_shot(), text="收集全部"))
                    if pos:
                        x, y, w, h = pos[0]
                        for j in range(2):
                            win_tools.adb_click(int(x+w/2), int(y+h/2))
                            time.sleep(delay_time)
                    else:
                        print(f"无可领取{i}奖励...")
            
        else:
            if not self.jump_to(AgenTools.get_json_data(self.se_json, level)):
                print("无可领取奖励...")
                return
        
        self.back_home()
        
            
    def jump_to(
        self, 
        targets: list, 
        delay_jump: int=3, 
        detect_times: int=3
    ):
        """
        根据传入的路径跳转到对应界面
        :params
            targets: 路径列表
            delay_jump: 界面间的切换时间
            detect_times: 未检测到时的重试次数
        :return
            是否跳转成功
        """
        for tar in targets:
            # 截图路径
            shot_path = win_tools.win_shot()
            
            ope, val = tar['ope'], tar['val']
            swipe = tar['swipe']
            if ope == "cv":
                # 模板匹配
                # 模板路径
                temp_path = os.path.join(self.dir, val)
                roi = tar['roi']
                # 获取位置信息
                if swipe:
                    pos = AgenTools.get_every_first(self.cvTools.img_match(
                        shot_path, temp_path, roi=roi))
                    if not pos:
                        w, h = CvTools.getWH(shot_path)
                        for sw in swipe:
                            pt1, pt2 = sw
                            pt1 = (int(pt1[0]*w), int(pt1[1]*h))
                            pt2 = (int(pt2[0]*w), int(pt2[1]*h))
                            win_tools.adb_swipe(pt1, pt2)
                            time.sleep(2)
                            pos = AgenTools.get_every_first(self.cvTools.img_match(
                                win_tools.win_shot(), temp_path, roi=roi))
                            if pos:
                                break
                            win_tools.adb_swipe(pt2, pt1)
                else:
                    pos = AgenTools.get_every_first(self.cvTools.img_match(
                        shot_path, temp_path, roi=roi))
                    for i in range(detect_times):
                        pos = AgenTools.get_every_first(self.cvTools.img_match(
                            win_tools.win_shot(), temp_path, roi=roi))
                        time.sleep(2)
                        if pos:
                            break
                if not pos:
                    print("找不到")
                    return False
                x, y, w, h = pos
                
                
            elif ope == "ocr":
                # 文本匹配
                ope2, rule = val
                x1, x2, y1, y2 = tar['lim']
                if swipe:
                    pos = AgenTools.get_every_first(self.cvTools.text_match(
                        shot_path, text=rule, x1=x1,x2=x2,y1=y1,y2=y2))
                    if not pos:
                        w, h = CvTools.getWH(shot_path)
                        for sw in swipe:
                            pt1, pt2 = sw
                            pt1 = (int(pt1[0]*w), int(pt1[1]*h))
                            pt2 = (int(pt2[0]*w), int(pt2[1]*h))
                            win_tools.adb_swipe(pt1, pt2)
                            time.sleep(2)
                            pos = AgenTools.get_every_first(self.cvTools.text_match(
                                win_tools.win_shot(), text=rule, x1=x1,x2=x2,y1=y1,y2=y2))
                            if pos:
                                break
                            win_tools.adb_swipe(pt2, pt1)
                else:
                    pos = AgenTools.get_every_first(self.cvTools.text_match(
                        shot_path, text=rule, x1=x1,x2=x2,y1=y1,y2=y2))
                    for i in range(detect_times):
                        pos = AgenTools.get_every_first(self.cvTools.text_match(
                            win_tools.win_shot(), text=rule, x1=x1,x2=x2,y1=y1,y2=y2))
                        time.sleep(2)
                        if pos:
                            break
                if not pos:
                    print("找不到")
                    return False
                x, y, w, h = pos[0]
            
            # 点击
            win_tools.adb_click(x=x+w/2, y=y+h/2)
            
            # 跳转到对应界面的时间
            time.sleep(delay_jump)
        
        return True

    def back_home(self):
        """
        返回主页
        """
        AgenTools.jump_to(AgenTools.get_json_data(self.se_json, "backHome"), 
                          delay_jump=2)


    @staticmethod
    def get_every_first(result):
        """
        获取每个匹配列表的第一项
        :params
            result: 结果
        return
            处理后的结果
        """
        res = [res[0] for res in result if res]
        return res[0] if len(res) == 1 else res

    @staticmethod
    def get_json_data(path: str, id: str=None):
        """
        从json中获取图片地址
        :params
            path: json文件路径
            id: 操作
        :return
            图片路径: [path, path, ...]
        """
        path = path.replace('\\', '/')
        # 从json中获取图片地址
        with open(path, 'r', encoding='utf-8') as f_json:
            level_data = json.load(f_json)
        if id:
            return level_data[id]
        else:
            return level_data

    
if __name__ == "__main__":
    ...
