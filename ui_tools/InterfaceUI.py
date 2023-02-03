# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InterfaceUI.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
import ui_tools.rec

class Ui_InterfaceUI(object):
    def setupUi(self, InterfaceUI):
        if not InterfaceUI.objectName():
            InterfaceUI.setObjectName(u"InterfaceUI")
        InterfaceUI.resize(842, 549)
        self.centralwidget = QWidget(InterfaceUI)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"#frame{\n"
"	background-color: rgba(56, 57, 60, 1);\n"
"	border-radius: 20px;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.titleBar = QFrame(self.frame)
        self.titleBar.setObjectName(u"titleBar")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.titleBar.sizePolicy().hasHeightForWidth())
        self.titleBar.setSizePolicy(sizePolicy)
        self.titleBar.setStyleSheet(u"#titleBar{\n"
"	background-color: rgba(86, 88, 93, 1);\n"
"	border-top-left-radius: 20px;\n"
"	border-top-right-radius: 20px;\n"
"}")
        self.titleBar.setFrameShape(QFrame.StyledPanel)
        self.titleBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.titleBar)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.logoTitle = QFrame(self.titleBar)
        self.logoTitle.setObjectName(u"logoTitle")
        self.logoTitle.setMinimumSize(QSize(100, 0))
        self.logoTitle.setMaximumSize(QSize(160, 16777215))
        self.logoTitle.setStyleSheet(u"#labTitle{\n"
"	font: 14pt \"\u534e\u6587\u96b6\u4e66\";\n"
"	color: rgb(255, 255, 255);\n"
"}")
        self.logoTitle.setFrameShape(QFrame.StyledPanel)
        self.logoTitle.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.logoTitle)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.labLogo = QLabel(self.logoTitle)
        self.labLogo.setObjectName(u"labLogo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.labLogo.sizePolicy().hasHeightForWidth())
        self.labLogo.setSizePolicy(sizePolicy1)
        self.labLogo.setMinimumSize(QSize(20, 20))
        self.labLogo.setMaximumSize(QSize(30, 30))
        self.labLogo.setPixmap(QPixmap(u":/logo.png"))
        self.labLogo.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.labLogo)

        self.horizontalSpacer = QSpacerItem(15, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.labTitle = QLabel(self.logoTitle)
        self.labTitle.setObjectName(u"labTitle")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labTitle.sizePolicy().hasHeightForWidth())
        self.labTitle.setSizePolicy(sizePolicy2)
        self.labTitle.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.labTitle)


        self.horizontalLayout_2.addWidget(self.logoTitle)

        self.widgetTool = QFrame(self.titleBar)
        self.widgetTool.setObjectName(u"widgetTool")
        self.widgetTool.setMinimumSize(QSize(160, 0))
        self.widgetTool.setStyleSheet(u"#widgetTool{\n"
"	border-top-right-radius: 20px;\n"
"}\n"
"\n"
"QPushButton{\n"
"	border: none;\n"
"}\n"
"QPushButton:hover{\n"
"	padding-bottom: 5px;\n"
"}\n"
"#pBtnClose:hover{\n"
"	border-top-right-radius: 20px;\n"
"	background-color: rgba(170, 0, 0, .5);\n"
"}\n"
"#pBtnMinimize:hover, #pBtnMaximize:hover{\n"
"	background-color: rgba(0, 0, 0, .5);\n"
"}")
        self.widgetTool.setFrameShape(QFrame.StyledPanel)
        self.widgetTool.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.widgetTool)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 0, 0)
        self.pBtnMaximize = QPushButton(self.widgetTool)
        self.pBtnMaximize.setObjectName(u"pBtnMaximize")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pBtnMaximize.sizePolicy().hasHeightForWidth())
        self.pBtnMaximize.setSizePolicy(sizePolicy3)
        self.pBtnMaximize.setMinimumSize(QSize(0, 0))
        icon = QIcon()
        icon.addFile(u":/maximize_w.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pBtnMaximize.setIcon(icon)
        self.pBtnMaximize.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pBtnMaximize)

        self.pBtnMinimize = QPushButton(self.widgetTool)
        self.pBtnMinimize.setObjectName(u"pBtnMinimize")
        sizePolicy3.setHeightForWidth(self.pBtnMinimize.sizePolicy().hasHeightForWidth())
        self.pBtnMinimize.setSizePolicy(sizePolicy3)
        self.pBtnMinimize.setMinimumSize(QSize(0, 0))
        icon1 = QIcon()
        icon1.addFile(u":/minimize_w.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pBtnMinimize.setIcon(icon1)
        self.pBtnMinimize.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pBtnMinimize)

        self.pBtnClose = QPushButton(self.widgetTool)
        self.pBtnClose.setObjectName(u"pBtnClose")
        sizePolicy3.setHeightForWidth(self.pBtnClose.sizePolicy().hasHeightForWidth())
        self.pBtnClose.setSizePolicy(sizePolicy3)
        self.pBtnClose.setMinimumSize(QSize(0, 0))
        icon2 = QIcon()
        icon2.addFile(u":/close_w.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pBtnClose.setIcon(icon2)
        self.pBtnClose.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pBtnClose)


        self.horizontalLayout_2.addWidget(self.widgetTool, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.titleBar)

        self.subWidget = QFrame(self.frame)
        self.subWidget.setObjectName(u"subWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(14)
        sizePolicy4.setHeightForWidth(self.subWidget.sizePolicy().hasHeightForWidth())
        self.subWidget.setSizePolicy(sizePolicy4)
        self.subWidget.setStyleSheet(u"")
        self.subWidget.setFrameShape(QFrame.StyledPanel)
        self.subWidget.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.subWidget)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.widgetTask = QFrame(self.subWidget)
        self.widgetTask.setObjectName(u"widgetTask")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(3)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widgetTask.sizePolicy().hasHeightForWidth())
        self.widgetTask.setSizePolicy(sizePolicy5)
        self.widgetTask.setStyleSheet(u"#listWTask{\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(66, 66, 78, 1);\n"
"	border: 5px solid rgba(66, 66, 78, 1);\n"
"	border-radius: 10px;\n"
"}\n"
"#listWTask::item {\n"
"}\n"
"#listWTask::item:hover {\n"
"}\n"
"#listWTask::item:selected {\n"
"}\n"
"\n"
"#pBtnSE{\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"\u9ed1\u4f53\";\n"
"	background-color: rgba(86, 88, 93, 1);\n"
"	border-radius: 10px;\n"
"}\n"
"#pBtnSE:hover{\n"
"	background-color: rgba(86, 88, 93, .5);\n"
"}")
        self.widgetTask.setFrameShape(QFrame.StyledPanel)
        self.widgetTask.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.widgetTask)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.widgetTaskList = QFrame(self.widgetTask)
        self.widgetTaskList.setObjectName(u"widgetTaskList")
        self.widgetTaskList.setFrameShape(QFrame.StyledPanel)
        self.widgetTaskList.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.widgetTaskList)
        self.verticalLayout_4.setSpacing(12)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 6, 6, 6)
        self.listWTask = QListWidget(self.widgetTaskList)
        self.listWTask.setObjectName(u"listWTask")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(10)
        sizePolicy6.setHeightForWidth(self.listWTask.sizePolicy().hasHeightForWidth())
        self.listWTask.setSizePolicy(sizePolicy6)

        self.verticalLayout_4.addWidget(self.listWTask)

        self.fbtn = QFrame(self.widgetTaskList)
        self.fbtn.setObjectName(u"fbtn")
        sizePolicy.setHeightForWidth(self.fbtn.sizePolicy().hasHeightForWidth())
        self.fbtn.setSizePolicy(sizePolicy)
        self.hLayoutPBtn = QHBoxLayout(self.fbtn)
        self.hLayoutPBtn.setObjectName(u"hLayoutPBtn")
        self.horizontalSpacer_3 = QSpacerItem(48, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hLayoutPBtn.addItem(self.horizontalSpacer_3)

        self.pBtnSE = QPushButton(self.fbtn)
        self.pBtnSE.setObjectName(u"pBtnSE")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.pBtnSE.sizePolicy().hasHeightForWidth())
        self.pBtnSE.setSizePolicy(sizePolicy7)
        self.pBtnSE.setStyleSheet(u"")

        self.hLayoutPBtn.addWidget(self.pBtnSE)

        self.horizontalSpacer_2 = QSpacerItem(48, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.hLayoutPBtn.addItem(self.horizontalSpacer_2)


        self.verticalLayout_4.addWidget(self.fbtn)


        self.verticalLayout_5.addWidget(self.widgetTaskList)


        self.horizontalLayout_3.addWidget(self.widgetTask)

        self.widgetCt = QFrame(self.subWidget)
        self.widgetCt.setObjectName(u"widgetCt")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy8.setHorizontalStretch(8)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.widgetCt.sizePolicy().hasHeightForWidth())
        self.widgetCt.setSizePolicy(sizePolicy8)
        self.widgetCt.setFrameShape(QFrame.StyledPanel)
        self.widgetCt.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.widgetCt)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.widgetCt)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.pageSetting = QWidget()
        self.pageSetting.setObjectName(u"pageSetting")
        self.stackedWidget.addWidget(self.pageSetting)
        self.pageLogo = QWidget()
        self.pageLogo.setObjectName(u"pageLogo")
        self.pageLogo.setStyleSheet(u"")
        self.verticalLayout_6 = QVBoxLayout(self.pageLogo)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.fLog = QFrame(self.pageLogo)
        self.fLog.setObjectName(u"fLog")
        self.fLog.setStyleSheet(u"#treeLog{\n"
"	color: rgba(255, 255, 255, 1);\n"
"	font: 11pt \"\u9ed1\u4f53\";\n"
"	background-color: rgba(66, 66, 78, 1);\n"
"	border: 5px solid rgba(66, 66, 78, 1);\n"
"	border-radius: 10px;\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgba(66, 66, 78, 1);\n"
"	border: none;\n"
"	color: rgba(255, 255, 255, 1);\n"
"}\n"
"#treeLog::item{\n"
"	background-color: rgba(66, 66, 78, 0);\n"
"}")
        self.fLog.setFrameShape(QFrame.StyledPanel)
        self.fLog.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.fLog)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.treeLog = QTreeWidget(self.fLog)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font);
        self.treeLog.setHeaderItem(__qtreewidgetitem)
        self.treeLog.setObjectName(u"treeLog")
        font1 = QFont()
        font1.setFamilies([u"\u9ed1\u4f53"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.treeLog.setFont(font1)

        self.horizontalLayout_5.addWidget(self.treeLog)


        self.verticalLayout_6.addWidget(self.fLog)

        self.stackedWidget.addWidget(self.pageLogo)

        self.verticalLayout_3.addWidget(self.stackedWidget)


        self.horizontalLayout_3.addWidget(self.widgetCt)


        self.verticalLayout_2.addWidget(self.subWidget)


        self.verticalLayout.addWidget(self.frame)

        InterfaceUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(InterfaceUI)
        self.pBtnClose.clicked.connect(InterfaceUI.close)
        self.pBtnMinimize.clicked.connect(InterfaceUI.showMinimized)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(InterfaceUI)
    # setupUi

    def retranslateUi(self, InterfaceUI):
        InterfaceUI.setWindowTitle(QCoreApplication.translate("InterfaceUI", u"MainWindow", None))
        self.labLogo.setText("")
        self.labTitle.setText(QCoreApplication.translate("InterfaceUI", u"Auto Ark", None))
        self.pBtnMaximize.setText("")
        self.pBtnMinimize.setText("")
        self.pBtnClose.setText("")
        self.pBtnSE.setText(QCoreApplication.translate("InterfaceUI", u"\u5f00\u59cb", None))
        ___qtreewidgetitem = self.treeLog.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("InterfaceUI", u"\u65e5\u5fd7", None));
    # retranslateUi

