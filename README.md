# 📸 Instagram Caption Scraper

A lightweight Flask + Selenium service to extract captions from **public Instagram Reels**.  
Includes rate limiting, Docker support, and ready-to-deploy configuration.

🌐 **Live Demo**: [Insta Caption Scraper](https://insta-caption-scraper-o9q2.onrender.com/)

---

## 🚀 Features
- 🖥️ Minimal web UI (HTML + JS).
- ⚡ REST API endpoint for programmatic use.
- 🔒 Rate limiting: **5 requests/minute/IP**.
- 🐳 Dockerfile + Render deployment manifest included.
- 📱 Mobile emulation with headless Chromium.

---

## 🛠️ Tech Stack

- **Backend**: Flask (Python)  
- **Scraping**: Selenium + Chrome WebDriver  
- **Frontend**: HTML (Jinja templates) + CSS  
- **Deployment**: Render + Docker
- 
---

## 📂 Project Structure
```
Insta/
├── Dockerfile
├── README.md
├── requirements.txt
├── app.py              # Flask app + endpoints
├── templates/
│   └── index.html       # UI
└── render.yaml          # Render deployment config
```

---

## 📡 API Usage

### `POST /scrape`
**Request JSON:**
```json
{
  "url": "https://www.instagram.com/reel/XXXXXXXXX/"
}
```

**Response (success):**
```json
{
  "status": "success",
  "caption": "This is the extracted caption"
}
```

**Response (error):**
```json
{
  "status": "error",
  "message": "Failed to extract caption"
}
```

---

## 🖥️ Local Development

```bash
# 1. Clone the repo
git clone https://github.com/girija-12/insta-caption-scraper.git
cd insta-caption-scraper/Insta

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run locally
python app.py
```

App runs on: **http://127.0.0.1:5000/**

---

## 🐳 Docker Setup

Build and run using Docker:
```bash
docker build -t insta-caption-scraper .
docker run -p 5000:5000 insta-caption-scraper
```

App runs on: **http://127.0.0.1:10000/**

---

## Screenshots
![Results](assets/Screenshot%202025-08-30%20112554.png)
---

## ⚠️ Notes
- Works only for public Instagram profiles.
- Might break if Instagram changes its layout or scraping restrictions.
- Requires stable internet and ChromeDriver support.
