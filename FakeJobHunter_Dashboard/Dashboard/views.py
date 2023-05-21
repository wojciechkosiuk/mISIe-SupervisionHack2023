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
    if request.method == 'POST':

        if 'risk' in request.POST:

            # Risk Value form submitted
            risk_value = request.POST['risk']
            link = request.POST['link']


            job_offer = JobOffer.objects.get(link=link)
            job_offer.risk_value = risk_value
            job_offer.save()
            context = {
                'job_offer_info': job_offer,
            }
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
                ROW = predict_and_get_cols(df,'model/iso_model.pkl')
                print(ROW)

                job_offer = JobOffer.objects.filter(link=link).first()
                if job_offer:
                    # Row with the same link already exists
                    job_offer_info = JobOffer.objects.get(link=link)
                    context = {
                        'message': 'This link is already in the database!',
                        'job_offer_info': job_offer_info,
                        'correct_link': True
                    }

                # Perform web scraping and job offer analysis
                # Retrieve the relevant information for the job offer from the analysis

                #Save the job offer information to the database
                else:
                    job_offer = create_random(link=link)
                    job_offer.save()
                    # Retrieve the job offer information from the database
                    job_offer_info = JobOffer.objects.get(link=link)

                    # Pass the job offer information to the template
                    context = {
                        'job_offer_info': job_offer_info,
                        'correct_link': True
                    }
                return render(request, 'job_offer_analysis.html', context)
            
            else:

                context = {
                    'not_required_pages': 'olx or sprzedajemy domain required!'
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