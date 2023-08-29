import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsItemGroup, QWidget, QVBoxLayout, QSlider, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap, QTransform
from PyQt5.QtCore import Qt, QObject

def scaleImg(value):
    exp = value * 0.01
    scl = 10.0 ** exp
    qGItemGrp.setTransform(QTransform().scale(scl, scl))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #print("Qt Version:", QT_VERSION_STR)

    qGScene = QGraphicsScene()
    qGItemGrp = QGraphicsItemGroup()
    qImgCat = QImage("cat.jpg")
    qGItemImg = QGraphicsPixmapItem(QPixmap.fromImage(qImgCat).scaledToWidth(600))
    qGItemImg.setTransform(QTransform().translate(-0.5 * qImgCat.width(), -0.5 * qImgCat.height()))
    qGItemGrp.addToGroup(qGItemImg)
    qGScene.addItem(qGItemGrp)

    qWinMain = QWidget()
    qWinMain.setWindowTitle("QGraphicsView - Scale Image")
    qVBox = QVBoxLayout()
    qGView = QGraphicsView()
    qGView.setScene(qGScene)
    qVBox.addWidget(qGView, 1)
    qSlider = QSlider(Qt.Horizontal)
    qSlider.setRange(-100, 100)
    qVBox.addWidget(qSlider)
    qWinMain.setLayout(qVBox)
    qWinMain.show()

    qSlider.valueChanged.connect(scaleImg)

    sys.exit(app.exec_())
