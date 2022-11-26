from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie,Director,Review


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id username first_name last_name email'.split()


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()
    class Meta:
        model = Director
        fields = '__all__'

    def get_movies_count(self, director):
        return director.movie_count()

class MovieSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = 'id title description duration director rating'

    def get_rating(self,movie):
        return movie.rating()

class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'title'.split()


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer()
    movie = MovieNameSerializer()
    class Meta:
        model = Review
        fields = '__all__'

class ReviewOnMovieSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Review

        fields = 'id author text stars'.split()

class FilmListSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    reviews = ReviewOnMovieSerializer(many=True)
    class Meta:
        model = Movie
        fields = 'id title description duration director reviews rating'.split()

    def get_rating(self, movei):
        return movei.rating()

