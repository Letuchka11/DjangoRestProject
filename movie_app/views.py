from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def director_view(request):
    if request.method == 'GET':
        print(request.user)
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        director_name = serializer.validated_data["name"]
        dir = Director.objects.create(name=director_name,)
        dir.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={
                            "message" : "Director was created!",
                            "Director" : DirectorSerializer(dir).data
                        })

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def director_id_view(request, **kwargs):
    try:
        directors = Director.objects.get(id=kwargs['id'])
    except Director.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    if request.method == "GET":
        serializer = DirectorSerializer(directors, many=False)
        return Response(data=serializer.data)
    elif request.method == "DELETE":
        directors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = DirectorValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        name = serializer.validated_data["name"]
        directors.name = name
        directors.save()
        return Response(data={
            "message" : "Operation done successfuly"
        })
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_view(request, **kwargs):
    if request.method == 'GET':
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return Response(data=serializer.data)
    else:
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        duration = serializer.validated_data['duration']
        director = serializer.validated_data['director']
        movie = Movie.objects.create(title=title, description=description,
                                     duration=duration, director_id=director)
        movie.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={
                            "message": "Movie was created!"
                        })

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def movie_id_view(request, **kwargs):
    try:
        movie = Movie.objects.get(id=kwargs['id'])
    except Movie.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    if request.method =='GET':
        serializer = MovieSerializer(movie, many=False)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        duration = serializer.validated_data['duration']
        director = serializer.validated_data['director']
        movie = Movie.objects.create(title=title, description=description,
                                     duration=duration, director_id=director)
        movie.save()
        return Response(data={
            "message": "Movie was updated"
        })
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data=status.HTTP_204_NO_CONTENT)
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def review_view(request):
    review = Review.objects.all()
    if request.method == 'GET':
        serizlizer = ReviewSerializer(review, many=True)
        return Response(data=serizlizer.data)
    else:
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        stars = serializer.validated_data["stars"]
        text =  serializer.validated_data["text"]
        movie_id =  serializer.validated_data["movie_id"]
        # movie = request.data['movie']
        reviewAPI = Review.objects.create(author=request.user,stars=stars,text=text,movie=movie_id)
        reviewAPI.save()
        return Response(status=status.HTTP_201_CREATED,data={
            "message": "Review was created"
        })

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def review_id_view(request, **kwargs):
    try:
        review = Review.objects.get(id=kwargs['id'])
    except Review.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    if request.method == "GET":
        serizlizer = ReviewSerializer(review, many=False)
        return Response(data=serizlizer.data)
    elif request.method == "PUT":
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'errors': serializer.errors})
        author = request.data.get("author", None)
        stars = serializer.validated_data["stars"]
        text = serializer.validated_data["text"]
        movie = serializer.validated_data["movie"]
        reviewAPI = Review.objects.create(author=author, stars=stars, text=text, movie=movie)
        reviewAPI.save()
        return Response(data={
            "message": "Review was updated"
        })
    elif request.method == "DELETE":
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def film_list_review_view(request):
    movie = Movie.objects.all()
    serializer = FilmListSerializer(movie, many=True)
    return Response(data=serializer.data)
