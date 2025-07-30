from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from selenium.webdriver.chrome.service import Service

service = Service("/usr/bin/chromedriver")  # works with chromium-driver in Docker

logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()          # Also output to console
    ]
)

app = Flask(__name__)

limiter = Limiter(
    key_func=get_remote_address
)

def get_reel_caption(url):
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import logging

    logging.info(f"Scraping started for URL: {url}")

    options = Options()
    options.add_argument("--headless=new")  # Use new headless mode if available
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=375,812")  # Emulate mobile screen size

    # Spoof a mobile user-agent (Instagram often serves different markup for mobile)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15A372 Safari/604.1"
    )
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(url)
        logging.info("Page loaded successfully.")

        # Accept cookies popup if present
        try:
            cookie_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Only allow essential cookies") or contains(text(), "Accept All")]'))
            )
            cookie_btn.click()
            logging.info("Accepted cookie banner.")
        except:
            pass  # No cookie banner

        # Attempt primary: look for span in article (new layout)
        try:
            caption = wait.until(
                EC.presence_of_element_located((By.XPATH, '//article//div[contains(@class, "_a9zs")]/span'))
            ).text.strip()

            if caption:
                logging.info("Caption found via primary method.")
                return {"status": "success", "caption": caption}
        except TimeoutException:
            logging.warning("Primary method failed. Trying fallback...")

        # Fallback 1: Look for meta description
        try:
            meta_desc = driver.find_element(By.XPATH, '//meta[@property="og:description"]')
            content = meta_desc.get_attribute("content")
            if content:
                logging.info("Caption found via og:description fallback.")
                return {"status": "success", "caption": content.strip()}
        except Exception:
            logging.warning("og:description not found.")

        # Fallback 2: Scan all spans and find probable caption
        try:
            spans = driver.find_elements(By.XPATH, '//span')
            for span in spans:
                text = span.text.strip()
                if text and len(text) > 10:
                    logging.info("Caption found via fallback span scan.")
                    return {"status": "success", "caption": text}
        except Exception as e:
            logging.warning(f"Fallback span scan failed: {str(e)}")

        logging.error("Caption not found in any method.")
        return {"status": "error", "message": "Caption not found"}

    except Exception as e:
        logging.exception("An unexpected error occurred while scraping.")
        return {"status": "error", "message": str(e)}
    finally:
        driver.quit()
        logging.info("Browser closed.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
@limiter.limit("5 per minute")
def scrape():
    url = request.json.get('url')
    logging.info(f"Received scrape request for URL: {url}")

    if not url:
        logging.warning("No URL provided in request.")
        return jsonify({"status": "error", "message": "URL is required"})

    if not url.startswith(('http://', 'https://')):
        logging.warning("Invalid URL format.")
        return jsonify({"status": "error", "message": "Invalid URL format"})

    if 'instagram.com' not in url:
        logging.warning("Non-Instagram URL rejected.")
        return jsonify({"status": "error", "message": "Please enter an Instagram URL"})

    result = get_reel_caption(url)
    logging.info(f"Scraping result found")
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
