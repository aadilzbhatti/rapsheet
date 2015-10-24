from django.db import models

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    author = models.CharField(max_length=50)
    date = models.DateTimeField
