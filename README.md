# Candy Dispenser (3-Slot Automatic Dispenser)

An automated candy dispensing system controlled via a Python (Tkinter) graphical interface and driven by an Arduino UNO controlling 3 independent servo motors.

---

## Hardware & Software Prerequisites

* **Hardware:**
  * Arduino UNO (with USB cable)
  * 3 servo motors (e.g., SG90) connected to pins **D8**, **D9**, and **D10**
  * External 5V power supply recommended for the servos (with shared GND to the Arduino)
* **Software:**
  * [Python 3.10+](https://www.python.org/) (*on Windows, check "Add Python to PATH" during setup*)
  * [Arduino IDE](https://www.arduino.cc/en/software)
  * [Git](https://git-scm.com/)

---

## Quick Start Guide

### 1. Clone the Repository
Open a terminal and clone the project:
```bash
git clone [https://github.com/](https://github.com/)<your-username>/candy-dispenser.git
cd candy-dispenser
