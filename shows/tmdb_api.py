from django.conf import settings
import requests


class TmdbApi:
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.read_access_token = settings.TMDB_READ_ACCESS_TOKEN
        self.base_url = "https://api.themoviedb.org/3"
        self.base_image_url = "https://image.tmdb.org/t/p/w500"
        self.base_original_image_url = "https://image.tmdb.org/t/p/original"

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
    
    def get_all_trending_shows(self, time_window: str = "day"):
        response = self.get(f"/trending/all/{time_window}")
        for show in response["results"]:
            show["poster_path"] = f"{self.base_image_url}{show['poster_path']}"
            show["backdrop_path"] = f"{self.base_image_url}{show['backdrop_path']}"
        return response

    def get_movie_details(self, movie_id: int):
        response = self.get(f"/movie/{movie_id}")
        response["backdrop_path"] = f"{self.base_original_image_url}{response['backdrop_path']}"
        response["poster_path"] = f"{self.base_original_image_url}{response['poster_path']}"
        return response
    
    def get_tv_show_details(self, tv_show_id: int):
        response = self.get(f"/tv/{tv_show_id}")
        response["backdrop_path"] = f"{self.base_original_image_url}{response['backdrop_path']}"
        response["poster_path"] = f"{self.base_original_image_url}{response['poster_path']}"
        return response
    
    def search_all(self, query: str):
        response = self.get("/search/multi", {"query": query, "include_adult": True})
        for result in response["results"]:
            if result.get("media_type") in ["tv", "movie"] and (result.get("poster_path") or result.get("backdrop_path")):
                result["poster_path"] = f"{self.base_image_url}{result['poster_path']}"
                result["backdrop_path"] = f"{self.base_image_url}{result['backdrop_path']}"
        response["results"] = [result for result in response["results"] if result.get("media_type") in ["tv", "movie"] and (result.get("poster_path") or result.get("backdrop_path"))]
        return response
    
    def get_popular_shows(self, media_type: str = "tv"):
        response = self.get(f"/{media_type}/popular")
        for show in response["results"]:
            show["poster_path"] = f"{self.base_image_url}{show['poster_path']}"
            show["backdrop_path"] = f"{self.base_image_url}{show['backdrop_path']}"
            show["media_type"] = media_type
        return response

if __name__ == "__main__":
    tmdb_api = TmdbApi()
    print(tmdb_api.get_movie_details(950396))
    

