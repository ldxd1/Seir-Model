#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from PyQt5.QtWidgets import QPushButton, QMenu, QAction, QFontDialog

from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt
from qss import Qss


class Celluar(QPushButton):
    def __init__(self, identifier, parent):
        super().__init__()
        self.setParent(parent)
        self.initAction()
        self.initContextMenu()
        self.initStyleSheet()

        self.setText('H')
        self.clicked.connect(self.changeHuman)

        self.tooltiptext = '地区编号：' + identifier + '\n地区人数：11451人\n感染人数：5086人\n感染情况：中等'
        self.setToolTip(self.tooltiptext)
        self.setStatusTip('宏观仿真地图')

    def initAction(self):
        self.setRelatedCelluarAction = QAction('设置关联地区', self)
        self.setRelatedCelluarAction.setStatusTip('仿真时，关联地区将直接影响本地区')

    def initStyleSheet(self):
        self.qstylesheet = Qss('QPushButton')
        self.qstylesheet.setPro('color', 'none', 'black')
        self.qstylesheet.setPro('background', 'none', 'rgba(255, 0, 0, 30%)')
        self.qstylesheet.setPro('border', 'color', 'rgba(180,180,180,100%)')
        self.qstylesheet.setPro('border', 'width', '1px')
        self.qstylesheet.setPro('border', 'style', 'solid')
        self.qstylesheet.setPro('font', 'size', '30px')
        self.qstylesheet.setPro('color', 'none', 'black')

        self.qstylesheet.setPro('background', 'none', 'rgba(0, 205, 205, 80)', 'pressed')

        self.qstylesheet.setPro('border', 'color', 'rgba(0, 0, 0, 255)', 'hover')
        self.qstylesheet.setPro('background', 'none', 'rgba(50, 225, 225, 60)', 'hover')

        self.setStyleSheet(self.qstylesheet.getPropertyValueText())

    def initContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)

        self.contextMenu.addAction(self.setRelatedCelluarAction)
        self.contextMenu.addAction(QAction('仅供测试，功能未实装', self))

    def showContextMenu(self, pos):
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示
        # self.contextMenu.show()

    def setColor(self, r, g, b, a):
        rgba = 'rgba({0}, {1}, {2}, {3})'.format(r, g, b, a)
        self.qstylesheet.setPro('background', 'none', rgba)
        self.setStyleSheet(self.qstylesheet.getPropertyValueText())

    def changeHuman(self):
        human = self.text()
        if human == 'H':
            self.setText('L')
        elif human == 'M':
            self.setText('H')
        elif human == 'L':
            self.setText('M')

