from django.conf import settings
import requests


class TmdbApi:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.read_access_token = settings.TMDB_READ_ACCESS_TOKEN
        self.base_url = "https://api.themoviedb.org/3"

    def get(self, url: str, params: dict = None):
        response = requests.get(
            f"{self.base_url}/{url}",
            params=params,
            headers={"Authorization": f"Bearer {self.read_access_token}"},
        )
        return response.json()
    
    def get_trending_tv_shows(self):
        return self.get("/trending/tv/day")
    
    def get_trending_movies(self):
        return self.get("/trending/movie/day")
    
    def get_all_trending_shows(self):
        return self.get("/trending/all/day")
    

if __name__ == "__main__":
    tmdb_api = TmdbApi()
    print(tmdb_api.get_all_trending_shows())
    

