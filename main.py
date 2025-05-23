#создай тут фоторедактор Easy Editor!

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget, QListWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog
import os
from PIL import Image, ImageOps, ImageFilter
from PyQt5.QtGui import QPixmap

workdir = ""


class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.image = None
        self.dir = None
        self.save_dir = 'Modified/'
    
    def LoadImage(self, filename):
        self.filename = filename
        self.dir = workdir
        image_path = os.path.join(self.dir,self.filename)
        self.image = Image.open(image_path)

    def ShowImage(self, path):
        pixmapimage = QPixmap(path) 
        label_width, label_height = ImageLable.width(), ImageLable.height() 
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio) 
        ImageLable.setPixmap(scaled_pixmap) 
        ImageLable.setVisible(True)

    def SaveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def makeGray(self):
        self.image = ImageOps.grayscale(self.image)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

    def makeSharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)
    
    def makeMirror(self):
        self.image = ImageOps.mirror(self.image)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

    def makeFlip(self):
        self.image = ImageOps.flip(self.image)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

    def makeLeft(self):
        self.image = self.image.rotate(90)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

    def makeRight(self):
        self.image = self.image.rotate(-90)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)
    
    def makeBlur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur(0.5))
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

    def makeFindEdges(self):
        self.image = self.image.filter(ImageFilter.FIND_EDGES)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

    def makeContour(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.SaveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.ShowImage(image_path)

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
                break
    return result


def ShowFilenamesList():
    chooseWorkdir()
    extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.jfif']
    files = os.listdir(workdir)
    files = filter(files,extensions)
    ImagesList.clear()
    ImagesList.addItems(files)

workImage = ImageProcessor()

def showChosenImage():
    if ImagesList.currentRow() >= 0:
        filename = ImagesList.currentItem().text()
        workImage.LoadImage(filename)
        image_path = os.path.join(workdir,filename)
        workImage.ShowImage(image_path)


app = QApplication([])

mainWin = QWidget()
mainWin.resize(1000,500)
mainWin.setWindowTitle('Easy Editor')


# Widgets
ImagesList = QListWidget()
ImageLable = QLabel()
FolderButton = QPushButton('Folder')
LeftButton = QPushButton('Left')
RightButton = QPushButton('Right')
MirrorButton = QPushButton('Mirror')
FlipButton = QPushButton('Flip')
SharpButton = QPushButton('Sharp')
BlurButton = QPushButton('Blur')
GrayButton = QPushButton('Black/White')
FindEdgesButton = QPushButton('FindEdges')
ContourButton = QPushButton('Contour')


HLine0 = QHBoxLayout()
HLine1 = QHBoxLayout()
VLine0 = QVBoxLayout()
VLine1 = QVBoxLayout()


HLine1.addWidget(LeftButton)
HLine1.addWidget(RightButton)
HLine1.addWidget(FlipButton)
HLine1.addWidget(MirrorButton)
HLine1.addWidget(SharpButton)
HLine1.addWidget(BlurButton)
HLine1.addWidget(GrayButton)
HLine1.addWidget(FindEdgesButton)
HLine1.addWidget(ContourButton)
VLine0.addWidget(FolderButton)
VLine0.addWidget(ImagesList)
VLine1.addWidget(ImageLable)

VLine1.addLayout(HLine1)
HLine0.addLayout(VLine0)
HLine0.addLayout(VLine1)

mainWin.setLayout(HLine0)



FolderButton.clicked.connect(ShowFilenamesList)
ImagesList.currentRowChanged.connect(showChosenImage)
GrayButton.clicked.connect(workImage.makeGray)
SharpButton.clicked.connect(workImage.makeSharpen)
BlurButton.clicked.connect(workImage.makeBlur)
MirrorButton.clicked.connect(workImage.makeMirror)
FlipButton.clicked.connect(workImage.makeFlip)
LeftButton.clicked.connect(workImage.makeLeft)
RightButton.clicked.connect(workImage.makeRight)
FindEdgesButton.clicked.connect(workImage.makeFindEdges)
ContourButton.clicked.connect(workImage.makeContour)


mainWin.show()
app.exec_()