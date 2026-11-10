# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_2.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from user.pyside_guis.notes import *
from user.terroir.music_symbols import *

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, QLine)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsView, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QStatusBar, QWidget, QGraphicsScene)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(835, 459)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.test_button = QPushButton(self.centralwidget)
        self.test_button.setObjectName(u"test_button")
        self.test_button.setGeometry(QRect(10, 370, 83, 22))
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(10, 40, 811, 291))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 809, 289))
        self.score_view = QGraphicsView(self.scrollAreaWidgetContents)
        self.score_view.setObjectName(u"score_view")
        self.score_view.setGeometry(QRect(-5, -9, 1581, 321))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 835, 19))
        self.menusave = QMenu(self.menubar)
        self.menusave.setObjectName(u"menusave")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menusave.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.test_button.setText(QCoreApplication.translate("MainWindow", u"Button", None))
        self.menusave.setTitle(QCoreApplication.translate("MainWindow", u"save", None))
    # retranslateUi

    def draw_notation(self, events=[], clefs=[Clef.TREBLE]):
        QFontDatabase.addApplicationFont("user/terroir/assets/Bravura.otf")

        # view.show()
        # return view
        scene = QGraphicsScene()
        scene.setSceneRect(0, 0, 200, 200)
        # events=[
        # [50, [60, 10, 10]],
        # [80, [81, 0, 0]],
        # [200, [50, 10, 10]],
        # [300, [[40, 49, 57], 10, 10]]
        # ]
        # clefs=[Clef.TREBLE, Clef.BASS]
        max_onset = 100
        for event in events:
            onset = event[0]
            midicents = event[1][0]
            duration = event[1][1]
            max_onset = max(max_onset, onset)
            if isinstance(midicents, list):
                pass
            else:
                print(midicents)
                notehead = QNotehead()
                notehead.setPos(onset, midicents)
                scene.addWidget(notehead)


        for clef in clefs:
            match clef :
                case Clef.TREBLE:
                    treble = QClef()
                    treble.setPos(0, 70)
                    scene.addWidget(treble)

                    for i in range(5):
                        scene.addLine(QLine(0, 40 + i * 10, max_onset + 200, 40 + i * 10))
                
                case Clef.BASS:
                    bass = QClef()
                    bass.setClef(Clef.BASS)
                    bass.setPos(3, 111)
                    scene.addWidget(bass)
                    
                    for i in range(5):
                        scene.addLine(QLine(0, 100 + i * 10, max_onset + 200, 100 + i * 10))


        self.score_view.setScene(scene)

        pass
