from opensubtitlescom import OpenSubtitles
from opensubtitlescom.responses import Subtitle
import re
from mainApi.settings import OPEN_SUBTITLES_API_KEY, OPEN_SUBTITLES_USERNAME, OPEN_SUBTITLES_PASSWORD

def srt_to_vtt(srt_text: str) -> str:
    """
    Converts an SRT subtitle string to a VTT subtitle string.
    """
    # Add WEBVTT header
    vtt_text = "WEBVTT\n\n"
    
    # Convert timestamps (SRT uses "," as decimal separator, VTT uses ".")
    srt_text = re.sub(r"(\d{2}:\d{2}:\d{2}),(\d{3})", r"\1.\2", srt_text)
    
    # Remove sequence numbers
    srt_text = re.sub(r"^\d+\s*$", "", srt_text, flags=re.MULTILINE)
    
    # Ensure proper spacing
    vtt_text += srt_text.strip() + "\n"
    
    return vtt_text

class SubtitlesAPI:
    def __init__(self):
        self.api_key = OPEN_SUBTITLES_API_KEY
        self.username = OPEN_SUBTITLES_USERNAME
        self.password = OPEN_SUBTITLES_PASSWORD
        self.client = OpenSubtitles("MyApp v1.0.0", self.api_key)
        self.client.login(username=self.username, password=self.password)

    def download_subtitle(self, tmdb_id: int, season_number: int = None, episode_number: int = None, language: str = "en"):
        response = self.client.search(
            tmdb_id=tmdb_id, 
            season_number=season_number, 
            episode_number=episode_number, 
            languages=language
        )
        if len(response.data) == 0:
            return None
        sub_data: Subtitle = response.data[0]
        sub_url = sub_data.file_id
        response_srt :bytes = self.client.download(sub_url)
        response_vtt = self.convert_srt_to_vtt(response_srt)
        return response_vtt
    
    def convert_srt_to_vtt(self, str_btyes: bytes) -> bytes:
        srt_string = self.client.bytes_to_str(str_btyes)
        response_vtt_string = srt_to_vtt(srt_string)
        return self.client.str_to_bytes(response_vtt_string)

if __name__ == "__main__":
    api = SubtitlesAPI()
    subtitle_url = api.download_subtitle(tmdb_id=95396, season_number=1, episode_number=4, language="en")
    print("subtitle_url", subtitle_url)