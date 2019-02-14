#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
import sys


class PropertyValue(object):
    def __init__(self):
        self.color = {'none': 'black'}
        self.background = {'none': 'gray'}
        self.border = {'none': None}
        self.font = {'none': None}

    def setSuffixValue(self, pro, suffix, value):
        exec("self.{0}['{1}'] = '{2}'".format(pro, suffix, value))

    def getText(self):
        result = ''
        for key, value in vars(self).items():
            for k, v in value.items():
                if k == 'none':
                    if v:
                        result += '{0}:{1};'.format(key, v)
                else:
                    result += '{0}-{1}:{2};'.format(key, k, v)
        return result[:-1]


class Qss(object):
    def __init__(self, widget):
        self.widget = widget
        none = PropertyValue()
        pressed = PropertyValue()
        hover = PropertyValue()

        # 不要更改字典键-值对的顺序！
        self.pro = {'none': none, 'hover': hover, 'pressed': pressed}

    def setPro(self, pro, suffix, value, status='none'):
        self.pro[status].setSuffixValue(pro, suffix, value)

    def getPropertyValueText(self):
        result = ''
        for key, value in self.pro.items():
            if key == 'none':
                result = result + self.widget + '{' + value.getText() + '}' + '\n'
            else:
                result = result + self.widget + ':' + key + '{' + value.getText() + '}' + '\n'
        return result


# 测试驱动程序
if '__main__' == __name__:
    qss = Qss('QPushButton')
    qss.setPro('background', 'none', 'yellow', 'pressed')
    qss.setPro('background', 'none', 'cyan', 'hover')

    app = QApplication(sys.argv)
    w = QWidget()

    ptn = QPushButton('ok', w)
    ptn.setStyleSheet(qss.getPropertyValueText())

    w.show()
    sys.exit(app.exec_())

