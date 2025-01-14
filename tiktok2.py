import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Path to ChromeDriver
chromedriver_path = r"C:\Users\andre\chromedriver-win64\chromedriver.exe"
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open TikTok login page
login_url = "https://www.tiktok.com/login"
driver.get(login_url)

print("Please manually log in and solve the CAPTCHA.")

# Wait until the user is logged in
try:
    profile_url = "https://www.tiktok.com/@d4ddy4lph4"
    driver.get(profile_url)
    
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/video/')]"))
    )
    print("Login detected! Proceeding to scrape video URLs.")
except Exception as e:
    print(f"An error occurred while waiting for login: {e}")
    driver.quit()
    exit()

# Scroll to load all videos
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Scrape video links
video_urls = []
video_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
for video in video_elements:
    video_urls.append(video.get_attribute("href"))

# Remove duplicates
video_urls = list(set(video_urls))

# Create a directory for videos
os.makedirs("TikTokVideos", exist_ok=True)

# Function to download videos
def download_video(video_url, file_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(video_url, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        # Write video content to file
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {file_path}")
    except Exception as e:
        print(f"Failed to download {video_url}: {e}")

# Download each video
for idx, url in enumerate(video_urls, start=1):
    video_id = url.split("/")[-1]  # Extract video ID from URL
    file_path = os.path.join("TikTokVideos", f"video_{idx}_{video_id}.mp4")
    download_video(url, file_path)

# Quit the WebDriver
driver.quit()


# d4ddy4lph4
# UrgMondays1!