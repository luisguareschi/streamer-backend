from django.shortcuts import render
from rest_framework import viewsets
from shows.tmdb_api import TmdbApi
from shows.serializers import TrendingShowsResponseSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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

