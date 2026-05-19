# 🚀 SnapClass AI Attendance System

SnapClass is an AI-powered smart classroom attendance system that automates attendance using **Face Recognition** and **Voice Authentication**.

The platform allows teachers to manage subjects and attendance while enabling students to register and authenticate using facial and voice embeddings.

---

# ✨ Features

## 👨‍🏫 Teacher Features
- Teacher Registration & Login
- Subject Management
- AI Attendance Dashboard
- Attendance Record Tracking

## 🎓 Student Features
- Automatic Face Login
- AI-based Student Registration
- Optional Voice Enrollment
- Face Recognition Authentication
- Voice-based Student Identification

## 🤖 AI Features
- Face Embedding Generation using Dlib
- Voice Embedding using Resemblyzer
- AI Attendance Prediction
- Multi-modal Authentication System
- Real-time Face Detection
- Speaker Recognition Pipeline

---

# 🧠 Tech Stack

## Frontend
- Streamlit

## Backend & Database
- Supabase

## Machine Learning / AI
- Dlib
- Resemblyzer
- Scikit-learn
- NumPy
- Librosa

## Other Tools
- Git
- GitHub
- Vercel

---

# 🌐 Live Demo

## Landing Page
https://landingsnapclass.vercel.app/

## AI Attendance Application
https://usesnapclass.streamlit.app/

---

# 📸 Screenshots

## Landing Page
_Add screenshot here_

## Teacher Dashboard
_Add screenshot here_

## Face Recognition Attendance
_Add screenshot here_

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Harshit-pundir/SnapClass.git
```

## Move into Project Directory

```bash
cd SnapClass
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```txt
.streamlit/secrets.toml
```

Add:

```toml
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_KEY = "YOUR_SUPABASE_KEY"
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# 📂 Project Structure

```txt
SnapClass/
│
├── src/
│   ├── components/
│   ├── database/
│   ├── pipelines/
│   ├── screens/
│   └── ui/
│
├── .streamlit/
├── app.py
├── requirements.txt
└── README.md
```

---

# 🧪 AI Pipelines

## Face Recognition Pipeline
- Detects faces using Dlib
- Generates 128-D facial embeddings
- Uses SVM classifier for prediction

## Voice Recognition Pipeline
- Generates voice embeddings
- Performs speaker identification
- Supports bulk audio processing

---

# 🎯 Future Improvements

- Real-time Webcam Attendance
- Attendance Analytics Dashboard
- Email Notifications
- Cloud Storage Integration
- Mobile Application
- Multi-classroom Support

---

# 👨‍💻 Author

## Harshit Pundir

- B.Tech CSE
- AI/ML Developer
- Python Developer
- Machine Learning Enthusiast

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
