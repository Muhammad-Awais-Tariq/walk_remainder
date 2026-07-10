from datetime import datetime
import sys
from PyQt6.QtWidgets import QApplication , QWidget , QLabel , QGridLayout , QPushButton , QTextEdit , QTabWidget , QComboBox , QSizePolicy , QLineEdit , QMainWindow
from PyQt6.QtCore import  QTimer , Qt , QTime
from PyQt6.QtGui import QFont , QFontDatabase , QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Walk Remainder")
        self.setGeometry(1715, 290 , 200,200)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()