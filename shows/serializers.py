from rest_framework import serializers

from shows.models import MovieProgress, ShowWatchProgress, TvProgress


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

class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()

class MovieDetailSerializer(serializers.Serializer):
    adult = serializers.BooleanField()
    backdrop_path = serializers.CharField(allow_null=True)
    belongs_to_collection = serializers.JSONField(allow_null=True)
    budget = serializers.IntegerField()
    genres = GenreSerializer(many=True)
    homepage = serializers.CharField(allow_null=True)
    id = serializers.IntegerField()
    imdb_id = serializers.CharField()
    original_language = serializers.CharField()
    original_title = serializers.CharField()
    overview = serializers.CharField()
    popularity = serializers.FloatField()
    poster_path = serializers.CharField(allow_null=True)
    production_companies = serializers.ListField(child=serializers.DictField())
    production_countries = serializers.ListField(child=serializers.DictField())
    release_date = serializers.DateField()
    revenue = serializers.IntegerField()
    runtime = serializers.IntegerField()
    spoken_languages = serializers.ListField(child=serializers.DictField())
    status = serializers.CharField()
    tagline = serializers.CharField()
    title = serializers.CharField()
    video = serializers.BooleanField()
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()

class TvDetailSerializer(serializers.Serializer):
    adult = serializers.BooleanField()
    backdrop_path = serializers.CharField(allow_null=True)
    created_by = serializers.ListField(child=serializers.DictField())
    episode_run_time = serializers.ListField(child=serializers.IntegerField())
    first_air_date = serializers.DateField()
    genres = GenreSerializer(many=True)
    homepage = serializers.CharField(allow_null=True)
    id = serializers.IntegerField()
    in_production = serializers.BooleanField()
    languages = serializers.ListField(child=serializers.CharField())
    last_air_date = serializers.DateField()
    last_episode_to_air = serializers.DictField(allow_null=True)
    name = serializers.CharField()
    next_episode_to_air = serializers.DictField(allow_null=True)
    networks = serializers.ListField(child=serializers.DictField())
    number_of_episodes = serializers.IntegerField()
    number_of_seasons = serializers.IntegerField()
    origin_country = serializers.ListField(child=serializers.CharField())
    original_language = serializers.CharField()
    original_name = serializers.CharField()
    overview = serializers.CharField()
    popularity = serializers.FloatField()
    poster_path = serializers.CharField(allow_null=True)
    production_companies = serializers.ListField(child=serializers.DictField())
    production_countries = serializers.ListField(child=serializers.DictField())
    seasons = serializers.ListField(child=serializers.DictField())
    spoken_languages = serializers.ListField(child=serializers.DictField())
    status = serializers.CharField()
    tagline = serializers.CharField()
    type = serializers.CharField()
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()

class TvEpisodeSerializer(serializers.Serializer):
    air_date = serializers.DateField()
    episode_number = serializers.IntegerField()
    id = serializers.IntegerField()
    name = serializers.CharField()
    overview = serializers.CharField()
    production_code = serializers.CharField()
    runtime = serializers.IntegerField()
    season_number = serializers.IntegerField()
    show_id = serializers.IntegerField()
    still_path = serializers.CharField(allow_null=True)
    vote_average = serializers.FloatField()
    vote_count = serializers.IntegerField()
    crew = serializers.ListField(child=serializers.DictField())
    guest_stars = serializers.ListField(child=serializers.DictField())


class TvEpisodesResponseSerializer(serializers.Serializer):
    _id = serializers.CharField()
    air_date = serializers.DateField()
    episodes = TvEpisodeSerializer(many=True)
    name = serializers.CharField()
    overview = serializers.CharField()
    id = serializers.IntegerField()
    poster_path = serializers.CharField(allow_null=True)
    season_number = serializers.IntegerField()
    vote_average = serializers.FloatField()


class TvProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = TvProgress
        fields = ['id', 'season', 'episode', 'watched_seconds', 'total_seconds']
        read_only_fields = ['id']

class MovieProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieProgress
        fields = ['id', 'watched_seconds', 'total_seconds']
        read_only_fields = ['id']

class ShowWatchProgressSerializer(serializers.ModelSerializer):
    tv_progress = TvProgressSerializer(many=True, allow_null=True)
    movie_progress = MovieProgressSerializer(many=True, allow_null=True)
    last_watched_episode = TvProgressSerializer(allow_null=True, read_only=True)

    class Meta:
        model = ShowWatchProgress
        fields = ['id', 'user', 'media_type', 'tmdb_id', 'poster_path', 'backdrop_path', 'title', 'created_at', 'tv_progress', 'movie_progress', 'last_watched_episode']
        read_only_fields = ['id', 'created_at', 'last_watched_episode', 'user']

    def create(self, validated_data):
        # get user from request
        user = self.context['request'].user
        validated_data['user'] = user


        tv_progress_data = validated_data.pop('tv_progress', None)
        movie_progress_data = validated_data.pop('movie_progress', None)

        # create show watch progress or update it if it already exists
        show_watch_progress, created = ShowWatchProgress.objects.get_or_create(
            user=user, media_type=validated_data['media_type'], tmdb_id=validated_data['tmdb_id']
        )
        show_watch_progress.poster_path = validated_data['poster_path']
        show_watch_progress.backdrop_path = validated_data['backdrop_path']
        show_watch_progress.title = validated_data['title']
        show_watch_progress.save()

        if tv_progress_data:
            for tv_progress in tv_progress_data:
                # remove id from tv_progress if it exists
                tv_progress.pop('id', None)
                # add show_watch_progress to tv_progress
                tv_progress['show_watch_progress'] = show_watch_progress
                # create tv progress or update it if it already exists
                new_tv_progress, created = TvProgress.objects.get_or_create(show_watch_progress=show_watch_progress, season=tv_progress['season'], episode=tv_progress['episode'])
                new_tv_progress: TvProgress = new_tv_progress
                new_tv_progress.watched_seconds = tv_progress['watched_seconds']
                new_tv_progress.total_seconds = tv_progress['total_seconds']
                new_tv_progress.save()
        if movie_progress_data:
            for movie_progress in movie_progress_data:
                # remove id from movie_progress if it exists
                movie_progress.pop('id', None)
                # add show_watch_progress to movie_progress
                movie_progress['show_watch_progress'] = show_watch_progress
                # create movie progress or update it if it already exists
                new_movie_progress, created = MovieProgress.objects.get_or_create(show_watch_progress=show_watch_progress)
                new_movie_progress: MovieProgress = new_movie_progress
                new_movie_progress.watched_seconds = movie_progress['watched_seconds']
                new_movie_progress.total_seconds = movie_progress['total_seconds']
                new_movie_progress.save()
        return show_watch_progress
