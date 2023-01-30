#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import re

import numpy as np

from paddleocr import PaddleOCR
from itertools import zip_longest


# 文本识别
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# 当前文件所在目录
dir = os.path.dirname(os.path.dirname(__file__)).replace('\\', '/')


def img_match(
    target_path: str, template_path=None, 
    ratio: float=1, thresh: float=0.4, 
    multiple: bool=False, 
    roi=None
):
    """
    模板匹配, 多目标
    :params
        target_path: 目标路径
        template_path: 模板路径
        ratio: 比例
        thresh: 阈值
        multiple: 是否多目标
        roi: 感兴趣区域 -> 主对角线(x1,y1, x2,y2):int // [("left/right/top/bottom",  (0-1] ), ...]
    :return
        [temp1:[pos, pos, ...], temp2:[pos, pos, ...]]
            : pos=(x, y, w, h)
    """
    target_path = target_path.replace('\\', '/')
    target = cv2.imread(target_path)
    h_target, w_target = target.shape[:2]
    
    # draw = target.copy()
    
    x_ori, y_ori = 0, 0
    if roi:
        if not isinstance(roi, list):
            roi = [roi]
        for i, r in enumerate(roi):
            if isinstance(r[0], int) and i == 0:
                x1, y1, x2, y2 = r
                x_ori, y_ori = x1, y1
                target = target[y1:y2, x1:x2, :]
                h_target, w_target = target.shape[:2]
            else:
                site, pp = r
                if ((not isinstance(site, str)) or 
                    (not isinstance(pp, (float, int)))):
                    return
                x1, y1, x2, y2 = 0, 0, w_target, h_target
                if site == "left":
                    x2 = int(w_target*pp)
                elif site == "right":
                    x1 = int(w_target - w_target*pp)
                    x_ori += x1
                elif site == "top":
                    y2 = int(h_target*pp)
                elif site == "bottom":
                    y1 = int(h_target - h_target*pp)
                    y_ori += y1
                target = target[y1:y2, x1:x2, :]
                h_target, w_target = target.shape[:2]
    
    if not isinstance(template_path, list):
        template_path = [template_path]
    postion = []
    
    for temp_path in template_path:
        temp_path = temp_path.replace('\\', '/')
        
        template = cv2.imread(temp_path)
        template = cv2.resize(template, 
                            (int(template.shape[1]*ratio), int(template.shape[0]*ratio)))
        h, w, _ = template.shape
    
        # 模板匹配
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if min_val < thresh:
            pos = [(min_loc[0]+x_ori, min_loc[1]+y_ori, w, h)]
        else:
            pos = []

        # cv2.rectangle(draw, (min_loc[0]+x_ori, min_loc[1]+y_ori), 
        #               (min_loc[0]+x_ori+w, min_loc[1]+y_ori+h), (0,0,225), 2)
        # print(f"{temp_path.split('/')[-1].split('.')[0]}, {min_val:.2}")
        # cv2.imwrite(os.path.join(dir, '1/', temp_path.split('/')[-1].split('.')[0])+'.jpg', target)
        
        if multiple:
            locs = np.where(result < thresh)
            for loc in zip(*locs[::-1]):
                x, y = loc
                if all([True if (abs(x-t_x)>w) or (abs(y-t_y)>h) else False 
                        for t_x, t_y, _, _ in pos]):
                    pos.append((x+x_ori, y+y_ori, w, h))
                    # cv2.rectangle(draw, (x, y), (x+w, y+h), (0,0,225), 2)
                    # cv2.imshow('tar', 
                    #            cv2.resize(target, 
                    #                       (int(target.shape[1]/1.6), 
                    #                        int(target.shape[0]/1.6))))
                    # cv2.waitKey(0)
                
        postion.append(pos)
    
    # cv2.imshow('tar', 
    #            cv2.resize(draw, 
    #                       (int(draw.shape[1]/1.6), int(draw.shape[0]/1.6))))
    # cv2.waitKey(0)
    
    return postion


