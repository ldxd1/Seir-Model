#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# ======================================
# 2019-2-1
# 一个简单的SEIR模型仿真测试
# 作者：Panda
# For 19挑战杯及课堂考勤系统讨论组
# ======================================

import sys
from PyQt5.QtWidgets import QApplication
from seir import Seir

if '__main__' == __name__:
    app = QApplication(sys.argv)
    w = Seir()
    w.show()
    sys.exit(app.exec_())
