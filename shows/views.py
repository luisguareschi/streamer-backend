from django.shortcuts import render
from rest_framework import viewsets
from shows.tmdb_api import TmdbApi
from shows.serializers import ArchiveShowSerializer, IsInWatchlistResponseSerializer, IsInWatchlistSerializer, ShowWatchProgressSerializer, TrendingShowsResponseSerializer, MovieDetailSerializer, TvDetailSerializer, TvEpisodesResponseSerializer, WatchlistSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from shows.models import ShowWatchProgress, MovieProgress, TvProgress, Watchlist
# Create your views here.

class ShowsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = None
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name="time_window", description="Time window", required=False, type=str, default="day", enum=["day", "week"])
        ]
    )
    @action(detail=False, methods=["GET"], serializer_class=TrendingShowsResponseSerializer)
    def trending(self, request):
        time_window = request.query_params.get("time_window", "day")
        tmdb_api = TmdbApi()
        trending_shows = tmdb_api.get_all_trending_shows(time_window=time_window)
        serializer = self.get_serializer(data=trending_shows)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(trending_shows)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], serializer_class=MovieDetailSerializer, url_path="movie/(?P<pk>\d+)")
    def movie(self, request, pk):
        tmdb_api = TmdbApi()
        movie = tmdb_api.get_movie_details(pk)
        serializer = self.get_serializer(data=movie)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(movie)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], serializer_class=TvDetailSerializer, url_path="tv/(?P<pk>\d+)")
    def tv(self, request, pk):
        tmdb_api = TmdbApi()
        tv = tmdb_api.get_tv_show_details(pk)
        serializer = self.get_serializer(data=tv)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(tv)
        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name="query", description="Query string", required=True, type=str)
        ]
    )
    @action(detail=False, methods=["GET"], serializer_class=TrendingShowsResponseSerializer)
    def search(self, request):
        tmdb_api = TmdbApi()
        query = request.query_params.get("query", None)
        if not query:
            return Response({"error": "Query string is required"}, status=status.HTTP_400_BAD_REQUEST)
        search_results = tmdb_api.search_all(query)
        serializer = self.get_serializer(data=search_results)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(search_results)
        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name="media_type", description="Media type", required=False, type=str, default="tv", enum=["tv", "movie"])
        ]
    )
    @action(detail=False, methods=["GET"], serializer_class=TrendingShowsResponseSerializer)
    def popular(self, request):
        media_type = request.query_params.get("media_type", "tv")
        tmdb_api = TmdbApi()
        popular_shows = tmdb_api.get_popular_shows(media_type=media_type)
        serializer = self.get_serializer(data=popular_shows)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(popular_shows)
        return Response(serializer.data)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name="tv_id", description="TV ID", required=True, type=int),
            OpenApiParameter(name="season_number", description="Season number", required=True, type=int)
        ]
    )
    @action(detail=False, methods=["GET"], serializer_class=TvEpisodesResponseSerializer)
    def get_tv_episodes(self, request):
        tv_id = request.query_params.get("tv_id", None)
        season_number = request.query_params.get("season_number", None)
        if not tv_id or not season_number:
            return Response({"error": "tv_id and season_number are required"}, status=status.HTTP_400_BAD_REQUEST)
        tmdb_api = TmdbApi()
        episodes = tmdb_api.get_tv_show_episodes(tv_id, season_number)
        serializer = self.get_serializer(data=episodes)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(episodes)
        return Response(serializer.data)


class ShowWatchProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ShowWatchProgressSerializer

    def get_queryset(self):
        query = ShowWatchProgress.objects.filter(archived=False).order_by('-updated_at')
        if self.request.user.is_authenticated:
            return query.filter(user=self.request.user)
        return query

    @action(detail=False, methods=["GET"], serializer_class=ShowWatchProgressSerializer, url_path="progress/(?P<tmdb_id>\d+)")
    def get_show_watch_progress(self, request, tmdb_id):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        show_watch_progress = ShowWatchProgress.objects.filter(user=user, tmdb_id=tmdb_id).first()
        if not show_watch_progress:
            return Response(None, status=status.HTTP_200_OK)
        serializer = self.get_serializer(show_watch_progress)
        return Response(serializer.data)
    
    @extend_schema(
        responses={
            200: ShowWatchProgressSerializer,
        }
    )
    @action(detail=False, methods=["POST"], serializer_class=ArchiveShowSerializer)
    def archive_show(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        show_watch_progress = ShowWatchProgress.objects.filter(user=user, tmdb_id=serializer.data["tmdb_id"]).first()
        if not show_watch_progress:
            return Response({"error": "Show watch progress not found"}, status=status.HTTP_404_NOT_FOUND)
        show_watch_progress.archived = True
        response = show_watch_progress.save()
        serializer = self.get_serializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WatchlistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchlistSerializer
    

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)
    
    @extend_schema(
        responses={
            200: IsInWatchlistResponseSerializer,
        }
    )
    @action(detail=False, methods=["POST"], serializer_class=IsInWatchlistSerializer)
    def is_in_watchlist(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        watchlist = Watchlist.objects.filter(user=user, tmdb_id=serializer.data["tmdb_id"]).first()
        serializer = IsInWatchlistResponseSerializer(data={"is_in_watchlist": watchlist is not None})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)