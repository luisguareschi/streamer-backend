from rest_framework import serializers


class TrendingShowSerializer(serializers.Serializer):
    # Common fields for both movies and TV shows
    id = serializers.IntegerField()
    backdrop_path = serializers.CharField(allow_null=True)
    poster_path = serializers.CharField(allow_null=True)
    overview = serializers.CharField()
    media_type = serializers.ChoiceField(choices=['tv', 'movie'])
    adult = serializers.BooleanField()
    original_language = serializers.CharField()
    genre_ids = serializers.ListField(child=serializers.IntegerField())
    popularity = serializers.FloatField()
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()

    # Movie-specific fields
    title = serializers.CharField(required=False)
    original_title = serializers.CharField(required=False)
    release_date = serializers.DateField(required=False)
    video = serializers.BooleanField(required=False)

    # TV show-specific fields
    name = serializers.CharField(required=False)
    original_name = serializers.CharField(required=False)
    first_air_date = serializers.DateField(required=False)
    origin_country = serializers.ListField(child=serializers.CharField(), required=False)

class TrendingShowsResponseSerializer(serializers.Serializer):
    results = TrendingShowSerializer(many=True)
    page = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    total_results = serializers.IntegerField()

