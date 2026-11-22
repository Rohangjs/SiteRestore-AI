
# SiteRestore AI
### AI-Powered Network Documentation Restoration System

## 1. Project Overview

SiteRestore AI is an image restoration system designed to improve degraded telecom and network infrastructure documentation images.

The system combines traditional image processing techniques using OpenCV with AI-based super-resolution using Real-ESRGAN.

It aims to improve the visual clarity of infrastructure images and support telecom maintenance and planning workflows.

## 2. Key Features

- Image restoration using OpenCV.
- AI-based image enhancement using Real-ESRGAN.
- Support for four degradation categories:
  - Blur
  - Noise
  - Low Resolution
  - Low Contrast
- Original and restored image comparison.
- Image quality evaluation using PSNR and SSIM.
- Processing-time measurement.
- Streamlit-based user interface.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| User Interface | Streamlit |
| Image Processing | OpenCV |
| AI Restoration | PyTorch, Real-ESRGAN |
| Data Analysis | NumPy, Pandas |
| Visualization | Matplotlib |
| Quality Evaluation | PSNR, SSIM |

## 4. Project Structure

```text
SiteRestore-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── compare_results.py
│   ├── evaluation.py
│   ├── opencv_baseline.py
│   ├── performance_analysis.py
│   ├── preprocessing.py
│   ├── restoration.py
│   ├── restore_batch.py
│   ├── three_method_chart.py
│   ├── visualize_results.py
│   └── web_backend.py
│
├── data/
│   ├── original/
│   └── degraded/
│
├── outputs/
│   ├── opencv_baseline/
│   └── restored/
│
├── reports/
│
└── Real-ESRGAN/
```

Note: The Real-ESRGAN repository, model weights, datasets, and generated outputs are maintained separately and are not included in this Git repository.

## 5. Installation and Setup

### Prerequisites

- Python 3.11
- Git
- pip

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd SiteRestore-AI
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install PyTorch

Install a PyTorch version compatible with your hardware.

For CPU-only systems, the project was developed using PyTorch 2.1.2 and torchvision 0.16.2.

```bash
pip install torch==2.1.2 torchvision==0.16.2
```

### Step 5: Clone Real-ESRGAN

```bash
git clone https://github.com/xinntao/Real-ESRGAN.git
```

Install its dependencies and package:

```bash
cd Real-ESRGAN
pip install -r requirements.txt
python setup.py develop
cd ..
```

### Step 6: Download model weights

Download the `RealESRGAN_x4plus.pth` pretrained model from the official Real-ESRGAN project.

Place it inside:

```text
Real-ESRGAN/weights/RealESRGAN_x4plus.pth
```

## 6. Run the Application

From the project root:

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 7. Evaluation

The project evaluates restoration performance using:

- PSNR (Peak Signal-to-Noise Ratio)
- SSIM (Structural Similarity Index)
- Processing time

For quantitative evaluation, restored images should be compared against their corresponding clean reference images.

## 8. Important Notes

- Large datasets and pretrained model weights are not stored in this repository.
- Each team member should configure their own Python virtual environment.
- Real-ESRGAN requires additional setup.
- AI restoration may introduce visual artifacts or hallucinated details. Restored images should not be treated as engineering-accurate infrastructure records without verification.

## 9. Project Status

Academic project under development. until required

