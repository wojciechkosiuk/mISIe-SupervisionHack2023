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
        link = request.POST['link']
        # Perform web scraping and job offer analysis
        # Set the values for is_fake, risk_value, and other fields accordingly
        text = "Sample text"
        date = "2023-05-20"
        author = "John Doe"
        key_words = "sample, keywords"
        semantic_value = 0.8
        is_fake = True
        
        # Save the job offer information to the database
        job_offer = JobOffer(
            link=link,
            text=text,
            date=date,
            author=author,
            key_words=key_words,
            semantic_value=semantic_value,
            fakeFlag=is_fake
        )
        job_offer.save()
        
        return redirect('overall_analysis')  # Redirect to the second page
    
    return render(request, 'job_offer_analysis.html')

def prepare_plot_data(job_offers):
    plot_data = []

    # Prepare the necessary data for plotting
    for job_offer in job_offers:
        # Perform any necessary data processing
        # For demonstration purposes, let's assume we want to plot semantic values
        plot_data.append(job_offer.semantic_value)

    return plot_data

def overall_analysis(request):
    job_offers = JobOffer.objects.all()

    # Prepare data for plotting
    plot_data = prepare_plot_data(job_offers)

    # Generate the Plotly figure
    fig = go.Figure(data=go.Scatter(x=list(range(len(plot_data))), y=plot_data))
    fig.update_layout(
        xaxis_title='Job Offer Index',
        yaxis_title='Semantic Value',
        title='Semantic Value Trend'
    )

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    return render(request, 'overall_analysis.html', {'plot_html': plot_html})