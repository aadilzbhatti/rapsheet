from django.db import models

class Tweet(models.Model):
    text = models.CharField(max_length=140)
    sentiment = models.FloatField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return str(self.text)

    def create(self, text, sentiment, pub_date):
        self.text = text
        self.sentiment = sentiment
        self.pub_date = pub_date

class Album(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    release_date = models.DateTimeField()
    sales = models.IntegerField()

    def __str__(self):
        return self.artist + ' - ' + self.title

# TODO add artists, songs as well
