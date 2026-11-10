# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from mmm_terroir import *
import numpy as np

from mmm_terroir.terroir.music_symbols import *
from mmm_terroir.pyside_guis.notes import *
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QEvent, QLocale,
    QMetaObject, QObject, QPoint, QPropertyAnimation, QRect,
    QSize, QTime, QUrl, QVariantAnimation, Qt, QLine)
from PySide6.QtGui import (QAction, QBrush, QCloseEvent, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGraphicsItem, QGraphicsView, QHBoxLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy, QStatusBar, QTextEdit,
    QWidget, QGraphicsScene)

class Ui_MainWindow(object):
    
    roll : Roll
    mmm_audio_instance = None
    data_handling = None
    def setupUi(self, MainWindow):
        self.active_selection = None
        self.default = False
        from mmm_python import Scheduler
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"Roll View")
        MainWindow.resize(800, 459)
        
        MainWindow.destroyed.connect(self.closeEvent)
        
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.score_view = QGraphicsView(self.centralwidget)
        self.score_view.setObjectName(u"score_view")
        self.score_view.setGeometry(QRect(-5, 51, 811, 301))
        
        self.play_button = QPushButton(self.centralwidget)
        self.play_button.setObjectName(u"play_button")
        self.play_button.setGeometry(QRect(10, 370, 83, 22))
        self.play_button.clicked.connect(self.play)
        
        self.stop_button = QPushButton(self.centralwidget)
        self.stop_button.setObjectName(u"stop_button")
        self.stop_button.setGeometry(QRect(80, 370, 83, 22))
        self.stop_button.clicked.connect(self.stop)
        
        self.pause_button = QPushButton(self.centralwidget)
        self.pause_button.setObjectName(u"pause_button")
        self.pause_button.setGeometry(QRect(150, 370, 83, 22))
        self.pause_button.clicked.connect(self.pause)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 19))
        self.menusave = QMenu(self.menubar)
        self.menusave.setObjectName(u"menusave")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menusave.menuAction())


        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(430, 370, 351, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.midicent_text = QLineEdit(self.horizontalLayoutWidget)
        self.midicent_text.setObjectName(u"midicent_text")
        self.midicent_text.editingFinished.connect(self.on_midicent_change)
        self.midicent_text.setText("midicent_text")
        self.horizontalLayout.addWidget(self.midicent_text)

        self.duration_text = QLineEdit(self.horizontalLayoutWidget)
        self.duration_text.setObjectName(u"duration_text")
        self.duration_text.setText("duration_text")
        self.duration_text.editingFinished.connect(self.on_duration_change)

        self.horizontalLayout.addWidget(self.duration_text)

        self.velocity_text = QLineEdit(self.horizontalLayoutWidget)
        self.velocity_text.setObjectName(u"textEdit")
        self.velocity_text.editingFinished.connect(self.on_velocity_change)
        self.horizontalLayout.addWidget(self.velocity_text)


        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        self.scheduler = Scheduler()
        QFontDatabase.addApplicationFont("user/terroir/assets/Bravura.otf")
        self.ledger_pen = QPen()
        self.ledger_pen.setWidth(2)
        self.ledger_pen.setStyle(Qt.PenStyle.SolidLine)
        self.ledger_pen.setColor("black")
        
        self.dur_pen = QPen()
        self.dur_pen.setWidth(4)
        self.dur_pen.setStyle(Qt.PenStyle.SolidLine)
        self.dur_pen.setColor(QColor(0,0,0,50))
        
        
        self.playhead_pen = QPen()
        self.playhead_pen.setWidth(2)
        self.playhead_pen.setStyle(Qt.PenStyle.SolidLine)
        self.playhead_pen.setColor("red")
        
        
        self.noteheads = []
        
        self.anim = QVariantAnimation()
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Roll View", None))
        self.play_button.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.pause_button.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.menusave.setTitle(QCoreApplication.translate("MainWindow", u"save", None))
    # retranslateUi
    
    def closeEvent(self, event: QCloseEvent):
        if self.default:
            print("turning audio off")
            self.mmm_audio_instance.stop_process()
        pass
    
    def draw_notation(self, events=[], clefs=[Clef.TREBLE]):
        QFontDatabase.addApplicationFont("user/terroir/assets/Bravura.otf")
        padding_l = 20
        padding_t = 20
        padding_b = 20
        self.events = events
        self.events.sort()
        self.ledgers = []
        self.max_time = (self.events[len(self.events) - 1][0] + self.events[len(self.events) - 1][1][1][0]) * 1000
        self.scene = QGraphicsScene()
        self.clefs = clefs
        
        max_onset = 100 + padding_l
        bot_y = 0
        top_y = 0
        for event_ind, event in enumerate(events):
            onset = event[0] * 100 + padding_l + 50
            midicents = event[1][0]
            duration = event[1][1]
            max_onset = max(max_onset, onset)
            
            if isinstance(midicents, list):
                
                for i, midicent in enumerate(midicents):
                    notehead = QNotehead(self.dur_pen)
                    self.scene.addWidget(notehead)
                    notehead.parent_roll = self
                    notehead.event_index = event_ind
                    notehead.sub_index = i
                    notehead.formatNote(onset, midicent)
                    notehead.duration = duration[i]
                    notehead.draw_duration()
                    notehead.draw_accidental()
                    
                    
                   
                    self.noteheads.append(notehead)
                    
                    self.drawLedgers(onset, midicents)
                    top_y = min(top_y, notehead.pos().y() - padding_t)
                    bot_y = max(bot_y, notehead.pos().y() + padding_b)
                    
                    # self.scene.addLine(notehead.pos().x() + 5, notehead.pos().y() + 8, notehead.pos().x() + (duration[i] * 100), notehead.pos().y() + 8, self.dur_pen)
                    
            else:
                
                notehead = QNotehead(self.dur_pen)
                notehead.formatNote(onset, midicents)
                self.scene.addWidget(notehead)
                notehead.parent_roll = self
                notehead.event_index = event_ind
                notehead.sub_index = 0
                if notehead.accidental != Accidental.NATURAL:
                    
                    acc = self.scene.addText(notehead.accidental, QFont("Bravura", 32))
                    acc.setPos(onset - 19, notehead.pos().y() - 83)
                self.drawLedgers(onset, midicents)
                top_y = min(top_y, notehead.pos().y() - padding_t)
                bot_y = max(bot_y, notehead.pos().y() + padding_b)
                self.noteheads.append(notehead)
                
        print(len(self.noteheads))
        max_height = 0
        for clef in clefs:
            match clef :
                case Clef.TREBLE:
                    treble = QClef()
                    treble.setPos(0 + padding_l, 70)
                    self.scene.addWidget(treble)

                    for i in range(5):
                        self.scene.addLine(QLine(padding_l - 5, 40 + i * 10, max_onset + 200, 40 + i * 10))
                        top_y = min(top_y,  40 + i * 10 + padding_t)
                        bot_y = max(bot_y,  40 + i * 10 + padding_b)
                
                case Clef.BASS:
                    bass = QClef()
                    bass.setClef(Clef.BASS)
                    bass.setPos(3 + padding_l, 111)
                    self.scene.addWidget(bass)
                    
                    for i in range(5):
                        self.scene.addLine(QLine(padding_l - 5, 100 + i * 10, max_onset + 200, 100 + i * 10))
                        top_y = min(top_y,  100 + i * 10 - padding_t)
                        bot_y = max(bot_y,  100 + i * 10 + padding_b)
                
                case Clef.TREBLE_8VA:
                    treble = QClef()
                    treble.setClef(Clef.TREBLE)
                    treble.setPos(3 + padding_l, 0)
                    self.scene.addWidget(treble)
                    
                    for i in range(5):
                        self.scene.addLine(QLine(padding_l - 5, -30 + i * 10, max_onset + 200, -30 + i * 10))
                        top_y = min(top_y,  -30 + i * 10 - padding_t)
                        bot_y = max(bot_y,  -30 + i * 10 + padding_b)
                
                case Clef.BASS_8VB:
                    bass = QClef()
                    bass.setClef(Clef.BASS)
                    bass.setPos(3 + padding_l, 181)
                    self.scene.addWidget(bass)
                    
                    for i in range(5):
                        self.scene.addLine(QLine(padding_l - 5, 170 + i * 10, max_onset + 200, 170 + i * 10))
                        top_y = min(top_y,  170 + i * 10 - padding_t)
                        bot_y = max(bot_y,  170 + i * 10 + padding_b)
                        
        for item in self.scene.items():
            item.moveBy(0, abs(top_y))
        
        for notehead in self.noteheads:
            notehead.y_offset = abs(top_y)
        self.scene.setSceneRect(0, 0, max_onset + 300, bot_y + abs(top_y) + padding_b * 2)
        self.max_time = self.events[len(self.events) -1][0] + self.events[len(self.events) -1][1][1][0]
        
        self.score_view.setScene(self.scene)
        
        
        pass

    def redraw_ledgers(self):
        self.ledgers = []
        for event in self.roll.events:
            self.drawLedgers(event[0], event[1][0])
        
        self.scene.update()
   
    def drawLedgers(self, onset, midicents):
        notes = []
        if isinstance(midicents, list):
            notes.append(min(midicents))
            notes.append(max(midicents))
        else:
            notes.append(midicents)
        
        
        for note in notes:
            
            ledgers = place_ledgers(onset, note, self.clefs)
            for ledger in ledgers:
                self.ledgers.append(self.scene.addLine(ledger[0] - 2, 91 - ledger[1], ledger[0] + 15, 91 - ledger[1], self.ledger_pen))
            pass
    
    def on_midicent_change(self):
        print("midi")
        if self.active_selection:
            self.roll.events[self.active_selection.event_index][1][0][self.active_selection.sub_index] = float(self.midicent_text.text())
            
            self.draw_notation(self.roll.events, self.clefs)
            self.draw_playhead()
        pass
    
    def on_duration_change(self):
        print("dur")
        if self.active_selection:
            self.roll.events[self.active_selection.event_index][1][1][self.active_selection.sub_index] = float(self.duration_text.text())
            
            self.draw_notation(self.roll.events, self.clefs)
            self.draw_playhead()
        pass
    
    def on_velocity_change(self):
        print("vol")
        if self.active_selection:
            self.roll.events[self.active_selection.event_index][1][2][self.active_selection.sub_index] = float(self.velocity_text.text())
            
            self.draw_notation(self.roll.events, self.clefs)
            self.draw_playhead()
        pass
    
    def draw_playhead(self):
        
        self.playhead = self.scene.addLine(0, 0, 0, 200, self.playhead_pen)
        self.playhead.setPos(76, 0)
        self.playhead_start = self.playhead.pos().x()
        self.playhead.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        pass
    
    def redraw_notehead(self, index):
        notehead = self.noteheads[index]
        notehead.redraw()
        pass
    
    def play(self):
        
        start = (self.playhead.pos().x() - 76)
        
        
        self.anim = QVariantAnimation()
        def update_line(value: float):
            self.playhead.setPos(value, 0)
            self.score_view.horizontalScrollBar().setValue(int(np.interp(self.playhead.pos().x(), [76, self.max_time * 100], [self.score_view.horizontalScrollBar().minimum(), self.score_view.horizontalScrollBar().maximum()])))
            pass
        
       
        self.anim.setDuration(((self.max_time)- ((self.playhead.pos().x()-76)/100)) * 1000)  # 1 second
        
       
        self.anim.setStartValue(float(self.playhead.pos().x()))
        
        self.anim.setEndValue(float(76 + self.max_time * 100))  # Moves and changes size
        
        
        
        self.anim.valueChanged.connect(update_line)
        
        
        # 5. Start the animation
        self.anim.start()
        # print(self.anim.valueChanged.emit(10.0))
       
        self.roll.play(self.scheduler, self.mmm_audio_instance, start=start, data_handling=self.data_handling)
        
        
        pass
    
    def pause(self):
        self.anim.stop()
        self.scheduler.stop_thread()
    
    def stop(self):
        self.playhead.setPos(76, 0)
        self.scheduler.stop_thread()
        self.anim.stop()
        self.score_view.horizontalScrollBar().setValue(0)
        


class KeyFilter(QScrollArea):
    def eventFilter(self, watched, event):
        # Check if a key was pressed
        if event.type() == QEvent.Type.KeyPress:
            # Catch arrow keys
            if event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_Left, Qt.Key.Key_Right):
                # Ignore the event so it doesn't scroll, or pass it to the parent
                event.ignore()
                return True # Tells Qt we handled this event
        
        # Pass all other events to the standard handler
        return super().eventFilter(watched, event)