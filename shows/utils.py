from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import time

def scrape_video_source(url: str) -> str | None:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    # FOR DIGITAL OCEAN ONLY
    chrome_path = "/.chromium/opt/google/chrome/chrome"
    chromedriver_path = "/.chromedriver/chromedriver"
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')  # DigitalOcean App Platform requires this
    options.add_argument('--remote-debugging-port=9222')
    options.binary_location = chrome_path
    service = Service(chromedriver_path)
    # END OF DIGITAL OCEAN ONLY
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(url)
    timer = 10 # Maximum time to wait for the video tag to load
    video_tag = None
    while timer > 0:
        time.sleep(1)
        timer -= 1
        try:
             video_tag = driver.find_element(By.TAG_NAME, "video")
        except NoSuchElementException:
             video_tag = None
             continue
        if video_tag:
                break
    if not video_tag:
        return None
    try:
        src_tag = video_tag.find_element(By.TAG_NAME, "source")
        return src_tag.get_attribute("src")
    except NoSuchElementException:
        return None



def get_watch_url(tmdb_id: int, media_type: str, season_number: int | None = None, episode_number: int | None = None) -> str | None:
    vid_link_url: str | None = None
    if media_type == "movie":
        vid_link_url = f"https://vidlink.pro/movie/{tmdb_id}"
    else:
        vid_link_url = f"https://vidlink.pro/tv/{tmdb_id}/{season_number}/{episode_number}"

    video_url = scrape_video_source(vid_link_url)

    return video_url

if __name__ == "__main__":
    # https://streamer-app.netlify.app/watch?mediaType=tv&id=95396&season=2&episode=8
    watch_url = get_watch_url(tmdb_id=107028, media_type="tv", season_number=1, episode_number=2)
    print("watch_url", watch_url)

    
