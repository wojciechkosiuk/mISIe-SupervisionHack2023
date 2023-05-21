from django.shortcuts import render, redirect
from .models import JobOffer
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.http import HttpResponse
import sys
sys.path.append('..')
import os
import re
import pickle
import numba
import cloudpickle
from django.http import HttpResponse
from copy import deepcopy
import random

# Add the parent directory to the Python path

print(sys.path)
from code.sprzedajemy_functions import *
from code.olx_functions import *
from code.scrape_functions import *
from code.text_preprocessing import *
from code.model import *
import base64
import plotly.graph_objects as go
from django.shortcuts import render
import random
import string
import pandas as pd
import numpy as np
import pandas as pd
from stempel import StempelStemmer
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import copy
from sklearn.feature_extraction.text import CountVectorizer
import datetime

def export_csv(request,df):

    csv_data = df.to_csv(index=False)

    response = HttpResponse(csv_data, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=data.csv'

    return response

def create_random(link):
    job_offer = JobOffer(
        link=link,
        text = ''.join(random.choices(string.ascii_letters + string.digits, k=5)),
        author = ''.join(random.choices(string.ascii_letters + string.digits, k=5)),
        tfidf_sum=random.uniform(0, 1),
        tfidf_mean=random.uniform(0, 1),
        emotions_sum=random.randint(0, 100),
        emotions_mean=random.uniform(0, 1),
        text_length=random.randint(0, 1000),
        capital_letters_count=random.randint(0, 100),
        numbers_count=random.randint(0, 100),
        question_marks_count=random.randint(0, 10),
        currency_signs_count=random.randint(0, 10),
        capital_words_count=random.randint(0, 100),
        non_polish_char_count=random.randint(0, 100),
        keywords_counter=random.randint(0, 100),
        ispossible_address=random.choice([True, False]),
        ispossible_email=random.choice([True, False]),
        ispossible_phone_numbers=random.choice([True, False]),
        possible_address=''.join(random.choices(string.ascii_letters + string.digits, k=5)),
        possible_email=''.join(random.choices(string.ascii_letters + string.digits, k=5)),
        possible_phone_numbers=''.join(random.choices(string.ascii_letters + string.digits, k=5)),
        label = random.randint(0, 100),
        prob = random.uniform(0, 1),
        risk_value = random.randint(1, 5)
    )
    return job_offer

def job_offer_analysis(request):
    df_all= pd.DataFrame({})
    if request.method == 'POST':

        if 'risk' in request.POST:

            # Risk Value form submitted
            risk_value = request.POST['risk']
            link = request.POST['link']

            df_all['risk_value'] = risk_value


            job_offer = JobOffer.objects.get(link=link)
            job_offer.risk_value = risk_value
            job_offer.save()
            context = {
                'job_offer_info': job_offer,
                'predict_flag_value': job_offer.Predict_Flag

            }
            #print(df_all.columns)
            randint = random.randint(1, 1e9)
            name = str(datetime.datetime.now())[:10] + " " +str(randint)
            
            df_all.to_csv(f"{name}.csv")
            return render(request, 'job_offer_analysis.html', context)

        else:
            # Link form submitted
            link = request.POST['link']

            if 'olx' in link or 'sprzedajemy' in link:

                df_olx = None
                df_sprzedajemy = None
                df_scraped = None
                # TU WEB SCRAPING Z ZAPISEM DO SYSTEMU
                if 'olx' in link:
                    df_olx = get_info_about_job_olx(url=link)
                    df_olx = adjust_olx_df(df_olx)
                    df_scraped = df_olx
                else:
                    df_sprzedajemy = get_info_about_job_sprzedajemy(url=link)
                    df_sprzedajemy = adjust_sprzedajemy_df(df_sprzedajemy)
                    df_scraped = df_sprzedajemy
                
                #print(df_scraped)

                df = create_final_dataframe(df_scraped)
                df_all = copy.deepcopy(df)
                randint = random.randint(1, 1e9)
                name = str(datetime.datetime.now())[:10] + " " +str(randint)
                df_all.to_csv(f"{name}.csv")

                ROW = predict_and_get_cols(df,'model/iso_model.pkl')
                #print(len(ROW.columns))

                job_offer = JobOffer.objects.filter(link=link).first()
                if job_offer:
                    # Row with the same link already exists
                    job_offer_info = JobOffer.objects.get(link=link)
                    context = {
                        'message': 'This link is already in the database!',
                        'job_offer_info': job_offer_info,
                        'correct_link': True,
                        'predict_flag_value': job_offer_info.Predict_Flag
                    }
                    #print(job_offer_info.Predict_Flag, "Xdxdxxdxdxddx")

                # Perform web scraping and job offer analysis
                # Retrieve the relevant information for the job offer from the analysis

                #Save the job offer information to the database
                else:

                    description = ROW['description'].values[0]
                    preprocessed_description = ROW['preprocessed_description'].values[0]
                    #index = ROW['index'].values[0]
                    tfidf_sum = ROW['tfidf_sum'].values[0]
                    tfidf_mean = ROW['tfidf_mean'].values[0]
                    emotions_sum = ROW['emotions_sum'].values[0]
                    emotions_mean = ROW['emotions_mean'].values[0]
                    text_length = ROW['text_length'].values[0]
                    capital_letters_count = ROW['capital_letters_count'].values[0]
                    numbers_count = ROW['numbers_count'].values[0]
                    question_marks_count = ROW['question_marks_count'].values[0]
                    currency_signs_count = ROW['currency_signs_count'].values[0]
                    capital_words_count = ROW['capital_words_count'].values[0]
                    possible_email = ROW['possible_email'].values[0]
                    possible_address = ROW['possible_address'].values[0]
                    non_polish_char_count = ROW['non_polish_char_count'].values[0]
                    possible_phone_numbers = ROW['possible_phone_numbers'].values[0]
                    personal_info_keywords_count = ROW['personal_info_keywords_count'].values[0]
                    inspiring_keywords_count = ROW['inspiring_keywords_count'].values[0]
                    money_related_keywords_count = ROW['money_related_keywords_count'].values[0]
                    dodane_data = ROW['dodane-data'].values[0]
                    link_id = ROW['id'].values[0]
                    title = ROW['title'].values[0]
                    category_tree_item = ROW['category-tree-item'].values[0]
                    user_profile_link = ROW['user-profile-link'].values[0]
                    filters = ROW['filters'].values[0]
                    pay_low = ROW['pay_low'].values[0]
                    pay_high = ROW['pay_high'].values[0]
                    pay_currency = ROW['pay_currency'].values[0]
                    pay_period = ROW['pay_period'].values[0]
                    Lokalizacja = ROW['Lokalizacja'].values[0]
                    Wymiar_pracy = ROW['Wymiar pracy'].values[0]
                    Typ_umowy = ROW['Typ umowy'].values[0]
                    user_profile_link_hash = ROW['user-profile-link-hash'].values[0]
                    Predict_Flag = ROW['Predict_Flag'].values[0]
                    Predict_Prob = ROW['Predict_Prob'].values[0]
                    Explain = ROW['Explain'].values[0]

                    # Create a new JobOffer object and save it to the database
                    job_offer = JobOffer(
                        link=link,
                        description=description,
                        preprocessed_description=preprocessed_description,
                        #index=index,
                        tfidf_sum=tfidf_sum,
                        tfidf_mean=tfidf_mean,
                        emotions_sum=emotions_sum,
                        emotions_mean=emotions_mean,
                        text_length=text_length,
                        capital_letters_count=capital_letters_count,
                        numbers_count=numbers_count,
                        question_marks_count=question_marks_count,
                        currency_signs_count=currency_signs_count,
                        capital_words_count=capital_words_count,
                        possible_email=possible_email,
                        possible_address=possible_address,
                        non_polish_char_count=non_polish_char_count,
                        possible_phone_numbers=possible_phone_numbers,
                        personal_info_keywords_count=personal_info_keywords_count,
                        inspiring_keywords_count=inspiring_keywords_count,
                        money_related_keywords_count=money_related_keywords_count,
                        dodane_data=dodane_data,
                        link_id=link_id,
                        title=title,
                        category_tree_item=category_tree_item,
                        user_profile_link=user_profile_link,
                        filters=filters,
                        pay_low=pay_low,
                        pay_high=pay_high,
                        pay_currency=pay_currency,
                        pay_period=pay_period,
                        Lokalizacja=Lokalizacja,
                        Wymiar_pracy=Wymiar_pracy,
                        Typ_umowy=Typ_umowy,
                        user_profile_link_hash=user_profile_link_hash,
                        Predict_Flag=Predict_Flag,
                        Predict_Prob=Predict_Prob,
                        Explain=Explain,
                        risk_value=None
                    )

                    job_offer.save()

                    # Retrieve the job offer information from the database
                    job_offer_info = JobOffer.objects.get(link=link)

                    # Pass the job offer information to the template
                    context = {
                        'job_offer_info': job_offer_info,
                        'correct_link': True,
                        'predict_flag_value': Predict_Flag
                    }
                    #print(Predict_Flag, "xdxdxdxdxxdxd")
                    #print('aha nie wnikkam')
                return render(request, 'job_offer_analysis.html', context)
            
            else:

                context = {
                    'not_required_pages': 'olx or sprzedajemy domain required!',
                   

                }

        return render(request, 'job_offer_analysis.html',context)
    
    return render(request, 'job_offer_analysis.html')



def prepare_plot_data(job_offers):
    plot_data = []

    # Prepare the necessary data for plotting
    for job_offer in job_offers:
        # Perform any necessary data processing
        # For demonstration purposes, let's assume we want to plot semantic values
        plot_data.append(job_offer.capital_words_count)

    return plot_data

def overall_analysis(request):
    job_offers = JobOffer.objects.all()

    # Prepare data for plotting
    plot_data = prepare_plot_data(job_offers)

    # Generate the Plotly figure
    fig = go.Figure(data=go.Scatter(x=list(range(len(plot_data))), y=plot_data))
    fig.update_layout(
        xaxis_title='Job Offer Index',
        yaxis_title='Uppercase Counter Value',
        title='Uppercase Counter Value Trend'
    )

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    return render(request, 'overall_analysis.html', {'plot_html': plot_html})