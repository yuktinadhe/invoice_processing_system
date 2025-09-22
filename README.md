# 📑 Invoice Processing with OCR + RAG

A **FastAPI + OCR + RAG pipeline** project that lets you upload invoices (PDF), extract fields using OCR + NLP, and export the results to **Excel**.  
Built with **FastAPI**, **pdf2image**, **Tesseract**, **RAG pipeline**, and a **modern frontend** (HTML/CSS/JS).

---

## 🚀 Features

- 📂 Upload PDF invoices (drag & drop or click)
- 🔍 Extract key fields from invoices using **OCR + NLP + RAG**
- 📊 Export extracted fields into **Excel (.xlsx)**
- 🕑 View upload **history** with download links
- ⚙️ Settings section (future config options)
- 🎨 Modern UI with sidebar navigation

---

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/), Uvicorn  
- **OCR:** [pdf2image](https://pypi.org/project/pdf2image/), [Tesseract](https://github.com/tesseract-ocr/tesseract), Poppler  
- **Excel Export:** [OpenPyXL](https://openpyxl.readthedocs.io/)  
- **Frontend:** HTML + CSS + JavaScript (served via FastAPI `StaticFiles`)  
- **Data Persistence:** JSON history (`history.json`)  

---

## 📂 Project Structure

invoice_mvp/
│── app.py # FastAPI app (routes, endpoints)
│── requirements.txt # Dependencies
│── history.json # Upload history (auto-created)
│
├── templates/
│ └── index.html # Frontend HTML (Jinja2 template)
│
├── static/
│ ├── css/
│ │ └── style.css # Frontend styles
│ └── js/
│ └── script.js # Frontend interactivity
│
├── services/
│ └── rag_pipeline.py # RAG pipeline logic
│
├── utils/
│ ├── ocr_utils.py # OCR & PDF → Image helpers
│ ├── nlp_utils.py # NLP helpers
│ └── file_utils.py # File utilities
│
├── data/ # Uploaded PDFs
├── exports/ # Processed Excel files
└── tests/ # Unit tests

## 📊 Usage

Go to Upload Invoice → Upload or drag a PDF.
Fields will be extracted and shown on screen.
Download results as Excel.
View past uploads in History tab.

## ✅ Example Workflow

Upload invoice1.pdf
Extracted fields → Vendor, Date, Amount
Download invoice1.xlsx
Appears in History with timestamp and download link

## 🔮 Future Improvements

Add authentication (user-based history)
Support multiple file uploads
Enhance OCR accuracy with advanced preprocessing
Cloud deployment (Azure / AWS)

## 👨‍💻 Author
Developed by Yukti Nadhe
