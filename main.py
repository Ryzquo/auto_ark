#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'ark_tools/').replace('\\', '/'))
from ark_tools.agen_tools import AgenTools

if __name__ == "__main__":

    # 模拟器路径
    path_emulator = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/BlueStacks 5.lnk"

    agenTools = AgenTools()

    try:
        agenTools.taskFlags['START_EMULATOR'] = True
        agenTools.taskFlags['CLEAR_SAN'] = True
        agenTools.taskFlags['RECEIVE_AWARD'] = True
        agenTools.start_ark(path_emulator=path_emulator)
        agenTools.stop_ark()
    except Exception as e:
        print(f"error: {e}")
