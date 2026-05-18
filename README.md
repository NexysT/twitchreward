<div align="center">

# Twitch Auto Reward Clicker

**Watches your screen. Clicks when it turns green. You sleep.**

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat&logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat)

</div>

---

## 💡 What it does

Most Twitch rewards follow the same pattern — the button is **grey** when unavailable, and turns **green** when you can claim it.

This tool monitors any area of your screen in real time. The moment it detects grey → green, it waits a second and clicks. No browser extensions, no API keys, no accounts. Just pixel detection and a mouse click.

---

## Demo

> Select area → monitor → auto click on green

![demo](https://i.imgur.com/kRVvXEf.png)

---

## ✨ Features

- 🖱️ Visual area selection with a fullscreen overlay
- 🎨 Real-time RGB pixel analysis — detects the exact moment it turns green
- ⏱️ 1s natural delay before clicking + smooth mouse movement
- 📋 Supports multiple areas at once
- 📊 Adjustable sensitivity slider with live debug output
- 🔔 Minimizes to system tray (like Discord) — runs silently in the background
- ✅ Builds into a standalone `.exe` — no terminal, no Python required

---

## 🚀 Quick Start

**Run with Python**
```bash
pip install pyautogui pillow numpy pystray
python AutoGreenClicker.py
```

**Build as `.exe`**
```
1. Place AutoGreenClicker.py, BUILD.bat and icon.ico in the same folder
2. Run BUILD.bat
3. Your exe is at dist\AutoGreenClicker.exe
```

---

## 🎮 How to use

1. Open the app and click **+ Add area**
2. Draw a rectangle over the reward button on screen
3. Give it a name and hit **Start monitoring**
4. Close the window — it stays in the tray
5. Walk away

When the reward becomes available, the app catches it, waits 1 second, and clicks.

---

## ⚙️ Sensitivity

The slider sets the minimum percentage of green pixels required to trigger a click.

| Scenario | Recommended |
|---|---|
| Full button turns green | 30 – 50% |
| Partial highlight | 10 – 20% |
| Small icon or indicator | 3 – 8% |

The live debug shows the real detected value — set the slider ~10 points below that.

---

## Stack

`Python` `Tkinter` `Pillow` `NumPy` `PyAutoGUI` `Pystray` `PyInstaller`

---

<div align="center">
<sub>Built to never miss a reward again.</sub>
</div>
