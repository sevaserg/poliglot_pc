import subprocess
import sys
import time
from os import listdir
from os.path import isfile, join

try:
    from pynput.keyboard import Key, Controller
    from PyQt5 import QtCore
    from PyQt5.QtCore import (pyqtSlot, QFile, QTimer)
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit,
                                 QVBoxLayout, QWidget, QComboBox,
                                 QPushButton, QGroupBox, QCheckBox, 
                                 QHBoxLayout, QVBoxLayout, QRadioButton,
                                 QGridLayout, QMenuBar, QScrollArea, QMessageBox)
    from PyQt5.QtGui import QPixmap

except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pynput'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyqt5'])

finally:
    from pynput.keyboard import Key, Controller
    from PyQt5 import QtCore
    from PyQt5.QtCore import (pyqtSlot, QFile, QTimer)
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit,
                                 QVBoxLayout, QWidget, QComboBox,
                                 QPushButton, QGroupBox, QCheckBox, 
                                 QHBoxLayout, QVBoxLayout, QRadioButton,
                                 QGridLayout, QMenuBar, QScrollArea, QMessageBox)
    from PyQt5.QtGui import QPixmap

import random
from datetime import datetime

random.seed()

############################

class Window(QWidget):

    avail = 0
    pts = 0
    hit = 0
    miss = 0
    date = datetime.today().strftime('%Y-%m-%d')
    med = 0
    days = 0
    inputMethod = 0
    voc = ""
    wrd = ""
    lang = ""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.blankpm = QLabel(self)
        self.corrpm = QLabel(self)
        self.failpm = QLabel(self)
        #self.correct.setText("1")
        self.crosspixmap=QPixmap("IMG/cross.png")
        self.tickpixmap=QPixmap("IMG/tick.png")
        self.blankpixmap=QPixmap("IMG/blank.png")
        self.blankpm.setPixmap(QPixmap(self.blankpixmap))
        self.corrpm.setPixmap(QPixmap(self.tickpixmap))
        self.failpm.setPixmap(QPixmap(self.crosspixmap))
        self.blankpm.show()
        self.corrpm.hide()
        self.failpm.hide()
        self.testOptions = QWidget(self)
        self.testOptionsLayout = QGridLayout(self)
        self.testOptions.setLayout(self.testOptionsLayout)
        self.tOps = []
        for i in range (4):
            self.tOps.append(QRadioButton(self))
            self.tOps[i].toggled.connect(self.subm)
            self.testOptionsLayout.addWidget(self.tOps[i], i/2, i%2)
        self.resize(500, 500)
        self.langChoiceLayout=QHBoxLayout(self) 
        self.langChoice = QWidget(self)
        self.langChoice.setLayout(self.langChoiceLayout)
        self.lchoice = []
        info = ["Eng", "Rus", "All"]
        for i in range(3):
            self.lchoice.append(QRadioButton(self))
            self.lchoice[i].setText(info[i])
            self.langChoiceLayout.addWidget(self.lchoice[i])
        self.lchoice[2].setChecked(True)
        self.scroller = QScrollArea(self)
        self.lvbox = QVBoxLayout(self)
        self.rvbox = QVBoxLayout(self)
        self.verticalLeft = QWidget(self)
        self.verticalLeft.setLayout(self.lvbox)
        self.verticalRight = QWidget(self)
        self.verticalRight.setLayout(self.rvbox)
        self.setWindowTitle('QUIZ')
        self.question = QLabel(self)
        self.question.setAlignment(QtCore.Qt.AlignCenter)
        self.question.setText("Выберите категории!")
        self.answer = QLineEdit(self)
        self.submit = QPushButton(self)
        self.submit.setText("Отправить")
        self.submit.clicked.connect(self.subm)
        self.inMeth = QPushButton(self)
        self.inMeth.setText("Метод ввода")
        self.inMeth.clicked.connect(self.changeInput)
        self.stats = QLabel(self)
        self.load()
        self.updateStats()
        self.rvbox.addWidget(self.langChoice)
        self.rvbox.addWidget(self.question)
        self.rvbox.addWidget(self.answer)
        self.rvbox.addWidget(self.testOptions)
        self.rvbox.addWidget(self.submit)
        self.rvbox.addWidget(self.blankpm)
        self.rvbox.addWidget(self.corrpm)
        self.rvbox.addWidget(self.failpm)
        self.rvbox.addWidget(self.stats)
        self.rvbox.addWidget(self.inMeth)
        self.lvbox.setAlignment(Qt.AlignTop)
        self.rvbox.setAlignment(Qt.AlignTop)
        self.question.setMinimumHeight(100)
        i = 0
        self.filescheck = []
        files = self.dirlist()
        self.checkall = QPushButton(self)
        self.checkall.setText("Выделить все")
        self.checkall.clicked.connect(self.chall)
        self.lvbox.addWidget(self.checkall)
        for f in files:
            self.filescheck.append (QCheckBox(f[:-4]))
            self.lvbox.addWidget(self.filescheck[i])
            self.filescheck[i].stateChanged.connect(self.getList)
            i = i + 1
        self.scroller.setWidget(self.verticalLeft)
        self.scroller.setWidgetResizable(True)
        self.scroller.resize(200,500)
        self.verticalLeft.resize(200,500)
        self.verticalRight.resize(300,500)
        self.verticalLeft.move(0,0)
        self.verticalRight.move(200,0)
        self.changeInput()
        self.getList()
        self.show()
        
    def chall(self):
        for chbox in self.filescheck:
            if (self.checkall.text() == "Выделить все"):
                chbox.setChecked(True)
            else:
                chbox.setChecked(False)
        if (self.checkall.text() == "Выделить все"):
            self.checkall.setText("Отменить выделение")
        else:
            self.checkall.setText("Выделить все")

    def dirlist(self):
        files = [f for f in listdir('VOCABULARY')]
        return files

    def keyPressEvent(self, event):
        if (str(event.key())=="16777220"):
            self.subm()

    def randomizeWord(self):
        ret = ""
        try:
            for i in range(0,4):
                self.tOps[i].setChecked(False)
            self.wrd = str(self.voc.split("\n")[random.randint(0, self.voc.count("\n"))])
            if random.randint(0,100) > 50 or self.lchoice[0].isChecked():
                self.lang = "ru"
                temp = str(self.wrd.split("=")[1])
                data = ""
                data += temp.split("/")[random.randint(0, temp.count("/"))]
                self.question.setText(data)
            else:
                if random.randint(0,100) <= 50 or self.lchoice[1].isChecked():
                    self.lang = "en"
                    temp = str(self.wrd.split("=")[0])
                    data = ""
                    data += temp.split("/")[random.randint(0, temp.count("/"))]
                    self.question.setText(data)
            c = 0
            if self.lang == "en":
                c = 1
            for i in range (4):
                self.tOps[i].setText("")
            bwrd = self.wrd.split("=")[c].split("/")
            self.tOps[random.randint(0,3)].setText(bwrd[random.randint(0, len(bwrd)-1)])
            for i in range (4):
                while self.tOps[i].text() == "":
                    temp1 = self.voc.split("\n")[random.randint(0, len(self.voc.split("\n"))-1)].split("=")[c].split("/")
                    randWord = temp1[random.randint(0, len(temp1)-1)]
                    temp1 = 1
                    for j in range (0, 3):
                        if randWord == self.tOps[j].text():
                            temp1 = 0
                    if temp1 == 1:
                        self.tOps[i].setText(randWord)
            ret += data
        except:
            pass
        
        return ret
    
    def readVoc(self, fileName):
        self.avail = 0
        f = open("VOCABULARY/"+str(fileName)+".txt","r")
        data = f.read()
        f.close()
        if len(data.split("\n")) > 2:
            self.voc = self.voc + data
            self.avail = 1
    
    def getList(self):
        self.voc = ""
        k = 0
        for i in range (len(self.filescheck)):
            if self.filescheck[i].isChecked() and list(self.filescheck[i].text())[0] != ".":
                try:
                    self.readVoc(str(self.filescheck[i].text()))
                    if self.avail == 1:
                        self.voc=self.voc+"\n"
                    else:
                        k = k - 1
                except:
                    k = k - 1
                k = k + 1
        if k > 0:
            self.submit.show()
            self.voc = self.voc[:-1]
            while self.randomizeWord() == "":
                pass
        else:
            self.submit.hide()
            self.question.setText("Выберите категории!")
            for i in range (4):
                self.tOps[i].setText("")
    
    def subm(self):
        ans = ""
        if self.inputMethod == 1:
            ans = self.answer.text()
        else:
            for i in range (0, 4):
                if self.tOps[i].isChecked():
                    ans = self.tOps[i].text()
        if ans != "":
            correct = 0
            if self.lang == "en":
                for i in self.wrd.split("=")[1].split("/"):
                    if str(ans.lower()) == str(i).lower():
                        correct = 1
            else:
                for i in self.wrd.split("=")[0].split("/"):
                    if str(ans.lower()) == str(i).lower():
                        correct = 1
            if correct == 1:
                self.hit = self.hit + 1
                self.blankpm.hide()
                self.corrpm.show()
                QTimer.singleShot(500, self.resetSigns)
            else:
                self.miss = self.miss + 1
                self.blankpm.hide()
                self.failpm.show()
                QTimer.singleShot(500, self.resetSigns)
            self.updateStats()
            self.save()
            self.answer.setText("")
        while self.randomizeWord() == "":
            pass
        for i in range (0, 4):
            self.tOps[i].setAutoExclusive(False)
            self.tOps[i].setChecked(False)
            self.tOps[i].setAutoExclusive(True)
    
    def resetSigns(self):
            self.corrpm.hide()
            self.failpm.hide()
            self.blankpm.show()
    
    def updateStats(self):
        self.stats.setText("Очки: " + str(self.points) + "\nВерно: " + str(self.hit) + "\nНеверно: " + str(self.miss) +"\nСредний результат: " + str(self.med/(self.days+1)))
    
    def save(self):
        f = open("results","w+")
        f.write(str(self.days)+"\n"+datetime.today().strftime('%Y-%m-%d')+"\n"+str(self.med)+"\n"+str(self.points)+"\n"+str(self.hit)+"\n"+str(self.miss)+"\n")
        f.close()
    
    def load(self):
        try:
            f = open("results","r")
            temp = f.read()
            self.days = int(temp.split("\n")[0], base=10)
            self.date = temp.split("\n")[1]
            self.med = int(temp.split("\n")[2], base=10)
            self.points = int(temp.split("\n")[3], base=10)
            self.hit = int(temp.split("\n")[4], base=10)
            self.miss = int(temp.split("\n")[5], base=10)
            if datetime.today().strftime('%Y-%m-%d') != self.date:
                self.med = self.med+self.points
                self.points = 0
                self.hit = 0
                self.miss = 0
                self.days = self.days+1
            f.close()
            self.save()
        except:
            f = open("results", "w+")
            temp = "0\n"+datetime.today().strftime('%Y-%m-%d')+"\n0\n0\n0\n0"
            f.write(temp)
            f.close()
            self.load()
    
    def changeInput(self):
        if self.inputMethod == 0:
            self.inputMethod = 1
            self.testOptions.hide()
            self.answer.show()
            self.submit.show()
        else:
            self.inputMethod = 0
            self.testOptions.show()
            self.answer.hide()
            self.submit.hide()

############################

def main():
    
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
