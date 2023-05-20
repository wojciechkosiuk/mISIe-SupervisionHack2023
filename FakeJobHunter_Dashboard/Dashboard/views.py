from django.shortcuts import render, redirect
from .models import JobOffer
import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.http import HttpResponse
import base64
import plotly.graph_objects as go
from django.shortcuts import render

def job_offer_analysis(request):
    if request.method == 'POST':

        if 'risk' in request.POST:

            # Risk Value form submitted
            risk_value = request.POST['risk']
            link = request.POST['link']

            # job_offer = JobOffer(
            #     link=link,
            #     text='Sample text',
            #     date='2023-05-20',
            #     author='John Doe',
            #     length=500,
            #     uppercase_counter=10,
            #     exclamation_mark_counter=3,
            #     currency_mark_counter=1,
            #     non_polish_counter=2,
            #     emotional_words_counter=5,
            #     possible_contact=True,
            #     possible_mail=True,
            #     categories='Software Development',
            #     fake_probability=0.75,
            #     risk_value=risk_value
            # )
            # job_offer.save()
            # Retrieve the job offer information from the database
            #job_offer_info = JobOffer.objects.get(link=link)

            # Update the job offer object with the risk value
            #job_offer_info = JobOffer.objects.get(link=link)

            # Pass the job offer information to the template
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
            # Perform web scraping and job offer analysis
            # Retrieve the relevant information for the job offer from the analysis

            #Save the job offer information to the database
            job_offer = JobOffer(
                link=link,
                text='Sample text',
                date='2023-05-20',
                author='John Doe',
                length=500,
                uppercase_counter=10,
                exclamation_mark_counter=3,
                currency_mark_counter=1,
                non_polish_counter=2,
                emotional_words_counter=5,
                possible_contact=True,
                possible_mail=True,
                categories='Software Development',
                fake_probability=0.75,
                risk_value=None
            )
            job_offer.save()

            # Retrieve the job offer information from the database
            job_offer_info = JobOffer.objects.get(link=link)

            # Pass the job offer information to the template
            context = {
                'job_offer_info': job_offer_info,
            }
            return render(request, 'job_offer_analysis.html', context)

    return render(request, 'job_offer_analysis.html')



def prepare_plot_data(job_offers):
    plot_data = []

    # Prepare the necessary data for plotting
    for job_offer in job_offers:
        # Perform any necessary data processing
        # For demonstration purposes, let's assume we want to plot semantic values
        plot_data.append(job_offer.uppercase_counter)

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