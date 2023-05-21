from django.db import models
import random
import string

# Define JobOffer model
# class JobOffer(models.Model):
#     link = models.URLField()
#     text = models.TextField()
#     date = models.DateField()
#     author = models.CharField(max_length=100)
#     length = models.IntegerField()
#     uppercase_counter = models.IntegerField()
#     exclamation_mark_counter = models.IntegerField()
#     currency_mark_counter = models.IntegerField()
#     non_polish_counter = models.IntegerField()
#     emotional_words_counter = models.IntegerField()
#     possible_contact = models.CharField(max_length=255)
#     possible_mail = models.CharField(max_length=255)
#     categories = models.CharField(max_length=255)
#     fake_probability = models.FloatField()
#     risk_value = models.IntegerField(null=True, blank=True)

# class JobOffer(models.Model):
#     id = models.AutoField(primary_key=True)
#     link = models.URLField()
#     text = models.TextField()
#     author = models.CharField(max_length=500)
#     tfidf_sum = models.FloatField()
#     tfidf_mean = models.FloatField()
#     emotions_sum = models.IntegerField()
#     emotions_mean = models.FloatField()
#     text_length = models.IntegerField()
#     capital_letters_count = models.IntegerField()
#     numbers_count = models.IntegerField()
#     question_marks_count = models.IntegerField()
#     currency_signs_count = models.IntegerField()
#     capital_words_count = models.IntegerField()
#     non_polish_char_count = models.IntegerField()
#     keywords_counter = models.IntegerField()
#     ispossible_address = models.BooleanField()
#     ispossible_email = models.BooleanField()
#     ispossible_phone_numbers = models.BooleanField()
#     possible_address = models.CharField(max_length=200)
#     possible_email = models.CharField(max_length=200)
#     possible_phone_numbers = models.CharField(max_length=200)
#     label = models.IntegerField()
#     prob = models.FloatField()
#     risk_value = models.IntegerField(null=True, blank=True)


    # class JobOffer(models.Model):
    #     id = models.AutoField(primary_key=True)
    #     link = models.URLField()

from django.db import models

class JobOffer(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.URLField()
    description = models.TextField()
    preprocessed_description = models.TextField()
    #index = models.IntegerField()
    tfidf_sum = models.FloatField(null=True)
    tfidf_mean = models.FloatField(null=True)
    emotions_sum = models.IntegerField(null=True)
    emotions_mean = models.FloatField(null=True)
    text_length = models.IntegerField(null=True)
    capital_letters_count = models.IntegerField(null=True)
    numbers_count = models.IntegerField(null=True)
    question_marks_count = models.IntegerField(null=True)
    currency_signs_count = models.IntegerField(null=True)
    capital_words_count = models.IntegerField(null=True)
    possible_email = models.CharField(max_length=200,null=True)
    possible_address = models.CharField(max_length=200,null=True)
    non_polish_char_count = models.IntegerField(null=True)
    possible_phone_numbers = models.CharField(max_length=200,null=True)
    personal_info_keywords_count = models.IntegerField(null=True)
    inspiring_keywords_count = models.IntegerField(null=True)
    money_related_keywords_count = models.IntegerField(null=True)
    dodane_data = models.DateField(null=True)
    link_id = models.CharField(max_length=200,null=True)
    title = models.CharField(max_length=200,null=True)
    category_tree_item = models.CharField(max_length=200,null=True)
    user_profile_link = models.URLField(null=True)
    filters = models.CharField(max_length=200,null=True)
    pay_low = models.FloatField(null=True)
    pay_high = models.FloatField(null=True)
    pay_currency = models.CharField(max_length=200,null=True)
    pay_period = models.CharField(max_length=200,null=True)
    Lokalizacja = models.CharField(max_length=200,null=True)
    Wymiar_pracy = models.CharField(max_length=200,null=True)
    Typ_umowy = models.CharField(max_length=200,null=True)
    user_profile_link_hash = models.CharField(max_length=200,null=True)
    Predict_Flag = models.IntegerField(null=True)
    Predict_Prob = models.IntegerField(null=True)
    Explain = models.TextField(null=True)
    risk_value = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.description
