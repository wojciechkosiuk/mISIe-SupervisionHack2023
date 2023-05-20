from django.db import models

# Define JobOffer model
class JobOffer(models.Model):
    link = models.URLField()
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    key_words = models.CharField(max_length=255)
    semantic_value = models.FloatField()
    fakeFlag = models.BooleanField(default=False)