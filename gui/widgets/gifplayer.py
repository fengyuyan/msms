__author__ = 'Tom Yan'
from PyQt4 import QtGui, QtCore
from dialog import Dialog

class GifPlayer(Dialog):
    """
    Gif player
    """
    def __init__(self, gif, parent=None):
        super(GifPlayer, self).__init__(parent)
        self.gif = gif
        self.gif_label = QtGui.QLabel(self)
        self.movie = QtGui.QMovie(gif)
        self.gif_label.setMovie(self.movie)
        wish = "Happy Birthday! This is the gift for your international business and it's not finished yet. I am so \
so sorry! I will try to develop a complete version by end of this year!"
        self.wish_label = QtGui.QLabel(wish)
        self.wish_label.setWordWrap(True)
        font = self.wish_label.font()
        font.setBold(True)
        font.setFamily('Harlow Solid Italic')
        font.setPointSize(12)
        self.wish_label.setFont(font)
        btn = QtGui.QPushButton('I Love Tom')
        btn.clicked.connect(self.accept)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.gif_label)
        layout.addWidget(self.wish_label)
        layout.addWidget(btn)
        self.movie.start()
        self.setWindowTitle('Happy Birthday LP')
