#!/user/bin/env python
# -*- coding: utf-8 -*-

import sys

from PySide6.QtWidgets import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
    def initStyle(self):
        """
        初始化窗口样式
        """
        ...
        
    def initControl(self):
        """
        初始化窗口控件
        """
        ...


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec())
