from django.urls import path

from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('job-offer-analysis/', views.job_offer_analysis, name='joa'),
    path('overall-analysis/', views.overall_analysis, name='oa'),
]
