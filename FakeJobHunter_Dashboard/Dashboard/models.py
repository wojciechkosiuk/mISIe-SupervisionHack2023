from django.db import models

# Define JobOffer model
class JobOffer(models.Model):
    link = models.URLField()
    text = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=100)
    length = models.IntegerField()
    uppercase_counter = models.IntegerField()
    exclamation_mark_counter = models.IntegerField()
    currency_mark_counter = models.IntegerField()
    non_polish_counter = models.IntegerField()
    emotional_words_counter = models.IntegerField()
    possible_contact = models.CharField(max_length=255)
    possible_mail = models.CharField(max_length=255)
    categories = models.CharField(max_length=255)
    fake_probability = models.FloatField()
    risk_value = models.IntegerField(null=True, blank=True)