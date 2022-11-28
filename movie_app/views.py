from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *

@api_view(['GET', 'POST'])
def director_view(request):
    if request.method == 'GET':
        print(request.data)
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return Response(data=serializer.data)
    elif request.method == "POST":
        director_name = request.data.get("name","")
        dir = Director.objects.create(name=director_name,)
        dir.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={
                            "message" : "Director was created!",
                            "Director" : DirectorSerializer(dir).data
                        })

@api_view(['GET', 'PUT', 'DELETE'])
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
        name = Director.objects.get("name","")
        directors.name = name
        directors.save()
        return Response(data={
            "message" : "Operation done successfuly"
        })
@api_view(['GET', 'POST'])
def movie_view(request):
    if request.method == 'GET':
        movie = Movie.objects.all()
        serializer = MovieSerializer(movie, many=True)
        return Response(data=serializer.data)
    else:
        title = request.data.get("title", "")
        description = request.data.get("description", "")
        duration = request.data.get("duration", None)
        director = request.data.get("director_id", None)
        movie = Movie.objects.create(title=title, description=description,
                                     duration=duration, director_id=director)
        movie.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={
                            "message": "Movie was created!"
                        })

@api_view(['GET','PUT','DELETE'])
def movie_id_view(request, **kwargs):
    try:
        movie = Movie.objects.get(id=kwargs['id'])
    except Movie.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    if request.method =='GET':
        serializer = MovieSerializer(movie, many=False)
        return Response(data=serializer.data)
    elif request.method == 'PUT':
        title = request.data.get("title", "")
        description = request.data.get("description", "")
        duration = request.data.get("duration", None)
        director = request.data.get("director_id", None)
        movie.title = title
        movie.description = description
        movie.duration = duration
        movie.director = director
        movie.save()
        return Response(data={
            "message": "Movie was updated"
        })
    elif request.method == 'DELETE':
        movie.delete()
        return Response(data=status.HTTP_204_NO_CONTENT)
@api_view(['GET','POST'])
def review_view(request):
    review = Review.objects.all()
    if request.method == 'GET':
        serizlizer = ReviewSerializer(review, many=True)
        return Response(data=serizlizer.data)
    else:
        author = request.data.get("author", None)
        stars = request.data.get("stars",1)
        text =  request.data.get("text","")
        movie =  request.data.get("movie",None)
        reviewAPI = Review.objects.create(author=author,stars=stars,text=text,movie=movie)
        reviewAPI.save()
        return Response(status=status.HTTP_201_CREATED,data={
            "message": "Review was created"
        })

@api_view(['GET','PUT','DELETE'])
def review_id_view(request, **kwargs):
    try:
        review = Review.objects.get(id=kwargs['id'])
    except Review.DoesNotExist:
        return Response(data={'error' : 'Not found!'})
    if request.method == "GET":
        serizlizer = ReviewSerializer(review, many=False)
        return Response(data=serizlizer.data)
    elif request.method == "PUT":
        author = request.data.get("author", None)
        stars = request.data.get("stars", 1)
        text = request.data.get("text", "")
        movie = request.data.get("movie", None)
        review.author = author
        review.stars = stars
        review.text = text
        review.movie = movie
        review.save()
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
def film_list_review_view(request):
    movie = Movie.objects.all()
    serializer = FilmListSerializer(movie, many=True)
    return Response(data=serializer.data)