# 为了方便使用, 可能需要包装一下
def text_match(
    img_path: str, 
    text=None, re_rule=None, 
    multiple: bool=False, 
    x1=None,y1=None,x2=None,y2=None
):
    """
    文本匹配, 多目标
    :params
        img_path: 图像路径
        text: 需要从图像中寻找的文本
        re_rule: 正则
        multiple: 是否多目标
        x1, y1, x2, y2: 需要的区域
    :return
        {
            "text": [text1:[pos, pos, ...], text2:[pos, pos, ...], ...], 
            "re_rule": [rule1:[pos, pos, ...], rule2:[pos, pos, ...], ...]
        }: pos=((x, y, w, h), detect_text)
    """
    img_path = img_path.replace('\\', '/')
    # img = cv2.imread(img_path)
    if not os.path.exists(img_path):
        print("图片不存在")
        return

    h, w = cv2.imread(img_path).shape[:2]
    x1 = (x1*w if (0<x1<1) else x1) if x1 else 0
    y1 = (y1*h if (0<y1<1) else y1) if y1 else 0
    x2 = (x2*w if (0<x2<1) else x2) if x2 else w
    y2 = (y2*h if (0<y2<1) else y2) if y2 else h
    
    if not isinstance(text, list):
        text = [text]
    if not isinstance(re_rule, list):
        re_rule = [re_rule]
    
    pos_text = [[] for i in range(len(text))]
    pos_rule = [[] for i in range(len(re_rule))]
    
    result = ocr.ocr(img_path, cls=True)
    for res in result:
        for line in res:
            x, y = tuple(map(int, line[0][0]))
            if (not (x1 < x < x2)) or (not (y1 < y < y2)):
                continue
            w, h = int(line[0][2][0]-x), int(line[0][2][1]-y)
            dec_text, confidence = line[1]
            
            for tt, rule in zip_longest(enumerate(text), enumerate(re_rule)):
                if tt:
                    i, tt = tt
                    if tt and (tt in dec_text):
                        pos_text[i].append(((x, y, w, h), dec_text))
                if rule:
                    i, rule = rule
                    if rule and re.findall(rule, dec_text):
                        pos_rule[i].append(((x, y, w, h), dec_text))
            
            # cv2.polylines(img, [np.array(line[0],np.int32)], True, (0, 0, 255), 3)
            # print(dec_text)
            # cv2.imshow('img', cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2))))
            # cv2.waitKey(0)
    
    # cv2.imshow('img', cv2.resize(img, (int(img.shape[1]/2), int(img.shape[0]/2))))
    # cv2.waitKey(0)

    return {"text": pos_text, "re_rule": pos_rule}


def getWH(img_path):
    """
    获取图像的宽高
    :params:
        img_path: 图像路径
    :return:
        (w, h)
    """
    return cv2.imread(img_path).shape[:2][::-1]
    

if __name__ == "__main__":
    # print("模板匹配:", 
    #       img_match(os.path.join(dir, 'shot.png'), 
    #                 os.path.join(dir, 'images/start/logo.jpg'), 
    #                 ratio=1))
    # print("文本匹配:", text_match(os.path.join(dir, "images/st.png"), text="开始行动"), 
    #       "开始行动")
    
    # remain_san_text, cost_san_text = text_match(os.path.join(dir, "shot.png"), 
    #                                             re_rule=[r"^\d{1,3}/\d{2,3}$", 
    #                                                      r"^-\d{1,2}$"], 
    #                                             x1=10)["re_rule"]
    # print(remain_san_text, cost_san_text)
    # remain_san = int(remain_san_text[0][1].split('/')[0])
    # cost_san = int(cost_san_text[0][1].replace('-', ''))
    # print(remain_san, cost_san)
    
    # print(img_match(os.path.join(dir, "shot.png"), 
    #                 os.path.join(dir, "images/ZhongDuan/ziYuanShouJi.jpg"), 
    #                 roi=[["bottom", 0.11], ["top", 0.8]]))
    # print(img_match(os.path.join(dir, "shot.png"), 
    #                 os.path.join(dir, "images/ZhongDuan/ziYuanShouJi.jpg"), 
    #                 roi=(0, 800, 1600, 900)))
    
    
    print(text_match("E:/Chrome/t1.jpg", text="空中威胁"))