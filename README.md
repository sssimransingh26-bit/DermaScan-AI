# DermaScan AI 
A web app that classifies **7 skin conditions** including Melanoma 
using EfficientNet-B0 + Flask.

> Not a medical diagnosis. Always consult a dermatologist.

## What it does
- Classifies 7 skin conditions with confidence score
- Rejects poor quality images before inference
- Returns severity, symptoms & precautions per condition
- Drag & drop UI with dark/light mode

## Tech Stack
Python, Flask, PyTorch, EfficientNet-B0 (timm), Vanilla JS

## Run Locally
```bash
git clone https://github.com/yourusername/dermascan-ai
cd dermascan-ai
pip install -r requirements.txt
python app.py
```

## Model
EfficientNet-B0 fine-tuned on HAM10000 dataset 
(10,015 dermoscopic images, 7 classes) achieving 
**82% validation accuracy**. AUC-ROC used over accuracy 
due to class imbalance.

## Roadmap
- [x] REST API + image quality validation
- [x] 7-class disease info system  
- [x] Responsive frontend
- [x] Fine-tuned on HAM10000 — 82% val accuracy
- [ ] Grad-CAM heatmap
- [ ] Docker + deployment
