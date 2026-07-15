import sys

import matplotlib

matplotlib.use("Qt5Agg")

from os.path import join as join_path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui, QtWidgets


class UIGraph(object):
    def setupUi(self, Graph):
        Graph.setObjectName("Graph")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Graph.sizePolicy().hasHeightForWidth())
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(join_path("media_resources", "Generate.ico")),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        Graph.setWindowIcon(icon)
        Graph.setStyleSheet("background-color: rgb(32, 33, 37);\n")
        Graph.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Graph)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)
        self.main_frame = QtWidgets.QFrame(Graph)
        self.main_frame.setMinimumSize(QtCore.QSize(400, 400))
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.bottomLayout = QtWidgets.QVBoxLayout(self.main_frame)
        self.bottomLayout.setContentsMargins(0, -1, 0, -1)
        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setObjectName("bottomLayout")
        self.frame_addSelClan = QtWidgets.QFrame(self.main_frame)
        self.frame_addSelClan.setSizePolicy(sizePolicy)
        self.frame_addSelClan.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_addSelClan.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_addSelClan.setObjectName("frame_addSelClan")
        self.topLayout = QtWidgets.QHBoxLayout(self.frame_addSelClan)
        self.topLayout.setContentsMargins(-1, -1, -1, 0)
        self.topLayout.setObjectName("topLayout")
        self.label_choiceClan = QtWidgets.QLabel(self.frame_addSelClan)
        font = QtGui.QFont()
        font.setFamily("Segoe Print")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_choiceClan.setFont(font)
        self.label_choiceClan.setStyleSheet("color: white;")
        self.label_choiceClan.setTextFormat(QtCore.Qt.AutoText)
        self.label_choiceClan.setAlignment(
            QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft
        )
        self.label_choiceClan.setObjectName("label_choiceClan")
        self.topLayout.addWidget(self.label_choiceClan)
        self.comboBox_clan = QtWidgets.QComboBox(self.frame_addSelClan)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.comboBox_clan.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_clan.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(14)
        self.comboBox_clan.setFont(font)
        self.comboBox_clan.setStyleSheet(
            "background-color: rgba(21, 22, 26, 255);\n"
            "color: rgb(190, 190, 190);\n"
            "border-radius: 10px;\n"
            "border-bottom: 2px solid rgba(80, 80, 85, 255);\n"
            "border-right: 2px solid rgba(80, 80, 85, 255);\n"
            "border-top: 2px solid rgba(80, 80, 85, 255);\n"
            "border-left: 2px solid rgba(80, 80, 85, 255);\n"
            "selection-background-color: white;\n"
            "selection-color: rgba(21, 22, 26, 255);\n"
            ""
        )
        self.comboBox_clan.setObjectName("comboBox_clan")
        self.topLayout.addWidget(self.comboBox_clan)
        self.bottomLayout.addWidget(
            self.frame_addSelClan, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.line = QtWidgets.QFrame(self.main_frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.bottomLayout.addWidget(self.line)
        self.figure = plt.figure(figsize=(800, 500), dpi=70, frameon=False)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.bottomLayout.addWidget(self.canvas)
        self.bottomLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.main_frame)

        self.retranslateUi(Graph)
        QtCore.QMetaObject.connectSlotsByName(Graph)

    def retranslateUi(self, Graph):
        _translate = QtCore.QCoreApplication.translate
        Graph.setWindowTitle(_translate("Graph", "Дерево роду"))
        self.label_choiceClan.setText(_translate("Graph", "Рід"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Graph = QtWidgets.QDialog()
    ui = UIGraph()
    ui.setupUi(Graph)
    Graph.show()
    sys.exit(app.exec_())
