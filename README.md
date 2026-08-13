# 🎨 AirInk

### Gesture-Controlled Virtual Drawing Application

AirInk is a real-time computer vision application that lets you **draw in the air using your hand**.

Using a webcam, OpenCV, and MediaPipe, AirInk tracks hand movements and converts fingertip movements into strokes on a virtual canvas, creating a simple **touchless drawing interface**.

---

## ✨ Features

* 🖐️ Real-time hand tracking
* ✍️ Gesture-controlled drawing
* 🎨 Multiple drawing colors
* 🖌️ Three brush sizes
* 🧽 Eraser functionality
* 🗑️ Clear the canvas
* 💾 Save drawings as PNG images
* 🎯 Smooth fingertip tracking
* 📷 Real-time webcam interaction
* 🖥️ Separate webcam and drawing canvas views
* 📏 Live brush-size indicator

---

## 🛠️ Tech Stack

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| **Python**    | Core application                |
| **OpenCV**    | Webcam processing and drawing   |
| **MediaPipe** | Hand landmark detection         |
| **NumPy**     | Image and coordinate processing |

---

## 🎮 Controls

AirInk uses simple hand gestures and toolbar controls to interact with the canvas.

| Gesture / Action            | Function                   |
| --------------------------- | -------------------------- |
| ☝️ Index finger up          | Drawing mode               |
| ✌️ Index + middle finger up | Selection mode             |
| 🎨 Color                    | Open color palette         |
| 🧽 Eraser                   | Erase parts of the drawing |
| 🗑️ Clear                   | Clear the entire canvas    |
| 💾 Save                     | Save the current drawing   |
| 🔹 Small brush              | 3px                        |
| 🔸 Medium brush             | 6px                        |
| 🔴 Large brush              | 12px                       |
| `Q`                         | Exit application           |

---

## 🧠 How It Works

AirInk processes the webcam feed in real time.

The application uses **MediaPipe** to detect the user's hand and track its landmarks. The position of the index fingertip is used as the drawing cursor.

Finger positions are also analyzed to distinguish between drawing mode and selection mode.

### Processing Pipeline

```text
Webcam
   ↓
OpenCV Frame Capture
   ↓
MediaPipe Hand Detection
   ↓
Hand Landmark Tracking
   ↓
Gesture Recognition
   ↓
Drawing / Tool Selection
   ↓
Virtual Canvas
```

---

## 🎨 Drawing Tools

### Color Palette

AirInk provides a color palette that allows the user to select different drawing colors.

Available colors include:

* 🔴 Red
* 🟢 Green
* 🔵 Blue
* ⚫ Black
* 🟡 Yellow
* 🟣 Purple

The selected color is applied to subsequent strokes.

### Brush Sizes

Three brush sizes are available:

```text
Small   → 3px
Medium  → 6px
Large   → 12px
```

The currently selected brush size is displayed on the toolbar.

### Eraser

The eraser uses a larger stroke size to make removing unwanted portions of a drawing easier.

### Clear

The Clear tool removes the current drawing from the virtual canvas.

### Save

The Save tool stores the current drawing as a PNG image inside the `drawings/` directory.

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

* Python 3.10 or higher
* A working webcam
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/srishtisharma07/AirInk.git
cd AirInk
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```powershell
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run AirInk

```bash
python src/main.py
```

Make sure your webcam is connected and accessible.

---

## 📁 Project Structure

```text
AirInk/
│
├── assets/
│
├── drawings/
│
├── src/
│   ├── main.py
│   ├── drawing.py
│   ├── gestures.py
│   ├── hand_tracker.py
│   └── constants.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🧩 Core Components

### `main.py`

Controls the main application loop, webcam input, gesture handling, drawing interaction, and application windows.

### `hand_tracker.py`

Handles hand detection and landmark tracking using MediaPipe.

### `gestures.py`

Identifies finger positions and determines whether the user is in drawing or selection mode.

### `drawing.py`

Manages the virtual canvas and drawing functionality, including:

* Drawing strokes
* Smoothing
* Colors
* Brush sizes
* Eraser
* Clear
* Toolbar interaction

### `constants.py`

Contains application-wide constants such as:

* Colors
* Window dimensions
* Toolbar dimensions
* UI settings

---

## 🎯 Project Objective

AirInk was created as a hands-on exploration of:

* Computer Vision
* Hand Landmark Detection
* Gesture Recognition
* Real-Time Image Processing
* Human-Computer Interaction

The project demonstrates how a standard webcam can be transformed into a **touchless input device**.

---

## 📚 What I Learned

Building AirInk provided practical experience with:

* Real-time webcam processing
* MediaPipe hand landmarks
* Hand coordinate tracking
* Gesture-based interaction
* OpenCV drawing operations
* Smoothing noisy hand movements
* Building an interactive computer vision application
* Structuring a Python project
* Managing a project with Git and GitHub

---

## 🔮 Future Improvements

Possible future improvements include:

* ↩️ Undo and redo
* 🔷 Shape recognition
* 📐 Geometric drawing tools
* 📝 Text insertion
* 🎨 More color customization
* 🧠 Improved gesture recognition
* 📤 Additional export formats
* ⚡ Further performance optimization

---

## 👩‍💻 Author

**Srishti Sharma**

B.Tech Computer Science Engineering

---

## ⭐ Support

If you find AirInk interesting, consider giving the repository a ⭐.

---

<p align="center">
  Made with ❤️ using Python, OpenCV & MediaPipe
</p>
