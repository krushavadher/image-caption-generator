# VisionAI — Image Caption Generator

An AI-powered web app that generates captions, tags, and detects objects in any image using **Azure AI Vision** and **Python + Flask**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Azure](https://img.shields.io/badge/Azure-AI%20Vision-0078D4?style=flat-square&logo=microsoft-azure)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square)

---

## Features

- Generate natural language captions for any image
- Detect and list objects present in the image
- Extract relevant tags with confidence scores
- Support for both image URLs and local file uploads
- Clean dark-themed web UI — no frontend framework needed

## Azure Services Used

| Service | Purpose |
|---|---|
| Azure AI Vision (Computer Vision) | Image analysis, captioning, object detection |

## Demo

> Paste any image URL or upload a photo → get an instant AI-generated caption

Example output:
```
Caption    : "a group of people sitting around a table with laptops"
Confidence : 91.3%
Tags       : laptop, person, table, office, work, technology
Objects    : laptop, person, chair
```

## Project Structure

```
image-caption-generator/
├── app.py               # Flask backend + Azure Vision logic
├── templates/
│   └── index.html       # Frontend UI
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/image-caption-generator.git
cd image-caption-generator
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your Azure AI Vision resource
1. Go to [portal.azure.com](https://portal.azure.com)
2. Search for **Computer Vision** → Create
3. Choose **Free F0** tier
4. Copy your **Endpoint** and **Key 1** from Keys and Endpoint

### 5. Set up environment variables
```bash
cp .env.example .env
```
Edit `.env` and fill in your Azure credentials:
```
VISION_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
VISION_KEY=your_key_here
```

### 6. Run the app
```bash
python app.py
```
Open [http://localhost:5000](http://localhost:5000) in your browser.

## How It Works

1. User submits an image (URL or file upload)
2. Flask backend sends the image to **Azure AI Vision API**
3. Azure returns caption, tags, objects, and dense captions
4. Results are displayed in the UI instantly

## Tech Stack

- **Backend**: Python 3.10+, Flask
- **AI**: Azure AI Vision (azure-ai-vision-imageanalysis SDK)
- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Config**: python-dotenv

## License

MIT
