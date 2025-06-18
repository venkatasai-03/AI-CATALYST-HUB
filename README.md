# 🧠 AI Catalyst Hub

A scalable B2B AI platform delivering plug-and-play machine learning solutions across multiple industries—**healthcare, agriculture, business, and pollution control**. Developed as a final-year engineering project at VIT-AP University, this hub democratizes AI for startups and SMEs by offering domain-specific, pre-trained, and customizable AI/ML models.

## 📌 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Domains & Models](#domains--models)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Demo](#demo)
- [Results](#results)
- [Future Scope](#future-scope)
- [Contributors](#contributors)
- [License](#license)

---

## Overview

**AI Catalyst Hub** was built to bridge the AI accessibility gap for organizations that cannot afford expensive AI development. It simplifies AI adoption through a collection of pre-trained models across key domains:

- 👩‍⚕️ Healthcare
- 🌾 Agriculture
- 💼 Business Analytics
- 🌍 Pollution Control

These models are optimized, scalable, and can be accessed through an interactive web UI or APIs.

---

## 🚀 Key Features

- 🔌 Pre-trained, customizable ML/DL models
- 🧠 Support for structured (tabular), unstructured (image, text) data
- 🔎 Real-world use cases across 4 industries
- 📈 High-performance models with accuracy up to 98%
- 📦 Docker-based deployment ready
- 🧩 Modular codebase for plug-and-play use

---

## 🏥🌱📊🌫️ Domains & Models

### 🔬 Healthcare
| Task | Model | Accuracy |
|------|-------|----------|
| Eye Disease Classification | Swin Transformer + EfficientNet | 94.6% |
| Heart Disease Prediction | Logistic Regression | 89.3% |
| Diabetes Prediction | Random Forest | 92.1% |

### 🌾 Agriculture
| Task | Model | Accuracy |
|------|-------|----------|
| Crop Recommendation | KNN | 98.8% |
| Soil Quality Prediction | XGBoost | 86.3% |
| Crop Quality Classification | CNN | 85–90% |

### 📈 Business
| Task | Model | Accuracy |
|------|-------|----------|
| Customer Segmentation | K-Means | Silhouette ~ 0.65 |
| Sentiment Analysis | DistilBERT | 91.2% |
| Churn Prediction | Random Forest | 87.4% |

### 🌫️ Pollution Control
| Task | Model | Metric |
|------|-------|--------|
| AQI Prediction | Random Forest | MAE = 3.2 |
| Water Quality Classification | Logistic Regression | 95.75% |
| Soil-Based Disease Prediction | SVM | 88.9% |

---

## 🧰 Tech Stack

- **Languages:** Python
- **Frameworks:** TensorFlow, PyTorch, Scikit-learn, XGBoost, Flask
- **Deployment:** Docker, FastAPI
- **Frontend:** HTML/CSS (basic)
- **NLP:** Transformers (Hugging Face - DistilBERT)
- **Data Handling:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.8+
- pip
- Git

### Clone the repository

```bash
git clone https://github.com/venkatasai-03/AI-CATALYST-HUB.git
cd AI-CATALYST-HUB```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run Flask API

```bash
python app.py
```

### Docker (Optional)

```bash
docker build -t ai-catalyst-hub .
docker run -p 5000:5000 ai-catalyst-hub
```

---

## 🌐 Demo

👉 [Live Demo (Render)](https://ai-catalyst-hub.onrender.com/)

---

## 📊 Results

| Domain       | Accuracy Range | Notes                                     |
|--------------|----------------|-------------------------------------------|
| Healthcare   | 89–94%         | Highly interpretable, clinical support    |
| Agriculture  | 86–98%         | Enables precision farming                 |
| Business     | ~91%           | Improves customer analytics               |
| Pollution    | 88–96%         | Supports early warning systems            |

---

## 🚧 Future Scope

- Add domains like Education, Finance, and Manufacturing
- Integrate Explainable AI (SHAP, LIME)
- Build real-time dashboards
- Introduce AutoML for dynamic model selection
- Enable real-time alerts and APIs for public use

---

## 👥 Contributors

- [M Venkata Sai](https://github.com/venkatasai-03)
- [YVK Chaitanya]
- [D Tirumalesh]

> Project guided by **Dr. Aravapalli Rama Satish**, VIT-AP University
