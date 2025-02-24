from django.shortcuts import render
from rest_framework import viewsets
from shows.tmdb_api import TmdbApi
from shows.serializers import TrendingShowsResponseSerializer, MovieDetailSerializer, TvDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
# Create your views here.

class ShowsViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    queryset = None
    
    @action(detail=False, methods=["GET"], serializer_class=TrendingShowsResponseSerializer)
    def trending(self, request):
        tmdb_api = TmdbApi()
        trending_shows = tmdb_api.get_all_trending_shows()
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