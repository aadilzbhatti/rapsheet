from django.db import models

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    author = models.CharField(max_length=50)
    date = models.DateTimeField

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_date = models.DateTimeField
    sales = models.IntegerField