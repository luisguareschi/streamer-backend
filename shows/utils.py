import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def scrape_video_source(url: str) -> str | None:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Set up Selenium with Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)

    # Wait for the video element
    max_attempts = 10
    video_tag = None
    for _ in range(max_attempts):
        try:
            video_tag = driver.find_element(By.TAG_NAME, "video")
            if video_tag:
                break
        except:
            pass
        time.sleep(1) 
    if not video_tag:
        driver.quit()
        return None
    try:
        src_tag = video_tag.find_element(By.TAG_NAME, "source")
        if src_tag:
            src_url = src_tag.get_attribute("src")
            driver.quit()
            return src_url
    except:
        pass

    driver.quit()
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
    watch_url = get_watch_url(tmdb_id=786892, media_type="movie")
    print("watch_url", watch_url)

    
