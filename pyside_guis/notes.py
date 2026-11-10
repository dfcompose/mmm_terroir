from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Property, Qt, Signal, QPoint, QMargins
from PySide6.QtGui import QFont, QMouseEvent, QPainter, QPen, QColor, QPainterPath, QPixmap, QBrush
from user.mmm_terroir.terroir.music_symbols import *
from user.mmm_terroir.terroir.graphics_helpers import *
from math import modf

    

class QNotehead(QtWidgets.QWidget):
    pitch = 60
    accidental = Accidental.SHARP
    notehead = Notehead.FILLED
    
    parent_roll : object
    def __init__(self, pen, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.y_offset = 0
        self.duration = 1.0
        self.setFixedSize(20, 20)
        self.event_index = 0
        self.sub_index = 0
        self.brush = QBrush()
        self.brush.setColor(QColor("black"))
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)
        self.acc = None
        self.pen = QPen()
        self.pen.setColor(QColor("black"))       # Line color
        self.pen.setWidth(2)                   # Line thickness in pixels
        self.pen.setStyle(Qt.PenStyle.SolidLine)
        
        self.dur_pen = pen
        
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    
    pass

   
    def formatNote(self, onset, midicent):
        cents, pitch = modf(midicent)
        octave = divmod(midicent, 12)[0]
        
        line, accidental = get_pitch_class(pitch, cents)
        octave_displacement = (octave - 5) * 3.5
        line = line + octave_displacement
       
        self.accidental = accidental
        self.setPos(onset, 90 - (line * 10) + self.y_offset)
        
        
        pass


    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            
            self.selected = True
            
            # self.pen.setColor("blue")
            # self.brush.setColor("blue")
            # self.update()
            # self.setStyleSheet("color: light-blue;")
            event.accept()
            self.parent_roll.active_selection = self
            print( self.parent_roll.active_selection, self)
            roll_event = self.parent_roll.roll.events[self.event_index]
            self.parent_roll.midicent_text.setText(str(roll_event[1][0][self.sub_index]))
            self.parent_roll.duration_text.setText(str(roll_event[1][1][self.sub_index]))
            self.parent_roll.velocity_text.setText(str(roll_event[1][2][self.sub_index]))
            #self.parent_roll.roll.events[self.event_indices[0]][0], self.parent_roll.roll.events[self.event_indices[0]][1])
        else:
            super().mousePressEvent(event)
    
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        print(self.parent_roll.active_selection)
        if  self.parent_roll.active_selection == self:
            
            if event.key() == Qt.Key.Key_Up:
                    roll = self.parent_roll.roll
                    roll.events[self.event_index][1][0][self.sub_index] += 1.0
                    print(roll.events[self.event_index][1][0][self.sub_index])
                    self.formatNote(roll.events[self.event_index][0] * 100 + 20 + 50, roll.events[self.event_index][1][0][self.sub_index])
                    # self.update()
                    # self.parent_roll.redraw_ledgers()
                    self.draw_accidental()
                    self.redraw_duration()
            elif event.key() == Qt.Key.Key_Down:
                    roll = self.parent_roll.roll
                    roll.events[self.event_index][1][0][self.sub_index] -= 1.0
                    self.formatNote(roll.events[self.event_index][0] * 100 + 20 + 50, roll.events[self.event_index][1][0][self.sub_index])
                    # self.update()
                    self.draw_accidental()
                    # self.parent_roll.redraw_ledgers()
                    self.redraw_duration()
            if event.key() == Qt.Key.Key_Left:
                    roll = self.parent_roll.roll
                    roll.events[self.event_index][0] -= 0.1
                    print(roll.events[self.event_index][1][0][self.sub_index])
                    self.formatNote(roll.events[self.event_index][0] * 100 + 20 + 50, roll.events[self.event_index][1][0][self.sub_index])
                    # self.update()
                    self.draw_accidental()
                    # self.parent_roll.redraw_ledgers()
                    self.redraw_duration()
            elif event.key() == Qt.Key.Key_Right:
                    roll = self.parent_roll.roll
                    roll.events[self.event_index][0] += 0.1
                    self.formatNote(roll.events[self.event_index][0] * 100 + 20 + 50, roll.events[self.event_index][1][0][self.sub_index])
                    # self.update()
                    self.draw_accidental()
                    # self.parent_roll.redraw_ledgers()
                    self.redraw_duration()
        return super().keyPressEvent(event)
    
    def setPos(self, x, y):
        self.move(x - 1, y - 7)
        pass
    
    def draw_accidental(self):
        
        if not self.acc and self.accidental != Accidental.NATURAL:
            self.acc = self.parent_roll.scene.addText(self.accidental, QFont("Bravura", 32))
            self.acc.setPos(self.pos().x() - 19, self.pos().y() - 83)
        elif self.accidental != Accidental.NATURAL:
            self.acc.setPlainText(self.accidental)
            self.acc.setPos(self.pos().x() - 19, self.pos().y() - 83)
        elif self.acc:
            self.acc.setPlainText("")
            self.acc.setPos(self.pos().x() - 19, self.pos().y() - 83)
    def draw_duration(self):
        self.dur_line = self.parent_roll.scene.addLine(self.pos().x() + 5, self.pos().y() + 8, self.pos().x() + (self.duration * 100), self.pos().y() + 8, self.dur_pen)
        pass
  
    def redraw_duration(self):
            self.dur_line.setLine(self.pos().x() + 5, self.pos().y() - self.y_offset + 8, self.pos().x() + (self.duration * 100), self.pos().y() - self.y_offset + 8)
            pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        
        
        
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        
        path = QPainterPath()
        path.addText(1, 8, QFont("Bravura", 32), Notehead.FILLED)
        path.closeSubpath()
        path.setFillRule(Qt.FillRule.WindingFill)
        
        painter.fillPath(path, self.brush)
        
        
        
        pass


