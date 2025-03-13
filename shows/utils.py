import time
from playwright.sync_api import sync_playwright

def scrape_video_source(url: str) -> str | None:
    with sync_playwright() as p:
        browser = p.firefox.launch(
            headless=True,
            args=[
                '--disable-gpu',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
            ]
        )
        page = browser.new_page()
        
        # Navigate to the URL
        page.goto(url)
        
        # Wait for video element with timeout
        video_tag = None
        max_attempts = 10 # Timeout in seconds to wait for video element
        for _ in range(max_attempts):
            try:
                # Check if video element exists
                video_tag = page.query_selector("video")
                if video_tag:
                    break
            except:
                pass
            time.sleep(1)
        
        # If no video tag found after all attempts
        if not video_tag:
            browser.close()
            return None
        
        # Try to find source tag and get src attribute
        try:
            src_tag = video_tag.query_selector("source")
            if src_tag:
                src_url = src_tag.get_attribute("src")
                browser.close()
                return src_url
        except:
            pass
        
        browser.close()
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

    
