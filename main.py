import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QTime, QRectF
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPainterPath

BREAK_DURATION = QTime(0, 5, 0, 0)  
INTERVAL_MS = 60*60*1000                  
SNOOZE_MS = 5 * 60 * 1000            
TICK_MS = 30                         

BTN_STYLE = """
QPushButton {{
    color: {color};
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 16px;
    padding: 6px 18px;
    font-size: 11px;
    font-family: 'Segoe UI';
}}
QPushButton:hover {{
    background-color: {bg_hover};
}}
QPushButton:pressed {{
    background-color: {bg_pressed};
}}
"""

PRIMARY_BTN = BTN_STYLE.format(
    color="white",
    bg="rgba(0, 200, 170, 140)",
    border="rgba(0, 230, 190, 180)",
    bg_hover="rgba(0, 220, 185, 180)",
    bg_pressed="rgba(0, 180, 150, 200)",
)

SECONDARY_BTN = BTN_STYLE.format(
    color="rgba(255,255,255,190)",
    bg="rgba(255,255,255,15)",
    border="rgba(255,255,255,50)",
    bg_hover="rgba(255,255,255,30)",
    bg_pressed="rgba(255,255,255,45)",
)


class WalkOverlay(QWidget):
    STATE_PROMPT = "prompt"        
    STATE_COUNTDOWN = "countdown" 
    STATE_DONE = "done"            

    def __init__(self):
        super().__init__()
        self.state = self.STATE_PROMPT
        self.remaining = BREAK_DURATION

        self._init_window()
        self._init_ui()

        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self._tick)

        self.fade_timer = QTimer(self)
        self.fade_timer.timeout.connect(self._fade_in_step)

        self.fade_out_timer = QTimer(self)
        self.fade_out_timer.timeout.connect(self._fade_out_step)

        self.done_timer = QTimer(self)
        self.done_timer.setSingleShot(True)
        self.done_timer.timeout.connect(self._begin_fade_out)

        self.hourly_timer = QTimer(self)
        self.hourly_timer.setSingleShot(True)
        self.hourly_timer.timeout.connect(self.show_reminder)
        self.hourly_timer.start(INTERVAL_MS)

    def _init_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(260, 190)
        self._position_right_center()

    def _position_right_center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.x() + screen.width() - self.width() - 40
        y = screen.y() + (screen.height() - self.height()) // 2
        self.move(x, y)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 26, 28, 24)
        layout.setSpacing(8)

        self.title_label = QLabel("TIME TO WALK")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: rgba(255,255,255,220);")
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        self.time_label = QLabel("05:00")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("color: white;")
        self.time_label.setFont(QFont("Segoe UI", 32, QFont.Weight.Light))

        self.sub_label = QLabel("a 5 minute break is due")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_label.setStyleSheet("color: rgba(255,255,255,140);")
        self.sub_label.setFont(QFont("Segoe UI", 9))

        self.start_btn = QPushButton("Start walk")
        self.start_btn.setStyleSheet(PRIMARY_BTN)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(self.begin_countdown)

        self.snooze_btn = QPushButton("Snooze 5m")
        self.snooze_btn.setStyleSheet(SECONDARY_BTN)
        self.snooze_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.snooze_btn.clicked.connect(self.snooze)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()
        btn_row.addWidget(self.start_btn)
        btn_row.addWidget(self.snooze_btn)
        btn_row.addStretch()

        layout.addWidget(self.title_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.sub_label)
        layout.addSpacing(4)
        layout.addLayout(btn_row)

        for lbl in (self.title_label, self.time_label, self.sub_label):
            glow = QGraphicsDropShadowEffect(self)
            glow.setBlurRadius(18)
            glow.setColor(QColor(0, 220, 180, 120))
            glow.setOffset(0, 0)
            lbl.setGraphicsEffect(glow)

        self.hide()

    def _to_ms(self, t: QTime) -> int:
        return t.hour() * 3600000 + t.minute() * 60000 + t.second() * 1000 + t.msec()

    def show_reminder(self):
        self.state = self.STATE_PROMPT
        self.remaining = BREAK_DURATION
        self.title_label.setText("TIME TO WALK")
        self.sub_label.setText("a 5 minute break is due")
        self._update_labels()
        self.start_btn.show()
        self.snooze_btn.show()
        self._position_right_center()
        self.setWindowOpacity(0.0)
        self.show()
        QApplication.beep()
        self._fade_step = 0
        self.fade_timer.start(15)

    def begin_countdown(self):
        self.state = self.STATE_COUNTDOWN
        self.start_btn.hide()
        self.snooze_btn.hide()
        self.sub_label.setText("stretch  •  breathe  •  hydrate")
        self.tick_timer.start(TICK_MS)

    def snooze(self):
        self.tick_timer.stop()
        self._begin_fade_out(next_delay=SNOOZE_MS)

    def _tick(self):
        self.remaining = self.remaining.addMSecs(-TICK_MS)
        if self._to_ms(self.remaining) <= 0:
            self.remaining = QTime(0, 0, 0, 0)
            self.tick_timer.stop()
            self._enter_done_state()
            return
        self._update_labels()

    def _update_labels(self):
        m = self.remaining.minute()
        s = self.remaining.second()
        self.time_label.setText(f"{m:02}:{s:02}")

    def _enter_done_state(self):
        self.state = self.STATE_DONE
        self.title_label.setText("NICE WORK")
        self.time_label.setText("✓")
        self.sub_label.setText("see you next hour")
        self.done_timer.start(1400)

    def _fade_in_step(self):
        self._fade_step += 1
        op = min(0.92, self._fade_step / 20 * 0.92)
        self.setWindowOpacity(op)
        if self._fade_step >= 20:
            self.fade_timer.stop()

    def _begin_fade_out(self, next_delay=INTERVAL_MS):
        self._next_delay = next_delay
        self._fade_step = 20
        self.fade_out_timer.start(15)

    def _fade_out_step(self):
        self._fade_step -= 1
        op = max(0.0, self._fade_step / 20 * 0.92)
        self.setWindowOpacity(op)
        if self._fade_step <= 0:
            self.fade_out_timer.stop()
            self.hide()
            delay = getattr(self, "_next_delay", INTERVAL_MS)
            self.hourly_timer.start(delay)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.state == self.STATE_PROMPT:
            self.snooze()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect().adjusted(6, 6, -6, -6))

        path = QPainterPath()
        path.addRoundedRect(rect, 24, 24)
        painter.fillPath(path, QBrush(QColor(15, 20, 30, 90)))

        painter.setPen(QPen(QColor(255, 255, 255, 25), 1))
        painter.drawPath(path)


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    overlay = WalkOverlay()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()