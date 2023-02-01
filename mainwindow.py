#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), 'ark_tools/').replace('\\', '/'))
from ark_tools.agen_tools import AgenTools

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        
        # 图标
        self.logoPath = os.path.join(self.dir, 'images/logo.jpg')
        # 模拟器路径
        self.path_emulator = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/BlueStacks 5.lnk"
        # 任务json
        self.task_json = os.path.join(self.dir, "json/task.json").replace('\\', '/')
        
        # 屏幕大小
        self.screenWidth, self.screenHeight = self.getScreenSize()
        
        # 初始化
        self.initStyle()
        self.agenTools = AgenTools()
        self.initControl()
        
    def __del__(self):
        self.agenTools.stop_ark()
        
    def initStyle(self):
        """
        初始化窗口样式
        """
        self.setWindowTitle("auto_ark")
        self.setWindowIcon(QIcon(self.logoPath))
        self.resize(QSize(int(self.screenWidth/2), int(self.screenHeight/2)))
        
    def initControl(self):
        """
        初始化窗口控件
        """
        # 任务列表
        self.listTask = QListWidget(self)
        self.listTask.setStyleSheet(
            "border: none;"
        )
        # 开始按钮
        self.btnStart = QPushButton(self, text="开始")
        # 设置
        self.widgetSetting = QWidget(self)
        self.widgetSetting.setStyleSheet(
            "background-color: white;"
        )
        # 日志列表
        self.treeLog = QTextEdit(self)
        self.treeLog.setStyleSheet(
            "border: none;"
        )
        
        # 布局
        grid = QGridLayout()
        grid.setSpacing(10)
        # 左
        grid.addWidget(self.listTask, 1, 0, 3, 3)
        grid.addWidget(self.btnStart, 4, 1, 1, 1)
        # 中
        grid.addWidget(self.widgetSetting, 1, 3, 4, 3)
        # 右
        grid.addWidget(self.treeLog, 1, 6, 4, 3)
        
        self.setLayout(grid)
        
        # 初始化任务列表
        self.initListTask()
        # 槽
        self.ctConnect()
        
    def ctConnect(self):
        """
        连接信号槽
        """
        self.btnStart.clicked.connect(
            lambda: threading.Thread(target=self.agenTools.start_ark, 
                                     kwargs={"path_emulator": self.path_emulator}).start()
        )
        
    def initListTask(self):
        """
        从json初始化任务列表
        """
        self.listTask.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        tasks = AgenTools.get_json_data(self.task_json)
        for key in tasks.keys():
            itemTask = QListWidgetItem()
            itemCheckBox = QCheckBox(text=tasks[key]['name'])
            itemCheckBox.stateChanged.connect(self.onCheckBoxChange())
            self.listTask.addItem(itemTask)
            self.listTask.setItemWidget(itemTask, itemCheckBox)
        
    def getScreenSize(self):
        """
        获取屏幕大小
        :params
        :return
            (width, height)
        """
        screen = QGuiApplication.primaryScreen().geometry()
        return (screen.width(), screen.height())
    
    def onCheckBoxChange(self):
        """
        复选框状态改变
        更改代理任务
        更改task.json对应项
        """
        with open(self.task_json, 'r', encoding='utf-8') as jf:
            tasks = json.load(jf)
        for i in range(len(tasks)):
            # item = QCheckBox(self.listTask.itemWidget(self.listTask.item(i)))
            ...
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec())
