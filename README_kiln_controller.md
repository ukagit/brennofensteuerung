# 🏺 Kiln Controller (ESP32 + MicroPython)

![ESP32](https://img.shields.io/badge/ESP32-MicroPython-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)

👉 **0–1000°C • MAX6675 • WiFi • Web UI • PID Control**  

A modern, high-precision kiln controller built with MicroPython and ESP32.  
Designed for makers, hobby ceramic artists, and experimental setups requiring reliable and flexible temperature control.

---

## ✨ Highlights

- 🎯 **Precise PID control** for stable temperature curves  
- 🔄 **Programmable firing profiles** (Ramp → Hold → Cooldown)  
- 🌐 **Modern web interface** (no app required)  
- 📊 **Live temperature monitoring** with charts  
- ⚡ **Lightweight & fast** (ESP32 + MicroPython)  
- 🧠 **Reusable profiles** for consistent results  

---

## 🖥️ Web Interface

- Real-time temperature graph  
- Responsive design (mobile & desktop)  
- Start/stop processes remotely  
- Edit firing profiles directly  

---

## 🔥 Use Cases

- 🏺 Ceramic firing (biscuit & glaze)  
- 🔬 DIY experiments & material testing  
- 🔥 Glass fusing & slumping  
- 🛠️ Retrofitting old kilns  

---

## ⚡ Hardware

- ESP32  
- MAX6675 temperature sensor  
- K-type thermocouple  
- Relay / SSR  

---

## 🧠 Control System

Uses a PID controller with time-based PWM:

- Ramp-Up (°C/h)  
- Hold temperature  
- Controlled cooldown  

---

## 🛡️ Safety

⚠️ **IMPORTANT: Hardware safety required!**

- Always use an independent **over-temperature cutoff (STB)**  
- Never operate unattended  
- Ensure proper ventilation  

Includes:

- emergency stop  
- sensor failure detection  
- automatic shutdown (~1020°C)  

---

## ⚠️ Disclaimer

This is a hobby project and not certified for industrial use.  
Use at your own risk.

---

## 📦 Installation

1. Configure WiFi in `wifi_config.py`  
2. Flash files to ESP32  
3. Open browser → ESP32 IP  

---

## 🔄 Update

```bash
mpremote cp main.py :
```

Restart after upload.

---

## 🧩 Tech Stack

- MicroPython  
- ESP32  
- MAX6675 (SPI)  
- Chart.js  

---

## ⭐ Why this project?

A simple, flexible alternative to expensive kiln controllers — built for makers.

---

🔥 *Build. Experiment. Fire.*
