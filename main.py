#!/user/bin/env python
# -*- coding: utf-8 -*-

import agen_tools


if __name__ == "__main__":
    
    # 模拟器路径
    path_emulator = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/BlueStacks 5.lnk"
    
    # agen_tools.start_ark(path_emulator=path_emulator)
    # # agen_tools.startup()
    # agen_tools.clear_san("WB-9")
    # agen_tools.stop_ark()

    try:
        agen_tools.start_ark(path_emulator=path_emulator)
        # agen_tools.startup()
        agen_tools.clear_san("WB-9")
        agen_tools.stop_ark()
    except Exception as e:
        print(f"error: {e}")
    