class QClef(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.clef = Clef.TREBLE
    
    def setClef(self, clef=Clef.TREBLE):
        self.clef = clef
    
    def setPos(self, x, y):
            self.move(x - 1, y - 50)
            pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # pixmap = QPixmap(400, 300)
        # pixmap.fill(QColor(0,0,0,0))
        
        brush = QBrush()
        brush.setColor(QColor("black"))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        # 2. (Optional) Configure the pen to change color, width, and style
        pen = QPen()
        pen.setColor(QColor("black"))       # Line color
        pen.setWidth(2)                   # Line thickness in pixels
        pen.setStyle(Qt.PenStyle.SolidLine) # Style (e.g., SolidLine, DashLine)
        painter.setPen(pen)
        painter.setBrush(brush)
        
        path = QPainterPath()
        path.addText(1, 50, QFont("Bravura", 32), self.clef)
        path.closeSubpath()
        path.setFillRule(Qt.FillRule.WindingFill)
        # painter.drawPath(path)
        painter.fillPath(path, brush)


class QStaff(QtWidgets.QWidget):
    
    def __init__(self, container,  x, y, clef=[Clef.TREBLE],  *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.clef = clef
        self.clef.sort()
        
        self.position = [x, y]

        for clef in self.clef:
            match clef:
                case Clef.TREBLE:
                    clef_to_draw = QLabel(Clef.TREBLE, self)
                    clef_to_draw.setFont(QFont('Bravura', 32))
                    clef_to_draw.move(QPoint(self.position[0], self.position[1] - 58))
                case Clef.BASS:
                    clef_to_draw = QLabel(Clef.BASS, self)
                    clef_to_draw.setFont(QFont('Bravura', 32))
                    clef_to_draw.move(QPoint(self.position[0], self.position[1] - 17))
                case Clef.TREBLE_8VA:
                    font = QFont('Bravura', 32)
                    treble = QLabel(Clef.TREBLE, self)
                    treble.setFont(font)
                    treble.move(QPoint(self.position[0], self.position[1] - 128))
                case Clef.BASS_8VB:
                    bass = QLabel(Clef.BASS, self)
                    bass.setFont(font)
                    bass.move(QPoint(self.position[0], self.position[1] + 53))

    def setPos(self, x, y):
            self.move(x - 1, y - 7)
            pass
    def paintEvent(self, event):
        # 1. Initialize the painter object to draw directly on this widget
        painter = QPainter(self)
        
        # 2. (Optional) Configure the pen to change color, width, and style
        pen = QPen()
        pen.setColor(QColor("black"))       # Line color
        pen.setWidth(2)                   # Line thickness in pixels
        pen.setStyle(Qt.PenStyle.SolidLine) # Style (e.g., SolidLine, DashLine)
        painter.setPen(pen)
        
        # 3. Draw the line using one of the method signatures
        # Signature: drawLine(x1, y1, x2, y2)


        for clef in self.clef:
            match clef:
                case Clef.TREBLE:
                    for i in range(5):
                        painter.drawLine(self.position[0], i * 10 + self.position[1], self.position[0] + 800, i * 10 + self.position[1])
                case Clef.BASS:
                    for i in range(5):
                        painter.drawLine(self.position[0], i * 10 + self.position[1] + 60, self.position[0] + 800, i * 10 + self.position[1] + 60)
                case Clef.TREBLE_8VA:
                    for i in range(5):
                        painter.drawLine(self.position[0], i * 10 + self.position[1] - 70, self.position[0] + 800, i * 10 + self.position[1] - 70)
                case Clef.BASS_8VB:
                    for i in range(5):
                        painter.drawLine(self.position[0], i * 10 + self.position[1] + 130, self.position[0] + 800, i * 10 + self.position[1] + 130)
                    pass
                

