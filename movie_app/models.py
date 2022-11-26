from django.contrib.auth.models import User
from django.db import models

class Director(models.Model):
    class Meta:
        verbose_name='Директор'
        verbose_name_plural = 'Директоры'

    name = models.CharField(max_length=50, verbose_name='Имя')
    def __str__(self):
        return self.name

    def movie_count(self):
        return len(self.movies.all())

class Movie(models.Model):
    class Meta:
        verbose_name='Фильм'
        verbose_name_plural = 'Фильмы'

    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Длительность')
    director = models.ForeignKey(Director, on_delete=models.PROTECT , null=True, related_name='movies')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    def rating(self):
        lst = [review.stars for review in self.reviews.all()]
        return (sum(lst) / len(lst)) if len(lst) != 0 else "No reviews yet"

class Review(models.Model):
    class Meta:
        verbose_name='Отзыв'
        verbose_name_plural = 'Отзывы'

    author = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    stars = models.FloatField(default=1 , verbose_name='Рейтинг' , choices=((1, '★'),
                                                                            (2, '★★'),
                                                                            (3, '★★★'),
                                                                            (4, '★★★★'),
                                                                            (5, '★★★★★'),))
    text = models.TextField(verbose_name='Текст')
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True, related_name='reviews' , verbose_name='Фильм')

    def __str__(self):
        if len(self.text) <= 50:
            return (self.author.username if self.author is not None else 'Anonymous') + ', ' \
                   + self.text + '; ' + self.movie.title
        return (self.author.username if self.author is not None else 'Anonymous') + ', ' \
               + self.text[0:50] + '...;  ' + self.movie.title