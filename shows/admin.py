from django.contrib import admin
from .models import ShowWatchProgress, MovieProgress, TvProgress
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
    inlines = [TvProgressInline, MovieProgressInline]

