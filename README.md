# VisageLab — Face Recognition Toolkit

A consent-based face detection and recognition toolkit built with **Python, OpenCV, and Streamlit**. VisageLab supports face enrollment, webcam recognition, image and video processing, model evaluation, and recognition performance testing.

## 🚀 Features

- **Face Detection:** Detect faces using OpenCV Haar Cascade.
- **Face Recognition:** Identify enrolled people using the LBPH algorithm.
- **Webcam Recognition:** Detect and recognize faces in real time.
- **Face Enrollment:** Register people using images or webcam captures with consent.
- **Image & Video Processing:** Run face recognition on photos and video files.
- **Quality Checks:** Filter blurry, dark, low-contrast, and duplicate enrollment images.
- **Accuracy Evaluation:** Measure recognition accuracy, False Acceptance Rate (FAR), and False Rejection Rate (FRR).
- **Performance Benchmarking:** Measure processing time and estimate FPS.
- **Web Interface:** Use the Streamlit application or browser-based demo.
- **Privacy-Focused Design:** Process data locally on your machine.

## 🛠️ Technology Stack

- **Language:** Python
- **Computer Vision:** OpenCV
- **Face Detection:** Haar Cascade
- **Face Recognition:** Local Binary Patterns Histograms (LBPH)
- **Web Interface:** Streamlit, HTML, CSS, JavaScript
- **Data Processing:** NumPy, Pandas
- **Testing:** Pytest

## 📁 Project Structure

```text
VisageLab/
├── app.py
├── requirements.txt
├── pyproject.toml
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── visagelab/
│   ├── cli.py
│   ├── detection.py
│   ├── recognizer.py
│   ├── enrollment.py
│   ├── preprocess.py
│   ├── evaluate.py
│   ├── quality.py
│   ├── tracker.py
│   └── pipeline.py
├── web/
│   ├── index.html
│   └── src/
├── docs/
├── scripts/
├── tests/
└── data/
```

## ⚙️ Installation

### Prerequisites

- Python 3.9 or newer
- pip
- A webcam for live recognition (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/VisageLab.git
cd VisageLab
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Check the Installation

```bash
python -m visagelab doctor
```

## 💻 Usage

### 1. Enroll a Person

Register a person using existing images:

```bash
python -m visagelab enroll Alice a1.jpg a2.jpg --consent
```

Register using a webcam:

```bash
python -m visagelab enroll Bob --camera --shots 5 --consent
```

### 2. Recognize Faces

Start real-time webcam recognition:

```bash
python -m visagelab identify
```

Recognize faces in an image:

```bash
python -m visagelab identify --source photo.jpg --output result.jpg
```

Process a video:

```bash
python -m visagelab identify --source clip.mp4 --output result.mp4
```

### 3. Manage Enrolled People

View the enrolled gallery:

```bash
python -m visagelab list
```

Remove a person from the gallery:

```bash
python -m visagelab remove Alice --yes
```

### 4. Launch the Streamlit Application

```bash
streamlit run app.py
```

### 5. Open the Browser Demo

Open `web/index.html` in a supported web browser and allow webcam access when prompted.

## 📊 Evaluation and Testing

Run the built-in self-test:

```bash
python -m visagelab selftest
```

Evaluate recognition performance on a labelled dataset:

```bash
python -m visagelab evaluate testset --csv report.csv --json report.json
```

Run the test suite:

```bash
python -m pytest -q
```

## 🔍 How It Works

1. Capture an image or video frame.
2. Detect faces using Haar Cascade.
3. Preprocess and align the detected face.
4. Compare the face against the enrolled gallery using LBPH.
5. Apply recognition thresholds to determine whether a match is acceptable.
6. Display the recognition result and optionally track detections across video frames.

## 🔐 Privacy and Responsible Use

- Obtain informed consent before enrolling anyone.
- Keep face images and recognition data private.
- Do not commit personal face images or biometric data to GitHub.
- Inform people when recognition or logging is being used.
- Do not use this prototype as the sole basis for access control, surveillance, or decisions affecting individuals.
- Test the system under different lighting conditions and camera angles before relying on its results.

## ⚠️ Limitations

VisageLab uses Haar Cascade and LBPH, which are lightweight traditional computer vision methods. Recognition performance can vary with lighting, facial pose, image quality, and changes in appearance.

This project is intended for learning, experimentation, and research. It is not a replacement for a professionally validated biometric identification system.

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome. Please review `CONTRIBUTING.md` before submitting changes.

## 📄 License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## 👨‍💻 Author

**Aditya Singh Thakur**

GitHub: https://github.com/YOUR-USERNAME

---

⭐ If you find VisageLab useful, consider giving the repository a star!
