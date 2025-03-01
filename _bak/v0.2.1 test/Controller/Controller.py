# -*- coding: utf-8 -*-

# PyQt5: pyuic5 -o View.py View.ui

''' ***** 自定义包,类 ***** '''
from View import *
from Util.Message import Message
from Model.Seg import SegFile,DataTtrack
from Controller.MyFigureCanvas import MyFigureCanvas
# from Controller.Algorithm import *

''' ==================== ↓  控制   ↓ ==================== '''
class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(Controller, self).__init__()  # 先调用父类的构造函数
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUi()   # 界面初始设置
        self.connect()  # 绑定信号槽
        self.addPainteWidget() #添加绘图控件
        
        self.stateDiagram = 0 #程序状态控制 —— 用于切换不同界面控制：0.初始状态、1.已加载文件、2.已完成FFT、3.已完成CWT、4、已完成LSTM

    def initUi(self):       # 界面初始设置
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.toolButton_Home_clicked()

    '''  ↓ 添加绘图控件 ↓    '''
    def addPainteWidget(self):

        self.pushButton123 = QtWidgets.QPushButton(self.ui.page_Canvas_Home)
        self.pushButton123.setObjectName("pushButton123")
        self.ui.gridLayout_Canvas_Home.addWidget(self.pushButton123, 3, 0, 2, 1)


        self.paintHome = MyFigureCanvas(self.ui.page_Canvas_Home)
        self.ui.gridLayout_Canvas_Home.addWidget(self.paintHome)

        self.paintFFT = MyFigureCanvas(self.ui.page_Canvas_FFT)
        self.ui.gridLayout_Canvas_FFT.addWidget(self.paintFFT,1,0,1,1)
        
        self.paintCWT = MyFigureCanvas(self.ui.page_Canvas_CWT)
        self.ui.gridLayout_Canvas_CWT.addWidget(self.paintCWT)

        # self.paintLSTM = MyFigureCanvas()
        # self.ui.gridLayout_Canvas_LSTM.addWidget(self.paintLSTM)

 
    def connect(self):  # 绑定信号槽
        # 绑定导航栏按钮
        self.ui.toolButton_Home.clicked.connect(self.toolButton_Home_clicked)
        self.ui.toolButton_FFT.clicked.connect(self.toolButton_FFT_clicked)
        self.ui.toolButton_CWT.clicked.connect(self.toolButton_CWT_clicked)
        self.ui.toolButton_LSTM.clicked.connect(self.toolButton_LSTM_clicked)
        self.ui.toolButton_Set.clicked.connect(self.toolButton_Set_clicked)

        # 绑定meanBar
        self.ui.opeanFile.triggered.connect(self.menu_opeanFile)

    '''  -------------------- ↓ 菜单栏事件 ↓ --------------------  '''

    def menu_opeanFile(self):
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(
            self, "选取文件", "C:/", "seg Files (*.seg)")  # 设置文件扩展名过滤,注意用双分号间隔

        if fileName == '' :
            QtWidgets.QMessageBox.warning(
                    self, "Warning", Message().dict['Error(1002)'], QtWidgets.QMessageBox.Yes)
        else:
            self.segFile = SegFile()
            
            reply = self.segFile.loadFile(fileName)
            if(reply != 0):
                QtWidgets.QMessageBox.warning(
                    self, "Warning", Message().dict[reply], QtWidgets.QMessageBox.Yes)
            else:
                self.stateDiagram = 1 # 1-已加载文件
                
                # self.paintFFT.figure.clf()
                # for i in range(0,self.segFile.tapeNum):
                # for i in range(0,1):
                #     self.paintCWT.setAx(i,self.segFile.tapeNum)
                #     self.paintCWT.paint(self.segFile.dataList[i].data,i)
                #### self.paintFFT.canvas.draw() #在画布上绘制

                #self.paintHome.figure.clf()
                # for i in range(0,self.segFile.tapeNum):
                for i in range(0,1):
                    self.paintHome.setAx(i,self.segFile.tapeNum)
                    self.paintHome.paint(self.segFile.dataList[i].data,i)
                self.paintHome.canvas.draw() #在画布上绘制
 
    # 导航栏更新

    def toolButton_NavigationBar_Update(self, i):
        # 设置导航栏颜色
        p = QtGui.QPalette() # 调色板
        p.setColor(QtGui.QPalette.Button, QtGui.QColor(44, 44, 44))     # 灰黑色

        self.ui.toolButton_Home.setPalette(p)
        self.ui.toolButton_FFT.setPalette(p)
        self.ui.toolButton_CWT.setPalette(p)
        self.ui.toolButton_LSTM.setPalette(p)
        self.ui.toolButton_Set.setPalette(p)

        p.setColor(QtGui.QPalette.Button, QtGui.QColor(128, 128, 128))  # 灰色
        if i == 0:
            self.ui.toolButton_Home.setPalette(p)
        if i == 1:
            self.ui.toolButton_FFT.setPalette(p)
        if i == 2:
            self.ui.toolButton_CWT.setPalette(p)
        if i == 3:
            self.ui.toolButton_LSTM.setPalette(p)
        if i == 4:
            self.ui.toolButton_Set.setPalette(p)

        self.ui.stackedWidget_Panel.setCurrentIndex(i)
        self.ui.stackedWidget_Canvs.setCurrentIndex(i)

    def toolButton_Home_clicked(self):
        self.toolButton_NavigationBar_Update(0)

    def toolButton_FFT_clicked(self):
        if self.stateDiagram >=1: # 1-已加载文件
            self.toolButton_NavigationBar_Update(1)
            self.stateDiagram = 2
        else:
            QtWidgets.QMessageBox.warning(
                 self, "Warning", Message().dict['Warning(1001)'], QtWidgets.QMessageBox.Yes)
    
    def toolButton_CWT_clicked(self):
        if self.stateDiagram >=2: # 2-已完成FFT
            self.toolButton_NavigationBar_Update(2)
        else:
            QtWidgets.QMessageBox.warning(
                 self, "Warning", Message().dict['Warning(1002)'], QtWidgets.QMessageBox.Yes)
    
    def toolButton_LSTM_clicked(self):
        if self.stateDiagram >=3: # 3-已完成CWT
            self.toolButton_NavigationBar_Update(3)
        else:
            QtWidgets.QMessageBox.warning(
                 self, "Warning", Message().dict['Warning(1003)'], QtWidgets.QMessageBox.Yes)
    
    def toolButton_Set_clicked(self):
        if self.stateDiagram >=1: # 1-已加载文件
            self.toolButton_NavigationBar_Update(4)
        else:
            QtWidgets.QMessageBox.warning(
                 self, "Warning", Message().dict['Warning(1001)'], QtWidgets.QMessageBox.Yes)
    
