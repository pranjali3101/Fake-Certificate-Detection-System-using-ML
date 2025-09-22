# Fake Certificate Detection System using ML

This project is a **Fake Certificate Detection System** built using **Machine Learning** to identify and verify the authenticity of certificates. It provides a reliable way to detect forged or tampered certificates by combining **image processing, database validation, and ML models** for classification.

## 🔍 Features

* **Certificate Upload**: Upload certificate images in formats like JPG/PNG/PDF.
* **Preprocessing**: Image enhancement, text extraction (OCR), and feature extraction.
* **Machine Learning Model**: Trained classifier to distinguish between *genuine* and *fake* certificates.
* **Database Verification**: Cross-check certificate details against a trusted database.
* **Streamlit Web App**: User-friendly interface for certificate verification.
* **Real-time Results**: Instant authenticity check with accuracy reports.

## 🛠️ Tech Stack

* **Python** (ML + backend)
* **OpenCV** & **Pillow** (image processing)
* **Tesseract OCR** (text extraction)
* **scikit-learn / TensorFlow / PyTorch** (ML model)
* **SQLite/MySQL** (certificate records database)
* **Streamlit** (web-based interface)

## 🚀 How It Works

1. User uploads a certificate image or enters certificate ID.
2. System extracts key features using OCR & image analysis.
3. ML model predicts whether the certificate is *real* or *fake*.
4. Details are cross-verified with the database.
5. The system outputs authenticity status with explanation.

## 📌 Use Cases

* Universities verifying student degree certificates.
* Companies validating candidate resumes.
* Government/Institutes preventing fraud in document submission.

## 📂 Project Structure

```
Fake-Certificate-Detection/
│── data/              # Sample certificate dataset
│── model/             # Trained ML models
│── app.py             # Streamlit app entry point
│── preprocessing.py   # Image & text preprocessing
│── verifier.py        # Certificate verification logic
│── database/          # SQLite/MySQL schema
│── requirements.txt   # Dependencies
│── README.md          # Project description
```

## 📊 Future Enhancements

* Integration with **blockchain** for tamper-proof certificate storage.
* API service for third-party verification.
* Improved ML model with larger training dataset.

---

✨ This project demonstrates how **Machine Learning** and **computer vision** can be used to tackle certificate fraud effectively.

#Created By - Pranjali Shewale 
# Support By - NewGen Tech Pvt. Ltd.
