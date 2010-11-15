from django.db import models

# Create your models here.
class Song(models.Model):
	play_time = models.TimeField()
	artist = models.CharField(max_length = 200)
	title = models.CharField(max_length = 200)
	album = models.CharField(max_length = 200)
	itunes_url = models.URLField(null = True)
	sample_url = models.URLField(null = True)
	albumart_url = models.URLField(null = True)

class Playlist(models.Model):
	uid = models.CharField(max_length = 20)
	songs = models.ManyToManyField(Song)
