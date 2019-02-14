#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

from PyQt5.QtWidgets import QWidget, QMainWindow, QDesktopWidget,\
                            QHBoxLayout, QVBoxLayout, QGridLayout, QGroupBox,\
                            QAction, QLabel, QPushButton, QComboBox, QSpinBox, QLineEdit, QTextEdit

from PyQt5.QtGui import QIcon, QImage, QPixmap, QPainter, QColor, QLinearGradient, QFont
from PyQt5.QtCore import Qt

import pyqtgraph as pg

from celluar import Celluar


class Seir(QMainWindow):
    """
    程序主窗口
    """
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # 生成组件
        self.labmap = QLabel()  # 背景地图
        self.labmap.setFixedSize(1000, 400)
        img = QImage(r'resource/map/citymap.png')
        result = img.scaled(self.labmap.width(), self.labmap.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.labmap.setPixmap(QPixmap.fromImage(result))

        self.pltfunc = pg.PlotWidget(title='人员状态变化情况')  # 绘制函数
        self.pltfunc.setStatusTip('函数绘制窗口')
        self.pltfunc.showGrid(x=True, y=True)
        self.pltfunc.addLegend()
        self.pltfunc.setLabel('left', 'Value', units='人数')
        self.pltfunc.setLabel('bottom', 'Time', units='天数')
        self.pltfunc.setXRange(0, 365)

        self.btnstart = QPushButton('开始仿真')
        self.btnpause = QPushButton('暂停仿真')

        self.cbbdisease = QComboBox()  # 选择传染病下拉列表框
        self.cbbdisease.addItems(['流行感冒', '痢疾', '肺结核', '艾滋病', '传染性非典型肺炎'])

        self.spbday = QSpinBox()  # 设置仿真天数
        self.spbday.setRange(10, 365)
        self.spbday.setValue(30)

        # 以下是提示标签组件
        self.lab_disease_color = QLabel()  # 染病程度颜色标签
        labcolorwidth, labcolorheight = 160, 30
        self.lab_disease_color.setFixedSize(labcolorwidth, labcolorheight)
        pixmap = QPixmap(labcolorwidth, labcolorheight)
        painter = QPainter()
        painter.begin(pixmap)
        linearGradient = QLinearGradient(0, labcolorheight/2, labcolorwidth, labcolorheight/2)
        linearGradient.setColorAt(0, Qt.green)
        linearGradient.setColorAt(0.34, QColor(255, 255, 0))
        linearGradient.setColorAt(0.66, QColor(255, 125, 0))
        linearGradient.setColorAt(1, Qt.red)
        painter.setPen(Qt.NoPen)
        painter.setBrush(linearGradient)
        painter.drawRect(0, 0, labcolorwidth, labcolorheight)
        painter.end()
        self.lab_disease_color.setPixmap(pixmap)

        self.labcolor = QLabel()
        self.labcolor.setText('地区感染程度')

        self.labdisease = QLabel()
        self.labdisease.setText('设置传染病')

        self.labday = QLabel()
        self.labday.setText('设置仿真天数')


        # 设置布局
        self.widget = QWidget()
        self.mainHBox = QHBoxLayout()
        self.leftVBox = QVBoxLayout()
        self.rightVBox = QVBoxLayout()

        self.decriptionGroupBox = QGroupBox("程序说明")
        self.decriptionGroupBox.setStyleSheet("QGroupBox{font-family:'黑体'; font-size: 15px}")
        self.decriptionGBox = QGridLayout()
        self.decriptionGBox.setColumnStretch(3, 10)
        self.decriptionGBox.setRowStretch(1, 10)

        self.settingGroupBox = QGroupBox('参数设置')
        self.settingGroupBox.setStyleSheet("QGroupBox{font-family:'黑体'; font-size: 15px}")
        self.settingGBox = QGridLayout()
        self.settingGBox.setColumnStretch(3, 10)
        self.settingGBox.setRowStretch(2, 10)

        self.ctrlGroupBox = QGroupBox('仿真控制')
        self.ctrlGroupBox.setStyleSheet("QGroupBox{font-family:'黑体'; font-size: 15px}")
        self.ctrlGBox = QGridLayout()
        self.ctrlGBox.setColumnStretch(0, 10)
        self.ctrlGBox.setColumnStretch(2, 10)

        # 布局添加组件
        # =================以下添加组件======================
        self.decriptionGBox.addWidget(self.labcolor, 0, 0)  # 程序说明部分
        self.decriptionGBox.addWidget(self.lab_disease_color, 0, 1)


        self.settingGBox.addWidget(self.labdisease, 0, 0, 1, 1)  # 设置参数部分
        self.settingGBox.addWidget(self.cbbdisease, 0, 1, 1, 1)
        self.settingGBox.addWidget(self.labday, 1, 0, 1, 1)
        self.settingGBox.addWidget(self.spbday, 1, 1, 1, 1)

        self.ctrlGBox.addWidget(self.btnstart, 0, 1)  # 控制仿真部分
        self.ctrlGBox.addWidget(self.btnpause, 1, 1)




        # 宏观地图元胞生成
        self.citymap = {}
        for x in range(0, 20):
            for y in range(0, 8):
                self.citymap[(x, y)] = Celluar(str((y, x)), self.labmap)  # 地区编号 (行, 列)
                self.citymap[(x, y)].setGeometry(50*x, 50*y, 50, 50)

        # 社区地图生成
        w, h = self.labmap.size().width(), self.labmap.size().height()
        communitypixmap = QPixmap(w, h)
        painter = QPainter()
        painter.begin(communitypixmap)
        font = QFont()
        font.setPixelSize(32)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(20, 100, '开发中......')
        painter.end()

        self.communitymap = QLabel(self.labmap)
        self.communitymap.setGeometry(0, 0, w, h)
        self.communitymap.setPixmap(communitypixmap)
        self.communitymap.hide()


        # ===================================================
        self.decriptionGroupBox.setLayout(self.decriptionGBox)
        self.settingGroupBox.setLayout(self.settingGBox)
        self.ctrlGroupBox.setLayout(self.ctrlGBox)

        self.leftVBox.addWidget(self.labmap)
        self.leftVBox.addWidget(self.pltfunc)
        self.rightVBox.addWidget(self.decriptionGroupBox)
        self.rightVBox.addWidget(self.settingGroupBox)
        self.rightVBox.addWidget(self.ctrlGroupBox)

        self.mainHBox.addLayout(self.leftVBox)
        self.mainHBox.addLayout(self.rightVBox)

        self.widget.setLayout(self.mainHBox)
        self.setCentralWidget(self.widget)

        # 生成行动
        self.initAction()

        # 设置主窗口菜单栏、状态栏
        self.mainMenubar = self.menuBar()

        self.fileMenu = self.mainMenubar.addMenu('文件(&F)')
        self.fileMenu.addAction(self.quitAction)

        self.toggleViewMenu = self.mainMenubar.addMenu('切换仿真方式(&T)')
        self.toggleViewMenu.addAction(self.toggleCityViewAction)
        self.toggleViewMenu.addAction(self.toggleCommunityViewAction)

        self.setDeseaseMenu = self.mainMenubar.addMenu('设置传染病参数(&S)')
        self.helpMenu = self.mainMenubar.addMenu('帮助(&H)')


        self.statusbar = self.statusBar()
        # 设置主窗口大小，居中，标题
        self.setGeometry(300, 300, 1280, 720)
        self.setMinimumSize(1280, 720)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowIcon(QIcon('resource/icons/MainWindowIcon.png'))
        self.setWindowTitle('传染病仿真程序')

    def initAction(self):
        # 生成行动
        self.quitAction = QAction(QIcon(r'resource/icons/quit.png'), '退出程序', self)
        self.quitAction.setShortcut('Ctrl+Q')
        self.quitAction.setStatusTip('退出仿真程序')
        self.quitAction.triggered.connect(self.close)

        self.toggleCityViewAction = QAction('宏观视图', self)
        self.toggleCityViewAction.triggered.connect(self.communitymap.hide)

        self.toggleCommunityViewAction = QAction('社区视图', self)
        self.toggleCommunityViewAction.triggered.connect(self.communitymap.show)


