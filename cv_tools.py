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
dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')


def img_match(
    target_path: str, template_path=None, 
    ratio: float=1, thresh: float=0.4, 
    multiple: bool=False
):
    """
    模板匹配, 多目标
    :params
        target_path: 目标路径
        template_path: 模板路径
    :return
        [temp1:[pos, pos, ...], temp2:[pos, pos, ...]]
            : pos=(x, y, w, h)
    """
    target_path = target_path.replace('\\', '/')
    target = cv2.imread(target_path)
    
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
            pos = [(*min_loc, w, h)]
        else:
            pos = []

        # cv2.rectangle(target, min_loc, (min_loc[0]+w, min_loc[1]+h), (0,0,225), 2)
        # print(f"{temp_path.split('/')[-1].split('.')[0]}, {min_val:.2}")
        # cv2.imwrite(os.path.join(dir, '1/', temp_path.split('/')[-1].split('.')[0])+'.jpg', target)
        
        locs = np.where(result < thresh)
        for loc in zip(*locs[::-1]):
            x, y = loc
            if all([True if (abs(x-t_x)>w) or (abs(y-t_y)>h) else False 
                    for t_x, t_y, _, _ in pos]):
                pos.append((x, y, w, h))
                cv2.rectangle(target, (x, y), (x+w, y+h), (0,0,225), 2)
                
        postion.append(pos)
    
    # cv2.imshow('tar', 
    #            cv2.resize(target, 
    #                       (int(target.shape[1]/1.6), int(target.shape[0]/1.6))))
    # cv2.waitKey(0)
    
    return postion


# 为了方便使用, 可能需要包装一下
def text_match(
    img_path: str, 
    text=None, re_rule=None, 
    multiple: bool=False
):
    """
    文本匹配, 多目标
    :params
        img_path: 图像路径
        text: 需要从图像中寻找的文本
    :return
        {
            "text": [text1:[pos, pos, ...], text2:[pos, pos, ...], ...], 
            "re_rule": [rule1:[pos, pos, ...], rule2:[pos, pos, ...], ...]
        }: pos=((x, y, w, h), detect_text)
    """
    if not isinstance(text, list):
        text = [text]
    if not isinstance(re_rule, list):
        re_rule = [re_rule]
    
    pos_text = [[] for i in range(len(text))]
    pos_rule = [[] for i in range(len(re_rule))]
    
    img_path = img_path.replace('\\', '/')
    # img = cv2.imread(img_path)
    
    result = ocr.ocr(img_path, cls=True)
    for res in result:
        for line in res:
            x, y = tuple(map(int, line[0][0]))
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
    

if __name__ == "__main__":
    # print("模板匹配:", 
    #       img_match(os.path.join(dir, 'shot.png'), 
    #                 os.path.join(dir, 'images/start/logo.jpg'), 
    #                 ratio=1))
    # print("文本匹配:", text_match(os.path.join(dir, "images/st.png"), text="开始行动"), 
    #       "开始行动")
    
    remain_san_text, cost_san_text = text_match(os.path.join(dir, "images/st.png"), 
                                                re_rule=[r"^\d{1,3}/\d{2,3}$", 
                                                         r"^-\d{1,2}$"])["re_rule"]
    print(remain_san_text, cost_san_text)
    remain_san = int(remain_san_text[0][1].split('/')[0])
    cost_san = int(cost_san_text[0][1].replace('-', ''))
    print(remain_san, cost_san)
