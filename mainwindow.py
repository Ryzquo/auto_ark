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
        # logo
        self.icon_path = os.path.join(self.dir, "images/ui/logo.png").replace('\\', '/')
        # 代理
        self.agenTools = AgenTools()
        
        # 窗口图标
        self.setWindowIcon(QIcon(self.icon_path))
        # 托盘
        self.initTray()
        # 任务列表
        self.initTaskList()
        # 槽
        self.ctConnect()
        
        # 脚本线程
        self.agenThread = threading.Thread(target=self.agenTools.start_ark,
                                           kwargs={"path_emulator": self.path_emulator})
        self.agenThread.setDaemon(True)
        
        # 一些标志
        # 脚本执行
        self.isRun = False
        # 切换日志前的页面
        self.lastPage = 0
        
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
        self.ui.pBtnLog.clicked.connect(self.onPBtnLog_clicked)
        self.ui.pBtnMaximize.clicked.connect(self.restore_or_maximize_window)
        
    def initTray(self):
        """
        初始化托盘
        """
        # 菜单项
        quit_action = QAction(u"退出", self, triggered=self.quit)
        
        # 托盘菜单
        tray_menu = QMenu(self)
        tray_menu.addAction(quit_action)
        # 样式
        tray_menu.setStyleSheet(
            "QMenu{"
            "padding: 2px;"
            "font: 11pt \"黑体\";"
            "color: rgba(255, 255, 255, .8);"
            "background-color: rgba(56, 57, 60, 1);"
            "border: 3px solid rgba(56, 57, 60, 1);"
            "border-radius: 6px;"
            "}"
            "QMenu:item{"
            "padding: 2px;"
            "background-color: rgba(86, 88, 93, 1);"
            "border: 3px solid rgba(86, 88, 93, 1);"
            "border-radius: 6px;"
            "}"
        )
        
        # 托盘图标
        self.tray = QSystemTrayIcon(self)
        self.tray.setContextMenu(tray_menu)
        self.tray.setIcon(QIcon(self.icon_path))
        self.tray.show()
        
    def initTaskList(self):
        """
        初始化任务列表
        """
        # 启动模拟器
        self.agenTools.taskFlags[self.tasks[u'启动模拟器']['key']] = self.tasks['启动模拟器']['checked']

        self.checkBoxStartEm = QCheckBox(text=u"启动模拟器")
        self.pBtnStartEm = QPushButton(text=u"设置")
        itemWidget = QWidget()
        hBox = QHBoxLayout(itemWidget)
        hBox.addWidget(self.checkBoxStartEm)
        hBox.addWidget(self.pBtnStartEm)
        self.setPBtnCBoxStyle(cBox=self.checkBoxStartEm, pBtn=self.pBtnStartEm)
        self.checkBoxStartEm.setCheckState(Qt.CheckState.Checked 
                                    if self.tasks[u'启动模拟器']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxStartEm.stateChanged.connect(self.onStartEmStateChanged)
        itemStartEm = QListWidgetItem()
        self.ui.listWTask.addItem(itemStartEm)
        self.ui.listWTask.setItemWidget(itemStartEm, itemWidget)
        # 启动游戏
        self.agenTools.taskFlags[self.tasks[u'启动游戏']['key']] = self.tasks['启动游戏']['checked']
        self.checkBoxStartGame = QCheckBox(text=u"启动游戏")
        self.pBtnStartGame = QPushButton(text=u"设置")
        itemWidget = QWidget()
        hBox = QHBoxLayout(itemWidget)
        hBox.addWidget(self.checkBoxStartGame)
        hBox.addWidget(self.pBtnStartGame)
        self.setPBtnCBoxStyle(cBox=self.checkBoxStartGame, pBtn=self.pBtnStartGame)
        self.checkBoxStartGame.setCheckState(Qt.CheckState.Checked
                                    if self.tasks[u'启动游戏']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxStartGame.stateChanged.connect(self.onStartGameStateChanged)
        itemStartGame = QListWidgetItem()
        self.ui.listWTask.addItem(itemStartGame)
        self.ui.listWTask.setItemWidget(itemStartGame, itemWidget)
        # 清理智
        self.agenTools.taskFlags[self.tasks[u'清理智']['key']] = self.tasks['清理智']['checked']
        self.checkBoxClearSan = QCheckBox(text=u"清理智")
        self.pBtnClearSan = QPushButton(text=u"设置")
        itemWidget = QWidget()
        hBox = QHBoxLayout(itemWidget)
        hBox.addWidget(self.checkBoxClearSan)
        hBox.addWidget(self.pBtnClearSan)
        self.setPBtnCBoxStyle(cBox=self.checkBoxClearSan, pBtn=self.pBtnClearSan)
        self.checkBoxClearSan.setCheckState(Qt.CheckState.Checked
                                    if self.tasks[u'清理智']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxClearSan.stateChanged.connect(self.onClearSanStateChanged)
        itemClearSan = QListWidgetItem()
        self.ui.listWTask.addItem(itemClearSan)
        self.ui.listWTask.setItemWidget(itemClearSan, itemWidget)
        # 领取奖励
        self.agenTools.taskFlags[self.tasks[u'领取奖励']['key']] = self.tasks['领取奖励']['checked']
        self.checkBoxRA = QCheckBox(text=u"领取奖励")
        self.pBtnRA = QPushButton(text=u"设置")
        itemWidget = QWidget()
        hBox = QHBoxLayout(itemWidget)
        hBox.addWidget(self.checkBoxRA)
        hBox.addWidget(self.pBtnRA)
        self.setPBtnCBoxStyle(cBox=self.checkBoxRA, pBtn=self.pBtnRA)
        self.checkBoxRA.setCheckState(Qt.CheckState.Checked
                                    if self.tasks[u'领取奖励']['checked'] 
                                    else Qt.CheckState.Unchecked)
        self.checkBoxRA.stateChanged.connect(self.onRAStateChanged)
        itemRA = QListWidgetItem()
        self.ui.listWTask.addItem(itemRA)
        self.ui.listWTask.setItemWidget(itemRA, itemWidget)
    
    def setPBtnCBoxStyle(
        self, 
        cBox: QCheckBox, pBtn: QPushButton
    ):
        """
        设置列表中复选框和按钮的样式
        """
        styleSheet = (
            "QPushButton{"
            "background-color: transparent;"
            "}"
            "QCheckBox, QPushButton {"
            "color: rgba(255, 255, 255, .8);"
            "}"
            "QCheckBox:hover, QPushButton:hover {"
            "color: rgba(255, 255, 255, 1);"
            "}"
        )
        
        pBtn.setStyleSheet(styleSheet)
        cBox.setStyleSheet(styleSheet)
    
    # 槽    
    def onPBtnSE_clicked(self):
        """
        开始与停止按钮
        """
        if not self.isRun:
            self.agenThread.start()
            self.isRun = True
            self.ui.pBtnSE.setText(u"停止")
            self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.isRun = False
            self.ui.pBtnSE.setText(u"开始")
            if self.ui.stackedWidget.currentIndex() == 1:
                self.ui.stackedWidget.setCurrentIndex(0)
            self.agenThread = threading.Thread(target=self.agenTools.start_ark,
                                               kwargs={"path_emulator": self.path_emulator})
            self.agenThread.setDaemon(True)
            
    def onPBtnLog_clicked(self):
        """
        显示与隐藏日志
        """
        if self.ui.stackedWidget.currentIndex() != 1:
                self.ui.stackedWidget.setCurrentIndex(1)
        else:
            self.ui.stackedWidget.setCurrentIndex(self.lastPage)
            
    def quit(self):
        """
        退出
        """
        self.close()
        sys.exit()
            
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
        """
        控制最大化
        """
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
            
    def mouseDoubleClickEvent(self, event):
        # 双击标题栏最大化
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
        # 拖动窗口
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
