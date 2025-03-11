from django.db import models
from shows.subtitles_api import SubtitlesAPI
from shows.tmdb_api import TmdbApi
from users.models import User
from django.core.files.base import ContentFile
# Create your models here.



class ShowWatchProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    media_type = models.CharField(max_length=10, choices=[('tv', 'tv'), ('movie', 'movie')], null=False, blank=False)
    tmdb_id = models.IntegerField(null=False, blank=False)
    poster_path = models.CharField(max_length=255, null=False, blank=False)
    backdrop_path = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.tmdb_id})"
    
    class Meta:
        unique_together = ('user', 'media_type', 'tmdb_id')

    @property
    def last_watched_episode(self):
        if self.media_type == 'movie':
            return None
        return self.tv_progress.order_by('-updated_at').first()
    
class MovieProgress(models.Model):
    show_watch_progress = models.ForeignKey(ShowWatchProgress, on_delete=models.CASCADE, related_name='movie_progress')
    watched_seconds = models.FloatField(default=0)
    total_seconds = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('show_watch_progress',)

    def __str__(self):
        return f"{self.show_watch_progress.user.username} - {self.show_watch_progress.title} ({self.show_watch_progress.tmdb_id})"



class TvProgress(models.Model):
    show_watch_progress = models.ForeignKey(ShowWatchProgress, on_delete=models.CASCADE, related_name='tv_progress')
    watched_seconds = models.FloatField(default=0)
    total_seconds = models.FloatField(default=0)
    season = models.IntegerField(default=0)
    episode = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('show_watch_progress', 'season', 'episode')
    
    def __str__(self):
        return f"{self.show_watch_progress.user.username} - {self.show_watch_progress.title} ({self.show_watch_progress.tmdb_id}) - S{self.season}E{self.episode}"
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    media_type = models.CharField(max_length=10, choices=[('tv', 'tv'), ('movie', 'movie')], null=False, blank=False)
    tmdb_id = models.IntegerField(null=False, blank=False)
    poster_path = models.CharField(max_length=255, null=False, blank=False)
    backdrop_path = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'media_type', 'tmdb_id')

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.tmdb_id})"
    
    
class WatchUrl(models.Model):
    tmdb_id = models.IntegerField(null=False, blank=False)
    media_type = models.CharField(max_length=10, choices=[('tv', 'tv'), ('movie', 'movie')], null=False, blank=False)
    url = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster_path = models.CharField(max_length=255, null=False, blank=False)
    backdrop_path = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    season = models.IntegerField(null=True, blank=True)
    episode = models.IntegerField(null=True, blank=True)
    en_subtitle = models.FileField(upload_to='subtitles/', null=True, blank=True)
    es_subtitle = models.FileField(upload_to='subtitles/', null=True, blank=True)

    def populate_details(self):
        tmdb_api = TmdbApi()
        result = None
        if self.media_type == 'tv':
            result = tmdb_api.get_tv_show_details(tv_show_id=self.tmdb_id)
        else:
            result = tmdb_api.get_movie_details(movie_id=self.tmdb_id)
        
        if result:
            self.poster_path = result['poster_path']
            self.backdrop_path = result['backdrop_path']
            self.title = result['name'] if self.media_type == 'tv' else result['title']
            self.save()
    
    def download_subtitles(self):
        if self.en_subtitle and self.es_subtitle:
            return

        subtitles_api = SubtitlesAPI()
        file_name_en = ""
        file_name_es = ""
        en_subtitle = None
        es_subtitle = None

        if self.media_type == 'tv':
            file_name_en = f"{self.title}S{self.season}E{self.episode}-en.srt"
            file_name_es = f"{self.title}S{self.season}E{self.episode}-es.srt"
            en_subtitle = subtitles_api.download_subtitle(tmdb_id=self.tmdb_id, season_number=self.season, episode_number=self.episode, language="en")
            es_subtitle = subtitles_api.download_subtitle(tmdb_id=self.tmdb_id, season_number=self.season, episode_number=self.episode, language="es")
        else:
            file_name_en = f"{self.title}-en.srt"
            file_name_es = f"{self.title}-es.srt"
            en_subtitle = subtitles_api.download_subtitle(tmdb_id=self.tmdb_id, language="en")
            es_subtitle = subtitles_api.download_subtitle(tmdb_id=self.tmdb_id, language="es")

        if en_subtitle:
            self.en_subtitle = ContentFile(en_subtitle, name=file_name_en)
        if es_subtitle:
            self.es_subtitle = ContentFile(es_subtitle, name=file_name_es)
        self.save()


    class Meta:
        unique_together = ('tmdb_id', 'media_type', 'season', 'episode')

    def __str__(self):
        if self.season and self.episode:
            return f"{self.title} ({self.tmdb_id}) - {self.media_type} - S{self.season}E{self.episode}"
        else:
            return f"{self.title} ({self.tmdb_id}) - {self.media_type}"
