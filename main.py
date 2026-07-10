from datetime import datetime
import sys
from PyQt6.QtWidgets import QApplication , QWidget , QLabel , QGridLayout , QPushButton , QTextEdit , QTabWidget , QComboBox , QSizePolicy , QLineEdit , QMainWindow , QVBoxLayout
from PyQt6.QtCore import  QTimer , Qt , QTime
from PyQt6.QtGui import QFont , QFontDatabase , QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time = QTime(0,5,0,0)
        self.time_label = QLabel("00:05:00.00" , self)
        self.start_button = QPushButton("Start" , self)
        self.timer = QTimer(self)
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Walk Remainder")
        self.setGeometry(1715, 290 , 200,200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.start_button)

        central_widget.setLayout(vbox)
        self.start_button.clicked.connect(self.start)
        self.timer.timeout.connect(self.update_display)
    def start(self):
        self.timer.start(10)

    def format_time(self , time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        millisecond = time.msec()

        return f"{hours:02}:{minutes:02}:{seconds:02}.{millisecond // 10:02}"

    def update_display(self):
        if self.time == QTime(0, 0, 0, 0):
            self.timer.stop()

            self.time = QTime(0, 5, 0, 0)
            self.time_label.setText(self.format_time(self.time))

            QTimer.singleShot(60 * 60 * 1000, self.start)
            return

        self.time = self.time.addMSecs(-10)
        self.time_label.setText(self.format_time(self.time))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()