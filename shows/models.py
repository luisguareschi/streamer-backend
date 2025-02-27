from django.db import models
from users.models import User
# Create your models here.



class ShowWatchProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    media_type = models.CharField(max_length=10, choices=[('tv', 'tv'), ('movie', 'movie')], null=False, blank=False)
    tmdb_id = models.IntegerField(null=False, blank=False)
    poster_path = models.CharField(max_length=255, null=False, blank=False)
    backdrop_path = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.tmdb_id})"
    
    class Meta:
        unique_together = ('user', 'media_type', 'tmdb_id')

    @property
    def last_watched_episode(self):
        if self.media_type == 'movie':
            return None
        return self.tv_progress.order_by('-season', '-episode').first()
    
class MovieProgress(models.Model):
    show_watch_progress = models.ForeignKey(ShowWatchProgress, on_delete=models.CASCADE, related_name='movie_progress')
    watched_seconds = models.FloatField(default=0)
    total_seconds = models.FloatField(default=0)

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

    class Meta:
        unique_together = ('show_watch_progress', 'season', 'episode')
    
    def __str__(self):
        return f"{self.show_watch_progress.user.username} - {self.show_watch_progress.title} ({self.show_watch_progress.tmdb_id}) - S{self.season}E{self.episode}"
    
