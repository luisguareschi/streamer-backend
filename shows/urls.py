from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShowsViewSet, ShowWatchProgressViewSet, WatchUrlViewSet, WatchlistViewSet

router = DefaultRouter()
router.register(r'shows', ShowsViewSet, basename='shows')
router.register(r'show-watch-progress', ShowWatchProgressViewSet, basename='show-watch-progress')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'watch', WatchUrlViewSet, basename='watch')

shows_urls = [
    path('', include(router.urls)),
]