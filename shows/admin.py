from django.contrib import admin
from .models import ShowWatchProgress, MovieProgress, TvProgress, WatchUrl, Watchlist
# Register your models here.

class TvProgressInline(admin.TabularInline):
    model = TvProgress
    extra = 1

class MovieProgressInline(admin.TabularInline):
    model = MovieProgress
    extra = 1

@admin.register(ShowWatchProgress)
class ShowWatchProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'tmdb_id', 'media_type')
    list_filter = ('media_type',)
    search_fields = ('user__username', 'title', 'tmdb_id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TvProgressInline, MovieProgressInline]


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'tmdb_id', 'media_type')
    list_filter = ('media_type',)
    search_fields = ('user__username', 'title', 'tmdb_id')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(WatchUrl)
class WatchUrlAdmin(admin.ModelAdmin):
    list_display = ('title', 'tmdb_id', 'media_type', 'season', 'episode', 'created_at', 'updated_at')
    list_filter = ('media_type',)
    search_fields = ('tmdb_id', 'title')
    readonly_fields = ('created_at', 'updated_at', 'url', 'poster_path', 'backdrop_path', 'season', 'episode', 'tmdb_id', 'media_type', 'title')

