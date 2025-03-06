from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowsViewSet, ShowWatchProgressViewSet, WatchlistViewSet

router = DefaultRouter()
router.register(r'shows', ShowsViewSet, basename='shows')
router.register(r'show-watch-progress', ShowWatchProgressViewSet, basename='show-watch-progress')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')

shows_urls = [
    path('', include(router.urls)),
]