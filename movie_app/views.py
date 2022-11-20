from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Director,Movie,Review
from .serializers import DirectorSerializer , MovieSerializer, ReviewSerializer


@api_view(['GET'])
def director_view(request):
    directors = Director.objects.all()
    serializer = DirectorSerializer(directors, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def director_id_view(request, **kwargs):
    try:
        directors = Director.objects.get(id=kwargs['id'])
    except Director.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    serializer = DirectorSerializer(directors, many=False)
    return Response(data=serializer.data)

@api_view(['GET'])
def movie_view(request):
    movie = Movie.objects.all()
    serializer = MovieSerializer(movie, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def movie_id_view(request, **kwargs):
    try:
        movie = Movie.objects.get(id=kwargs['id'])
    except Movie.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    serializer = MovieSerializer(movie, many=False)
    return Response(data=serializer.data)

@api_view(['GET'])
def review_view(request):
    review = Review.objects.all()
    serizlizer = ReviewSerializer(review, many=True)
    return Response(data=serizlizer.data)

@api_view(['GET'])
def review_id_view(request, **kwargs):
    try:
        review = Review.objects.get(id=kwargs['id'])
    except Review.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    serizlizer = ReviewSerializer(review, many=False)
    return Response(data=serizlizer.data)


@api_view(['GET'])
def test_view(request):
    dict_ = {
        'hello' : "Hi",
        123 : "345",
        'int': 1111,
        'float' : 1.22,
        'true' : True

    }
    return Response(data=dict_)
