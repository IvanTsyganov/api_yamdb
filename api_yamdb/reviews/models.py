from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)
 
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField('Genre_Title')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name


class Genre_Title():
    title = models.ForeignKey(
        'Title',
        on_delete= models.CASCADE,
        related_name='genres_titles',
        verbose_name='Жанр'

    )
    
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name='genres_titles'
    )

    def __str__(self):
        return 