from opensubtitlescom import OpenSubtitles
from opensubtitlescom.responses import Subtitle

class SubtitlesAPI:
    def __init__(self):
        self.api_key = "mQ4ngZOXRRPrRt3o9N2k0hBoLtGOkEle"
        self.username = "luisguareschi"
        self.password = "luis2012"
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
        response = self.client.download(sub_url)
        return response

if __name__ == "__main__":
    api = SubtitlesAPI()
    subtitle_url = api.download_subtitle(tmdb_id=95396, season_number=1, episode_number=4, language="en")
    print("subtitle_url", subtitle_url)