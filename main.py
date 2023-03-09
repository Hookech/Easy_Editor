#создай тут фоторедактор Easy Editor!houijpoj[
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog ,QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout

import os

from PyQt5.QtGui import QPixmap

from PIL import Image, ImageFilter, ImageEnhance

app = QApplication([])
win = QWidget()

win.setWindowTitle('Easy Editor')
win.resize(700, 400)

papka = QPushButton('Папа с файлами')
pic = QLabel('123')

list_widget = QListWidget()

button_left = QPushButton('Лево')
button_right = QPushButton("Право")
button_mirror = QPushButton('Зеркально')
button_rez = QPushButton('Резкость')
button_black = QPushButton('Ч/Б')

line_own = QHBoxLayout()
line_1 = QVBoxLayout()
line_2 = QVBoxLayout()
line_3= QHBoxLayout()

line_1.addWidget(papka, alignment= Qt.AlignLeft)
line_1.addWidget(list_widget, alignment= Qt.AlignLeft)
line_2.addWidget(pic)
line_3.addWidget(button_left)
line_3.addWidget(button_right)
line_3.addWidget(button_mirror)
line_3.addWidget(button_rez)
line_3.addWidget(button_black)

line_own.addLayout(line_1, 20)
line_own.addLayout(line_2, 80)
line_2.addLayout(line_3)

win.setLayout(line_own)

workdir = ""

def filter(files, extensions):
    result = []
    for i in files:
        for y in extensions:
            if i.endswith(y):
                result.append(i)
    return result


def showFilenamelist():
    extensions = ['png','jpg','gif','bmp']
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    filenames = filter(os.listdir(workdir), extensions)
    list_widget.clear()
    for i in filenames:
        list_widget.addItem(i)

class ImageProccesor():
    def __init__(self):
        self.image = None
        self.filename = None
        self.save_dir = 'Mod/'

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        pic.hide()
        pix_map_image = QPixmap(path)
        w,h = pic.width(), pic.height()
        pix_map_image = pix_map_image.scaled(w,h, Qt.KeepAspectRatio)
        pic.setPixmap(pix_map_image)
        pic.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(path)

    def do_rez(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

workimage = ImageProccesor()

def showChoosenImage():
    if list_widget.currentRow() >= 0:
        filename = list_widget.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        workimage.showImage(image_path)

list_widget.currentRowChanged.connect(showChoosenImage)
papka.clicked.connect(showFilenamelist)
button_black.clicked.connect(workimage.do_bw)
button_left.clicked.connect(workimage.do_left)
button_right.clicked.connect(workimage.do_right)
button_mirror.clicked.connect(workimage.do_mirror)
button_rez.clicked.connect(workimage.do_rez)

win.show()
app.exec_()
