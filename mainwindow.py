#!/user/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import json
import threading

sys.path.append(os.path.join(os.path.dirname(__file__), 'ark_tools/').replace('\\', '/'))
from ark_tools.agen_tools import AgenTools

from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'ui_tools/').replace('\\', '/'))
from ui_tools.InterfaceUI import Ui_InterfaceUI


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_InterfaceUI()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 工作目录
        self.dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
        # 模拟器路径
        self.path_emulator = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/BlueStacks 5.lnk"
        # 任务json
        self.task_json = os.path.join(self.dir, "json/task.json").replace('\\', '/')
        self.tasks = AgenTools.get_json_data(self.task_json)
        
        # 图标
        self.setWindowIcon(QIcon(os.path.join(self.dir, 'images/ui/logo.png')))
        
        self.agenTools = AgenTools()
        self.initTaskList()
        self.ctConnect()
        
        # 脚本是否执行
        self.isRun = False
        # 脚本线程
        self.agenThread = threading.Thread(target=self.agenTools.start_ark,
                                           kwargs={"path_emulator": self.path_emulator})
        self.agenThread.setDaemon(True)
        
    def __del__(self):
        self.agenTools.stop_ark()
        self.sav_json()
        self.agenThread.join()
            
    def sav_json(self):
        with open(self.task_json, 'w') as jf:
            json.dump(self.tasks, jf)
    
    def ctConnect(self):
        """
        连接信号槽
        """
        self.ui.pBtnSE.clicked.connect(self.onPBtnSE_clicked)
        self.ui.pBtnMaximize.clicked.connect(self.restore_or_maximize_window)
        
    def initTaskList(self):
        """
        初始化任务列表
        """
        # 启动模拟器
        self.agenTools.taskFlags[self.tasks[u'启动模拟器']['key']] = self.tasks['启动模拟器']['checked']
        self.checkBoxStartEm = QCheckBox(text=u"启动模拟器")
        self.checkBoxStartEm.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.checkBoxStartEm.setCheckState(Qt.CheckState.Checked 
                                    if self.tasks[u'启动模拟器']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxStartEm.stateChanged.connect(self.onStartEmStateChanged)
        itemStartEm = QListWidgetItem()
        self.ui.listWTask.addItem(itemStartEm)
        self.ui.listWTask.setItemWidget(itemStartEm, self.checkBoxStartEm)
        # 启动游戏
        self.agenTools.taskFlags[self.tasks[u'启动游戏']['key']] = self.tasks['启动游戏']['checked']
        self.checkBoxStartGame = QCheckBox(text=u"启动游戏")
        self.checkBoxStartGame.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.checkBoxStartGame.setCheckState(Qt.CheckState.Checked
                                    if self.tasks[u'启动游戏']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxStartGame.stateChanged.connect(self.onStartGameStateChanged)
        itemStartGame = QListWidgetItem()
        self.ui.listWTask.addItem(itemStartGame)
        self.ui.listWTask.setItemWidget(itemStartGame, self.checkBoxStartGame)
        # 清理智
        self.agenTools.taskFlags[self.tasks[u'清理智']['key']] = self.tasks['清理智']['checked']
        self.checkBoxClearSan = QCheckBox(text=u"清理智")
        self.checkBoxClearSan.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.checkBoxClearSan.setCheckState(Qt.CheckState.Checked
                                    if self.tasks[u'清理智']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxClearSan.stateChanged.connect(self.onClearSanStateChanged)
        itemClearSan = QListWidgetItem()
        self.ui.listWTask.addItem(itemClearSan)
        self.ui.listWTask.setItemWidget(itemClearSan, self.checkBoxClearSan)
        # 领取奖励
        self.agenTools.taskFlags[self.tasks[u'领取奖励']['key']] = self.tasks['领取奖励']['checked']
        self.checkBoxRA = QCheckBox(text=u"领取奖励")
        self.checkBoxRA.setStyleSheet(
            "color: rgb(255, 255, 255);"
        )
        self.checkBoxRA.setCheckState(Qt.CheckState.Checked
                                    if self.tasks[u'领取奖励']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxRA.stateChanged.connect(self.onRAStateChanged)
        itemRA = QListWidgetItem()
        self.ui.listWTask.addItem(itemRA)
        self.ui.listWTask.setItemWidget(itemRA, self.checkBoxRA)
    
    # 槽    
    def onPBtnSE_clicked(self):
        if not self.isRun:
            self.agenThread.start()
            self.isRun = True
            self.ui.pBtnSE.setText(u"停止")
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            # 终止脚本线程
            # self.agenThread.join()
            # 尝试
            # 在一个隐藏的窗口的执行该守护线程, 停止即关闭窗口
            self.agenThread = threading.Thread(target=self.agenTools.start_ark,
                                               kwargs={"path_emulator": self.path_emulator})
            self.agenThread.setDaemon(True)
            self.isRun = False
            self.ui.pBtnSE.setText(u"开始")
            if self.ui.stackedWidget.currentIndex() == 1:
                self.ui.stackedWidget.setCurrentIndex(0)
    
    def onStartEmStateChanged(self):
        self.agenTools.taskFlags[self.tasks[u'启动模拟器']['key']] = self.checkBoxStartEm.isChecked()
        self.tasks[u'启动模拟器']['checked'] = self.checkBoxStartEm.isChecked()
        self.sav_json()
    
    def onStartGameStateChanged(self):
        self.agenTools.taskFlags[self.tasks[u'启动游戏']['key']] = self.checkBoxStartGame.isChecked()
        self.tasks[u'启动游戏']['checked'] = self.checkBoxStartGame.isChecked()
        self.sav_json()
    
    def onClearSanStateChanged(self):
        self.agenTools.taskFlags[self.tasks[u'清理智']['key']] = self.checkBoxClearSan.isChecked()
        self.tasks[u'清理智']['checked'] = self.checkBoxClearSan.isChecked()
        self.sav_json()
    
    def onRAStateChanged(self):
        self.agenTools.taskFlags[self.tasks[u'领取奖励']['key']] = self.checkBoxRA.isChecked()
        self.tasks[u'领取奖励']['checked'] = self.checkBoxRA.isChecked()
        self.sav_json()
        
    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
            
    def mouseDoubleClickEvent(self, event):
        if (
            Qt.MouseButton.LeftButton 
            and event.pos().y() < self.ui.titleBar.height()
        ):
            self.restore_or_maximize_window()
        return super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MouseButton.LeftButton 
            and event.pos().y() < self.ui.titleBar.height()
            and self.isMaximized() == False
        ):
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))  # 更改鼠标图标
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if Qt.MouseButton.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        return super().mouseReleaseEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec())
