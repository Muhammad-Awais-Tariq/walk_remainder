# Walk Reminder
A transparent, frameless overlay that pops up once every hour to nudge you into taking a 5 minute walk break — no title bar, no close button, just a floating glass card that stays out of your way until it's time to move.

## Features
- Frameless, translucent overlay window that stays on top without cluttering the taskbar
- Appears automatically once an hour — no need to open or babysit the app
- **Start walk** button begins a live 5 minute countdown when you're actually ready
- **Snooze 5m** button (or `Esc`) pushes the reminder back by 5 real minutes if the timing's bad
- Smooth fade in/out animation instead of an abrupt popup
- Brief "Nice work" confirmation once the walk timer finishes
- Soft system beep when the reminder appears, so it doesn't rely on catching your eye
- Fixed position on the right-center of the screen — no dragging, no repositioning by accident

## How the Clock Works
The app has no visible window until it's time for a break — it just runs quietly in the background.

- **Prompt state**: once an hour, the overlay fades in showing `05:00` with two buttons.
  - Click **Start walk** to begin the 5 minute countdown.
  - Click **Snooze 5m** (or press `Esc`) to dismiss it and get reminded again in 5 real minutes.
- **Countdown state**: the timer counts down live while you're on your break. No buttons are shown during this time.
- **Done state**: when the countdown hits zero, the card briefly shows "NICE WORK ✓" before fading out and scheduling the next hourly reminder.

## How to Run the Program
1. Make sure **Python** is installed.
2. Install `uv` if you don't already have it, then let it handle the dependency automatically — no `requirements.txt` needed since the script declares its own dependencies inline:
   ```bash
   uv run walk_reminder.py
   ```
   The first run will install PyQt6 into an isolated environment automatically.

### Running it as a standalone app (recommended for daily use)
To turn it into a proper Windows app you can add to the Start Menu and forget about:
```bash
uv venv
.venv\Scripts\activate
uv pip install PyQt6 pyinstaller
pyinstaller --onefile --windowed --name "WalkReminder" walk_reminder.py
```
This produces `dist\WalkReminder.exe`, a standalone executable with no console window. Create a shortcut to it and drop that shortcut into your Startup folder (`shell:startup`) so it launches automatically every time you log in.

## File Structure
```bash
project/
│── main.py
│── README.md
```

## Technologies Used
- Python
- PyQt6
- QPainter (custom-drawn glass card UI)
- PyInstaller (for building a standalone `.exe`)

## Notes
- `INTERVAL_MS` controls the gap between reminders after a completed walk — set to `60 * 60 * 1000` for real hourly use (a shorter value is useful only for testing).
- Snoozing always waits a real 5 minutes (`SNOOZE_MS`), independent of the `INTERVAL_MS` testing value.
- There is intentionally no way to close or cancel the app from the overlay itself — it's designed to run silently in the background. To stop it, end the process via Task Manager.
- Positioning and window behavior (frameless, always-on-top, no drag) are tuned for Windows; other platforms haven't been tested.

## Author
Muhammad Awais Tariq

---
If you like this project, consider giving it a star on GitHub!