import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QPushButton, QSlider, QDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageFilter
import sqlite3


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 1350, 690)
        self.setWindowTitle('editor')
        self.flg = False
        self.exit_flg = False

        #объявление иконок верхнего меню
        saveAction = QAction(QIcon('save.png'), 'Save image\n(Ctrl+E)', self)
        saveAction.setShortcut('Ctrl+E')
        saveAction.triggered.connect(self.save)

        openAction = QAction(QIcon('open.png'), 'Open image\n(Ctrl+Q)', self)
        openAction.setShortcut('Ctrl+Q')
        openAction.triggered.connect(self.open)

        cancelAction = QAction(QIcon('cancel.png'), 'Cancel\n(Ctrl+Z)', self)
        cancelAction.setShortcut('Ctrl+Z')
        cancelAction.triggered.connect(self.cancel)

        exitAction = QAction(QIcon('exit24.png'), 'Exit\n(Ctrl+A)', self)
        exitAction.setShortcut('Ctrl+A')
        exitAction.triggered.connect(self.exit)

        self.opentool = self.addToolBar('Open image\n(Ctrl+Q)')
        self.opentool.addAction(openAction)
        self.opentool.addAction(cancelAction)
        self.opentool.addAction(exitAction)
        self.opentool.addAction(saveAction)

        self.pixmap = QPixmap('noname')
        self.image = QLabel(self)
        self.image.move(60, 60)
        self.image.resize(0, 0)
        self.image.setPixmap(self.pixmap)

        self.bright_label = QLabel('Яркость', self)
        self.contrast_label = QLabel('Контрастность', self)
        self.degradation_label = QLabel('Размытие', self)
        self.anagliph_label = QLabel('Анаглиф', self)
        self.min_label = QLabel('Масло', self)

        self.negative_button = QPushButton('Негатив', self)
        self.left_button = QPushButton('Повернуть направо', self)
        self.right_button = QPushButton('Повернуть налево', self)
        self.apply_button = QPushButton('Применить', self)
        self.bw_button = QPushButton('Черно-белый', self)
        self.r_button = QPushButton('R', self)
        self.g_button = QPushButton('G', self)
        self.b_button = QPushButton('B', self)
        self.f_1_button = QPushButton('Filter 1', self)
        self.f_2_button = QPushButton('Filter 2', self)

        #объявление ресурсов взаимодействия с пользователем
        self.negative_button.clicked.connect(self.negative)
        self.left_button.clicked.connect(self.left)
        self.right_button.clicked.connect(self.right)
        self.apply_button.clicked.connect(self.apply)
        self.bw_button.clicked.connect(self.bw)
        self.r_button.clicked.connect(self.r)
        self.g_button.clicked.connect(self.g)
        self.b_button.clicked.connect(self.b)
        self.f_1_button.clicked.connect(self.f_1)
        self.f_2_button.clicked.connect(self.f_2)

        self.bright_label.move(10000, 10000)
        self.contrast_label.move(10000, 10000)
        self.degradation_label.move(10000, 10000)
        self.anagliph_label.move(10000, 10000)
        self.min_label.move(10000, 10000)

        self.negative_button.move(10000, 10000)
        self.left_button.move(10000, 10000)
        self.right_button.move(10000, 10000)
        self.apply_button.move(10000, 10000)
        self.bw_button.move(10000, 10000)
        self.r_button.move(10000, 10000)
        self.g_button.move(10000, 10000)
        self.b_button.move(10000, 10000)
        self.f_1_button.move(10000, 10000)
        self.f_2_button.move(10000, 10000)

        self.sld_bright = QSlider(Qt.Horizontal, self)
        self.sld_contrast = QSlider(Qt.Horizontal, self)
        self.sld_degradation = QSlider(Qt.Horizontal, self)
        self.sld_anagliph = QSlider(Qt.Horizontal, self)
        self.sld_min = QSlider(Qt.Horizontal, self)

        self.sld_bright.setValue(0)
        self.sld_bright.setTickInterval(1)
        self.sld_bright.setRange(-10, 10)
        self.sld_bright.setFocusPolicy(Qt.StrongFocus)
        self.sld_bright.setTickPosition(QSlider.TicksBothSides)
        self.sld_bright.setSingleStep(1)
        self.sld_bright.move(10000, 10000)

        self.sld_min.setValue(-1)
        self.sld_min.setTickInterval(2)
        self.sld_min.setRange(-1, 10)
        self.sld_min.setFocusPolicy(Qt.StrongFocus)
        self.sld_min.setTickPosition(QSlider.TicksBothSides)
        self.sld_min.setSingleStep(1)
        self.sld_min.move(10000, 10000)

        self.sld_contrast.setValue(0)
        self.sld_contrast.setTickInterval(1)
        self.sld_contrast.setRange(-10, 10)
        self.sld_contrast.setFocusPolicy(Qt.StrongFocus)
        self.sld_contrast.setTickPosition(QSlider.TicksBothSides)
        self.sld_contrast.setSingleStep(1)
        self.sld_contrast.move(10000, 10000)

        self.sld_degradation.setValue(0)
        self.sld_degradation.setTickInterval(1)
        self.sld_degradation.setRange(0, 10)
        self.sld_degradation.setFocusPolicy(Qt.StrongFocus)
        self.sld_degradation.setTickPosition(QSlider.TicksBothSides)
        self.sld_degradation.setSingleStep(1)
        self.sld_degradation.move(10000, 10000)

        self.sld_anagliph.setValue(0)
        self.sld_anagliph.setTickInterval(1)
        self.sld_anagliph.setRange(0, 10)
        self.sld_anagliph.setFocusPolicy(Qt.StrongFocus)
        self.sld_anagliph.setTickPosition(QSlider.TicksBothSides)
        self.sld_anagliph.setSingleStep(1)
        self.sld_anagliph.move(10000, 10000)

        self.sld_bright.valueChanged.connect(self.ok_bright_func)
        self.sld_contrast.valueChanged.connect(self.ok_contrast_func)
        self.sld_degradation.valueChanged.connect(self.ok_degradation_func)
        self.sld_anagliph.valueChanged.connect(self.ok_anagliph_func)
        self.sld_min.valueChanged.connect(self.ok_min_func)

        self.ok_bright = QPushButton('OK', self)
        self.ok_bright.move(10000, 10000)
        self.ok_bright.clicked.connect(self.bright)

        self.ok_contrast = QPushButton('OK', self)
        self.ok_contrast.move(10000, 10000)
        self.ok_contrast.clicked.connect(self.contrast)

        self.ok_anagliph = QPushButton('OK', self)
        self.ok_anagliph.move(10000, 10000)
        self.ok_anagliph.clicked.connect(self.anagliph)

        self.ok_degradation = QPushButton('OK', self)
        self.ok_degradation.move(10000, 10000)
        self.ok_degradation.clicked.connect(self.degradation)

        self.ok_min = QPushButton('OK', self)
        self.ok_min.move(10000, 10000)
        self.ok_min.clicked.connect(self.min)

    #функция открытия
    def open(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        self.last_value_bright = 0
        self.last_value_contrast = 0
        self.last_value_anagliph = 0
        self.last_value_degradation = 0
        self.sld_anagliph.setValue(0)
        self.sld_degradation.setValue(0)
        self.sld_contrast.setValue(0)
        self.sld_bright.setValue(0)
        self.sld_min.setValue(0)
        self.idkhowtonamethis = False

        if self.fname:
            self.save_flag = False
            self.im = Image.open(self.fname)
            self.pixels = self.im.load()
            self.flg = True
            self.format = self.fname[-4:]
            self.dataname = 'data{}'.format(self.format)
            self.oldim = self.im
            self.x, self.y = self.im.size
            self.one_more_flg = False

            self.pixmap = QPixmap(self.fname)

            self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
            self.image.resize(600, 542)
            self.image.setPixmap(self.smaller_pixmap)

            self.bright_label.move(800, 100)
            self.contrast_label.move(800, 200)
            self.degradation_label.move(800, 300)
            self.anagliph_label.move(800, 400)
            self.min_label.move(800, 500)

            self.negative_button.move(1100, 200)
            self.left_button.move(1100, 100)
            self.right_button.move(1100, 150)
            self.bw_button.move(1100, 250)

            self.r_button.move(1100, 300)
            self.g_button.move(1100, 350)
            self.b_button.move(1100, 400)
            self.f_1_button.move(1100, 450)
            self.f_2_button.move(1100, 500)

            self.sld_bright.move(800, 150)
            self.sld_contrast.move(800, 250)
            self.sld_degradation.move(800, 350)
            self.sld_anagliph.move(800, 450)
            self.sld_min.move(800, 550)

            self.ok_bright.move(910, 150)
            self.ok_contrast.move(910, 250)
            self.ok_anagliph.move(910, 450)
            self.ok_degradation.move(910, 350)
            self.ok_min.move(910, 550)

            self.medbr = 0

            for i in range(self.x):
                for j in range(self.y):
                    w = list(self.pixels[i, j])
                    self.medbr += (w[0] * 0.299 + w[1] * 0.587 + w[2] * 0.114)
            self.medbr /= (self.x * self.y)

    #функция выхода
    def exit(self):
        if self.save_flag:
            qApp.quit()
        if self.exit_flg:

            self.save_quest = QDialog()
            self.save_quest.setGeometry(100, 100, 200, 110)

            yes_button = QPushButton('да', self.save_quest)
            yes_button.move(20, 50)
            yes_button.clicked.connect(self.save)

            no_button = QPushButton('нет', self.save_quest)
            no_button.clicked.connect(qApp.quit)
            no_button.move(100, 50)

            self.save_quest.setWindowTitle('Сохранить?')
            self.save_quest.exec_()
        else:
            qApp.quit()

    #функция сохранения фотографии
    def save(self):
        if not self.flg:
            pass
        else:
            fname, okBtnPressed = QInputDialog.getText(self, "Введите название файла",
                                                       "Название")
            fname = fname + self.fname[-4:]
            self.save_flag = True
            if okBtnPressed:
                self.im.save(fname)

    #применение изменений
    def apply(self):
        self.oldim = self.im
        self.im = self.newim
        self.apply_button.move(10000, 10000)
        self.exit_flg = True

    #отмена
    def cancel(self):
        if self.flg:
            self.im = self.oldim
            self.newim = self.oldim
            self.newim.save(self.dataname)
            self.pixmap = QPixmap(self.dataname)
            self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
            self.image.setPixmap(self.smaller_pixmap)
        else:
            pass

    def ok_bright_func(self, value):  #функции возвращающие значения слайдеров 
        self.value_bright = value

    def ok_contrast_func(self, value):
        self.value_contrast = value

    def ok_anagliph_func(self, value):
        self.value_anagliph = value

    def ok_degradation_func(self, value):
        self.value_degradation = value

    def ok_min_func(self, value):
        self.value_min = value

    def bright(self, z):
        self.newim = self.im.copy()
        pixels = self.newim.load()

        if self.idkhowtonamethis:
            asd = z
        else:
            asd = self.value_bright
        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                w[0] += asd * 10
                w[1] += asd * 10
                w[2] += asd * 10
                pixels[i, j] = tuple(w)

        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply_button.move(910, 600)
        self.idkhowtonamethis = False

    def contrast(self, z):
        self.newim = self.im.copy()
        pixels = self.newim.load()
        palitra = list()
        if self.idkhowtonamethis:
            zxc = z
        else:
            zxc = self.value_contrast
        if zxc == 0:
            self.newim.save(self.dataname)
            self.pixmap = QPixmap(self.dataname)
            self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
            self.image.setPixmap(self.smaller_pixmap)
            pass
        for i in range(0, 256):
            delta = i - self.medbr
            if zxc > 0:
                temp = (self.medbr + zxc * delta)
            else:
                temp = (self.medbr + ((11 - abs(zxc)) / 10) * delta)
            if temp < 0:
                temp = 0
            elif temp >= 255:
                temp = 255
            palitra.append(temp)
        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                w[0] = int(palitra[w[0]])
                w[1] = int(palitra[w[1]])
                w[2] = int(palitra[w[2]])
                pixels[i, j] = tuple(w)
        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply_button.move(910, 600)
        self.idkhowtonamethis = False

    def anagliph(self, z):
        anagl = self.im.copy()
        if self.idkhowtonamethis:
            delta = z
        else:
            delta = self.value_anagliph
        if delta == 0:
            anagl.save(self.dataname)
            self.pixmap = QPixmap(self.dataname)
            self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
            self.image.setPixmap(self.smaller_pixmap)
            pass
        else:
            ims = anagl.copy()
            p = anagl.load()
            ps = ims.load()
            k = anagl.copy()
            ks = k.load()
            self.newim = Image.new('RGB', (self.x, self.y), 'white')
            s = self.newim.load()

            for i in range(self.x):
                for j in range(self.y):
                    px = p[i, j]
                    p[i, j] = 0, px[1], px[2]

            for i in range(self.x - delta):
                for j in range(self.y):
                    pxs = ks[i, j]
                    ps[i + delta, j] = pxs[0], 0, 0

            for i in range(self.x):
                for j in range(self.y):
                    p2 = p[i, j]
                    p1 = ps[i, j]
                    s[i, j] = p2[0] + p1[0], p2[1] + p1[1], p2[2] + p1[2]

            for i in range(delta):
                for j in range(self.y):
                    s[i, j] = p[i, j]

            self.newim.save(self.dataname)
            self.pixmap = QPixmap(self.dataname)
            self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
            self.image.setPixmap(self.smaller_pixmap)
            self.apply_button.move(910, 600)
            self.idkhowtonamethis = False

    def degradation(self):
        self.newim = self.im.copy()
        self.newim = self.newim.filter(ImageFilter.GaussianBlur(self.value_degradation))
        self.last_value_degradation = self.value_degradation
        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply_button.move(910, 600)

    def negative(self):
        pixels = self.im.load()
        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                w[0] = 255 - w[0]
                w[1] = 255 - w[1]
                w[2] = 255 - w[2]
                pixels[i, j] = tuple(w)

        self.im.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)

    def left(self):
        self.im = self.im.rotate(270)
        self.im.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)

    def right(self):
        self.im = self.im.rotate(90)
        self.im.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)

    def bw(self):
        self.newim = self.im.copy()
        pixels = self.newim.load()

        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                if w[0] + w[1] + w[2] > 384:
                    w[0], w[1], w[2] = 256, 256, 256
                else:
                    w[0], w[1], w[2] = 0, 0, 0
                pixels[i, j] = tuple(w)

        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply()

    def min(self):
        if self.value_min == -1:
            pass
        else:
            if self.value_min % 2 == 0:
                self.value_min += 1
            self.newim = self.im.copy()
            self.newim = self.newim.filter(ImageFilter.MinFilter(size=self.value_min))
            self.newim.save(self.dataname)
            self.pixmap = QPixmap(self.dataname)
            self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
            self.image.setPixmap(self.smaller_pixmap)
            self.apply_button.move(910, 600)
        self.idkhowtonamethis = True

    def r(self):
        self.newim = self.im.copy()
        pixels = self.newim.load()
        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                w[0] = w[0]
                w[1] = 0
                w[2] = 0
                pixels[i, j] = tuple(w)
        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply()

    def g(self):
        self.newim = self.im.copy()
        pixels = self.newim.load()
        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                w[0] = 0
                w[1] = w[1]
                w[2] = 0
                pixels[i, j] = tuple(w)
        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply()

    def b(self):
        self.newim = self.im.copy()
        pixels = self.newim.load()
        for i in range(self.x):
            for j in range(self.y):
                w = list(pixels[i, j])
                w[0] = 0
                w[1] = 0
                w[2] = w[2]
                pixels[i, j] = tuple(w)
        self.newim.save(self.dataname)
        self.pixmap = QPixmap(self.dataname)
        self.smaller_pixmap = self.pixmap.scaled(550, 690, Qt.KeepAspectRatio)
        self.image.setPixmap(self.smaller_pixmap)
        self.apply()

    def f_1(self):
        con = sqlite3.connect('filters.db')
        cur = con.cursor()
        result = cur.execute("""SELECT anagliph FROM Filters
                    WHERE id = 1""").fetchall()
        self.idkhowtonamethis = True
        self.bw()
        self.anagliph(int(result[0][0]))

    def f_2(self):
        con = sqlite3.connect('filters.db')
        cur = con.cursor()
        result = cur.execute("""SELECT contrast FROM Filters
                            WHERE id = 2""").fetchall()
        self.idkhowtonamethis = True
        self.negative()
        self.contrast(int(result[0][0]) + 35)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
