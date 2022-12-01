from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
        fields = 'id title description duration director rating'.split()

    def get_rating(self,movie):
        return movie.rating()

class MovieNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = 'id title'.split()


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


class DirectorValidateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=3,max_length=70)

class ReviewValidateSerializer(serializers.Serializer):
    movie = serializers.IntegerField(min_value=1)
    text = serializers.CharField(min_length=5)
    stars = serializers.FloatField(min_value=1)

class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=3,max_length=1000)
    description = serializers.CharField(min_length=5)
    duration = serializers.IntegerField(min_value=5)
    director_id = serializers.IntegerField(min_value=1)

    def validate_director_id(self,director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director not found")
        return director_id