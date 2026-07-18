# 🎓 SmartLens – AI-Powered Attendance System

An intelligent attendance management system that uses **Artificial Intelligence** and **Facial Recognition** to automatically identify students and record attendance in real time. SmartLens eliminates manual attendance, improves accuracy, and provides a seamless user experience.

---

## ✨ Features

* 🤖 AI-powered face recognition
* 📸 Real-time webcam attendance
* 👨‍🎓 Register new students using image datasets
* ⚡ Fast and accurate face detection
* 📊 Automatic attendance recording
* 🌐 User-friendly web interface
* 🔒 Secure and reliable recognition

---

## 📁 Project Structure

```text
SmartLens-Attendance-AI-Powered/
│
├── app.py
├── dataset/
│   └── HariPrasanth/
│       ├── img1.jpg
│       ├── img2.jpg
│       └── img3.jpg
├── static/
├── templates/
├── requirements.txt
└── README.md
```

---

## 📁 Adding Student Dataset

To register a new student:

1. Open the `dataset/` folder.
2. Create a new folder using the student's name.
3. Add **10–20 clear facial images** captured from different angles.

### Example

```text
dataset/
└── HariPrasanth/
    ├── img1.jpg
    ├── img2.jpg
    ├── img3.jpg
```

> **Tip:** Use high-quality images with good lighting and different facial expressions for better recognition accuracy.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/SmartLens-Attendance-AI-Powered.git
```
2. Create a Virtual Environment

Windows

python -m venv venv

macOS / Linux

python3 -m venv venv
3. Activate the Virtual Environment

Windows (Command Prompt)

venv\Scripts\activate

Windows (PowerShell)

venv\Scripts\Activate.ps1

macOS / Linux

source venv/bin/activate

After activation, you should see:

(venv)

at the beginning of your terminal prompt.
Navigate to the project folder:

```bash
cd SmartLens-Attendance-AI-Powered
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 🧠 Tech Stack

* **Python**
* **Flask**
* **OpenCV**
* **face_recognition**
* **NumPy**
* **HTML5**
* **CSS3**
* **JavaScript**

---

## 🚀 Future Enhancements

* 📱 Mobile application support
* ☁️ Cloud database integration
* 📊 Attendance analytics dashboard
* 📧 Email notifications
* 🧑‍🏫 Multi-class attendance management
* 🌍 Face recognition using live IP cameras

---

## 👨‍💻 Author

**Hari Prasanth**

AI & Machine Learning Developer • Front-End Developer • Flutter Developer

---

⭐ **If you found this project useful, consider giving it a star on GitHub!**
