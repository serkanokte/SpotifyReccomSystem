from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User



class Track(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genres = models.TextField(max_length=255)
    danceability = models.FloatField()
    energy = models.FloatField()
    loudness = models.FloatField()
    speechiness = models.FloatField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    popularity = models.FloatField()
    
    mfccmean_0 = models.FloatField()
    mfccmean_1 = models.FloatField()
    mfccmean_2 = models.FloatField()
    mfccmean_3 = models.FloatField()
    mfccmean_4 = models.FloatField()
    mfccmean_5 = models.FloatField()
    mfccmean_6 = models.FloatField()
    mfccmean_7 = models.FloatField()
    mfccmean_8 = models.FloatField()
    mfccmean_9 = models.FloatField()
    mfccmean_10 = models.FloatField()
    mfccmean_11 = models.FloatField()
    mfccmean_12 = models.FloatField()

    mfccmedian_0 = models.FloatField()
    mfccmedian_1 = models.FloatField()
    mfccmedian_2 = models.FloatField()
    mfccmedian_3 = models.FloatField()
    mfccmedian_4 = models.FloatField()
    mfccmedian_5 = models.FloatField()
    mfccmedian_6 = models.FloatField()
    mfccmedian_7 = models.FloatField()
    mfccmedian_8 = models.FloatField()
    mfccmedian_9 = models.FloatField()
    mfccmedian_10 = models.FloatField()
    mfccmedian_11 = models.FloatField()
    mfccmedian_12 = models.FloatField()

    mfccstd_0 = models.FloatField()
    mfccstd_1 = models.FloatField()
    mfccstd_2 = models.FloatField()
    mfccstd_3 = models.FloatField()
    mfccstd_4 = models.FloatField()
    mfccstd_5 = models.FloatField()
    mfccstd_6 = models.FloatField()
    mfccstd_7 = models.FloatField()
    mfccstd_8 = models.FloatField()
    mfccstd_9 = models.FloatField()
    mfccstd_10 = models.FloatField()
    mfccstd_11 = models.FloatField()
    mfccstd_12 = models.FloatField()


    def __str__(self):
        return self.name


class TrackUserModel(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Track = models.ForeignKey(Track, on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    def __str__(self):
        return f"{self.User.pk} - {self.Track.pk} - {self.rating}"
    
    class Meta:
        unique_together = ['User', 'Track']

